import os
import json
import random
from equipo import Equipo
from colores import COLOR, COLOR_NEGRITA

class Torneo:
    
    EQUIPOS_PREDETERMINADOS = [
        "Almeria", "Athletic Club", "Atletico de Madrid", "Barcelona", "Cadiz", "Celta de Vigo", 
        "Deportivo Alaves", "Getafe", "Girona", "Granada", "Las Palmas", "Mallorca", "Osasuna", 
        "Rayo Vallecano", "Real Betis", "Real Madrid", "Real Sociedad", "Sevilla", "Valencia", "Villarreal"
    ]

    NUMERO_FECHAS = 6

    def __init__(self):
        self.equipos = {nombre: Equipo(nombre) for nombre in self.EQUIPOS_PREDETERMINADOS}
        self.calendario = self.generar_calendario()
        self.fechas_terminadas = []
        self.fecha_actual = 1
        self.torneo_terminado = False
        self.campeon = None
        self.equipos_ascendidos = []
        self.equipos_descendidos = []
        self.cargar_datos_json()

    def iniciar_nuevo_torneo(self):
        self.equipos = {nombre: Equipo(nombre) for nombre in self.EQUIPOS_PREDETERMINADOS}
        self.calendario = self.generar_calendario()
        self.fechas_terminadas = []
        self.fecha_actual = 1
        self.torneo_terminado = False
        self.campeon = None
        self.equipos_ascendidos = []
        self.equipos_descendidos = []
        self.guardar_datos_json()
        print(f"{COLOR['azul']}\n¡¡EXCELENTE!! Se ha creado un nuevo torneo.{COLOR['default']}")

    def generar_calendario(self):
        calendario = {}
        equipos = self.EQUIPOS_PREDETERMINADOS.copy()
        random.shuffle(equipos)  # Aleatorizamos los equipos
        
        for fecha in range(1, self.NUMERO_FECHAS + 1):
            enfrentamientos = []
            num_partidos = len(self.EQUIPOS_PREDETERMINADOS) // 2
            
            for i in range(num_partidos):
                local = equipos[i]
                visitante = equipos[num_partidos + i]
                enfrentamientos.append({local: None, visitante: None})
            
            calendario[str(fecha)] = enfrentamientos
            self.rotar_equipos(equipos)  # Rotamos los equipos para la siguiente fecha
        
        return calendario
    
    @staticmethod
    def rotar_equipos(equipos):
        ultimo_equipo = equipos.pop()
        equipos.insert(1, ultimo_equipo)

    def mostrar_calendario(self, fecha=None):
        # Preguntamos si se pasó el parametro fecha
        if fecha is not None:
            # Mostramos el calendario de la fecha elegida
            enfrentamientos = self.calendario[fecha]
            print(f"{COLOR_NEGRITA['azul']}\nCalendario de la fecha {fecha}:{COLOR['default']}") 
            for i, enfrentamiento in enumerate(enfrentamientos, start=1):
                print(f"Partido {i}: {list(enfrentamiento.keys())[0]} {COLOR['azul']}vs{COLOR['default']} {list(enfrentamiento.keys())[1]}")
                
        else:
            # Si no se pasó el parametro fecha mostramos el calendario completo de todas las fechas
            print(f"{COLOR['azul']}\nCalendario completo de enfrentamientos:{COLOR['default']}")
            for fecha, enfrentamientos in self.calendario.items():
                print(f"{COLOR['azul']}\nFecha {fecha}:{COLOR['default']}")
                for i, enfrentamiento in enumerate(enfrentamientos, start=1):
                    print(f"Partido {i}: {list(enfrentamiento.keys())[0]} {COLOR['azul']}vs{COLOR['default']} {list(enfrentamiento.keys())[1]}")
        
    def validar_fecha_anterior_terminada(self, fecha):
        fecha = int(fecha)
        
        if fecha == 1:
            return True  # No hay fecha anterior, se puede ingresar resultados para la fecha 1
        else:
            return str((fecha - 1)) in self.fechas_terminadas
    
    def partidos_completos_por_fecha(self, fecha):
        if fecha not in self.calendario:
            return False
        
        partidos = self.calendario[fecha]
        
        for partido in partidos:
            for equipo, resultado in partido.items():
                if resultado is None:
                    return False  # Si algún resultado es None, retornar False
        
        return True  # Si todos los resultados son diferentes de None, retornar True
    
    def ingresar_resultado(self, fecha, local, goles_local, visitante, goles_visitante):

        # Se busca el resultado del partido en el json para ver si es un partido que ya se ha jugado
        resultado_existente = None
        for resultado in self.calendario[fecha]:
            # Verificar si el partido ya tiene marcadores asignados
            if local in resultado and visitante in resultado:
                if resultado[local] is not None and resultado[visitante] is not None:
                    resultado_existente = True
                    break
                break

        if resultado_existente:
            # Se revierten las estadisticas del resultado anterior
            self.equipos[local].revertir_estadisticas(resultado[local], resultado[visitante])
            self.equipos[visitante].revertir_estadisticas(resultado[visitante], resultado[local])
            
        # Actualizar las estadísticas con el nuevo resultado
        self.equipos[local].actualizar_estadisticas(goles_local, goles_visitante)
        self.equipos[visitante].actualizar_estadisticas(goles_visitante, goles_local)

        # Actualizar resultado del partido ya existente
        resultado[local] = goles_local
        resultado[visitante] = goles_visitante
            
        # Validar si ya se tienen todos los resultados de una fecha para agregar la fecha como terminada
        if self.partidos_completos_por_fecha(fecha):
            if fecha not in self.fechas_terminadas:
                self.fechas_terminadas.append(fecha)
            if self.fecha_actual < self.NUMERO_FECHAS:
                self.fecha_actual += 1
        
        if len(self.fechas_terminadas) == self.NUMERO_FECHAS:
            self.terminar_torneo()
        
        self.guardar_datos_json()

    def simular_partidos_faltantes_por_fecha(self, fecha):
        if fecha not in self.calendario:
            print(f"{COLOR['rojo']}La fecha {fecha} no está en el calendario.{COLOR['default']}")
            return
        
        if not self.validar_fecha_anterior_terminada(fecha):
            print(f"{COLOR['rojo']}No se pueden ingresar resultados para esta fecha hasta que se jueguen todos los partidos de la fechas anteriores.{COLOR['default']}")
            return
                    
        if fecha in self.fechas_terminadas:
            print(f"{COLOR['rojo']}La fecha {fecha} ya está terminada.{COLOR['default']}")
            return
        
        # Simular resultados para los partidos que aún no tienen marcadores asignados
        for partido in self.calendario[fecha]:
            equipos = list(partido.keys())
            if partido[equipos[0]] is None or partido[equipos[1]] is None:
                goles_local = random.randint(0, 5)
                goles_visitante = random.randint(0, 5)
                partido[equipos[0]] = goles_local
                partido[equipos[1]] = goles_visitante
                self.equipos[equipos[0]].actualizar_estadisticas(goles_local, goles_visitante)
                self.equipos[equipos[1]].actualizar_estadisticas(goles_visitante, goles_local)
        
        # Validar si ya se tienen todos los resultados de una fecha para agregar la fecha como terminada
        
        if self.partidos_completos_por_fecha(fecha):
            if fecha not in self.fechas_terminadas:
                self.fechas_terminadas.append(fecha)
            if self.fecha_actual < self.NUMERO_FECHAS:
                self.fecha_actual += 1
        
        self.mostrar_resultados(fecha)
        
        if len(self.fechas_terminadas) == self.NUMERO_FECHAS:
            self.terminar_torneo()
         
        self.guardar_datos_json()
        
    def mostrar_resultados(self, fecha=None):
        if fecha is not None:
            # Mostrar resultados de partidos jugados solo de una fecha específica
            if fecha in self.calendario:
                print(f"{COLOR['azul']}\nResultados fecha {fecha}:{COLOR['default']}")
                for partido in self.calendario[fecha]:
                    equipos = list(partido.keys())
                    marcador_local = partido[equipos[0]]
                    marcador_visitante = partido[equipos[1]]
                    if marcador_local is not None and marcador_visitante is not None:
                        print(f"{equipos[0]} {COLOR['azul']}{marcador_local} - {marcador_visitante} {COLOR['default']}{equipos[1]}")
            else:
                print(f"{COLOR['rojo']}No existen resultados para la fecha especificada.{COLOR['default']}")
        else:
            # Mostrar todos los resultados de partidos jugados de todas las fechas
            for fecha in range(1, self.fecha_actual + 1):
                print(f"{COLOR['azul']}\nResultados fecha {fecha}:{COLOR['default']}")
                resultados_mostrados = False
                for partido in self.calendario[str(fecha)]:
                    equipos = list(partido.keys())
                    marcador_local = partido[equipos[0]]
                    marcador_visitante = partido[equipos[1]]
                    if marcador_local is not None and marcador_visitante is not None:
                        print(f"{equipos[0]} {COLOR['azul']}{marcador_local} - {marcador_visitante} {COLOR['default']}{equipos[1]}")
                        resultados_mostrados = True
            
            if not resultados_mostrados:
                print(f"{COLOR['rojo']}¡¡Esta es la fecha actual!! Aún no hay resultados.{COLOR['default']}")
 
    def mostrar_tabla_torneo(self):
        tabla = sorted(self.equipos.values(), key=lambda x: (x.puntos, x.diferencia_goles, x.goles_a_favor), reverse=True)
        print()
        print(f"{COLOR['azul']}{'Equipo':<20} {'J':<3} {'G':<3} {'E':<3} {'P':<3} {'GF':<3} {'GC':<3} {'DG':<4} {'Pts':<4}{COLOR['default']}")
        
        for i, equipo in enumerate(tabla, start=1):
            color = COLOR['default']
            if i <= 3:
                color = COLOR['verde']  # Primeros 3 equipos (ascenso) en verde
            elif i > len(tabla) - 3:
                color = COLOR['rojo']  # Últimos 3 equipos (descenso) en rojo
            
            print(f"{color}{equipo.nombre:<20} "
                f"{equipo.partidos_jugados:<3} "
                f"{equipo.partidos_ganados:<3} "
                f"{equipo.partidos_empatados:<3} "
                f"{equipo.partidos_perdidos:<3} "
                f"{equipo.goles_a_favor:<3} "
                f"{equipo.goles_en_contra:<3} "
                f"{equipo.diferencia_goles:<4} "
                f"{equipo.puntos:<4}{COLOR['default']}"
            )
        
         # Textos con emojis Unicode
        print(f"{COLOR['verde']}\nAscenso \N{UPWARDS ARROW}{COLOR['default']}")
        print(f"{COLOR['rojo']}Descenso \N{DOWNWARDS ARROW}{COLOR['default']}")

    def mostrar_estadisticas_generales(self):
        
        total_partidos_jugados = 0
        # Iterar sobre cada fecha en el calendario
        for partidos in self.calendario.values():
            # Iterar sobre cada enfrentamiento en la fecha
            for partido in partidos:
                # Verificar si el partido tiene marcadores definidos para ambos equipos
                if all(marcador is not None for marcador in partido.values()):
                    total_partidos_jugados += 1
        
        if total_partidos_jugados == 0:
            print(f"{COLOR['rojo']}\nNo se ha jugado ningun partido.{COLOR['default']}")
            print(f"{COLOR['rojo']}Ingrese resultados o simule fechas para ver estadisticas.{COLOR['default']}")
            return
        
        total_goles = sum(equipo.goles_a_favor for equipo in self.equipos.values())

        max_victorias = max(equipo.partidos_ganados for equipo in self.equipos.values())
        equipos_mas_victorias = [equipo.nombre for equipo in self.equipos.values() if equipo.partidos_ganados == max_victorias]

        max_empates = max(equipo.partidos_empatados for equipo in self.equipos.values())
        equipos_mas_empates = [equipo.nombre for equipo in self.equipos.values() if equipo.partidos_empatados == max_empates]

        max_derrotas = max(equipo.partidos_perdidos for equipo in self.equipos.values())
        equipos_mas_derrotas = [equipo.nombre for equipo in self.equipos.values() if equipo.partidos_perdidos == max_derrotas]

        max_puntos = max(equipo.puntos for equipo in self.equipos.values())
        equipos_mas_puntos = [equipo.nombre for equipo in self.equipos.values() if equipo.puntos == max_puntos]

        menos_puntos = min(equipo.puntos for equipo in self.equipos.values())
        equipos_menos_puntos = [equipo.nombre for equipo in self.equipos.values() if equipo.puntos == menos_puntos]

        max_goles_anotados = max(equipo.goles_a_favor for equipo in self.equipos.values())
        equipos_mas_goles_anotados = [equipo.nombre for equipo in self.equipos.values() if equipo.goles_a_favor == max_goles_anotados]

        max_goles_recibidos = max(equipo.goles_en_contra for equipo in self.equipos.values())
        equipos_mas_goles_recibidos = [equipo.nombre for equipo in self.equipos.values() if equipo.goles_en_contra == max_goles_recibidos]

        print(f"{COLOR['azul']}\nEstadísticas Generales del Torneo:\n{COLOR['default']}")
        print(f"{COLOR['azul']}- {COLOR['default']}Total de partidos jugados: {COLOR['azul']}{total_partidos_jugados}{COLOR['default']}")
        print(f"{COLOR['azul']}- {COLOR['default']}Total de goles anotados: {COLOR['azul']}{total_goles}{COLOR['default']}")
        print(f"{COLOR['azul']}- {COLOR['default']}Equipo(s) con más victorias: {', '.join(equipos_mas_victorias)} {COLOR['azul']}({max_victorias} victorias){COLOR['default']}")
        print(f"{COLOR['azul']}- {COLOR['default']}Equipo(s) con más empates: {', '.join(equipos_mas_empates)} {COLOR['azul']}({max_empates} empates){COLOR['default']}")
        print(f"{COLOR['azul']}- {COLOR['default']}Equipo(s) con más derrotas: {', '.join(equipos_mas_derrotas)} {COLOR['azul']}({max_derrotas} derrotas){COLOR['default']}")
        print(f"{COLOR['azul']}- {COLOR['default']}Equipo(s) con más puntos: {', '.join(equipos_mas_puntos)} {COLOR['azul']}({max_puntos} puntos){COLOR['default']}")
        print(f"{COLOR['azul']}- {COLOR['default']}Equipo(s) con menos puntos: {', '.join(equipos_menos_puntos)} {COLOR['azul']}({menos_puntos} puntos){COLOR['default']}")
        print(f"{COLOR['azul']}- {COLOR['default']}Equipo(s) con más goles anotados: {', '.join(equipos_mas_goles_anotados)} {COLOR['azul']}({max_goles_anotados} goles anotados){COLOR['default']}")
        print(f"{COLOR['azul']}- {COLOR['default']}Equipo(s) con más goles recibidos: {', '.join(equipos_mas_goles_recibidos)} {COLOR['azul']}({max_goles_recibidos} goles recibidos){COLOR['default']}")

    def mostrar_estadisticas_por_equipo(self, nombre_equipo):
        
        nombre_equipo = nombre_equipo.lower()  # Convertir el nombre del equipo ingresado a minúsculas
        equipo_encontrado = next((equipo for equipo in self.equipos.values() if equipo.nombre.lower() == nombre_equipo), None)

        if equipo_encontrado is None:
            print(f"El equipo {nombre_equipo} no se encuentra en el torneo")
            return
        
        print(f"{COLOR_NEGRITA['azul']}\nEstadísticas del {equipo_encontrado.nombre}:\n")
        print(f"{COLOR['azul']}-{COLOR['default']} Partidos jugados: {COLOR['azul']}{equipo_encontrado.partidos_jugados}")
        print(f"- {COLOR['default']}Partidos empatados: {COLOR['azul']}{equipo_encontrado.partidos_empatados}")
        print(f"- {COLOR['default']}Partidos perdidos: {COLOR['azul']}{equipo_encontrado.partidos_perdidos}")
        print(f"- {COLOR['default']}Partidos ganados: {COLOR['azul']}{equipo_encontrado.partidos_ganados}")
        print(f"- {COLOR['default']}Goles a favor: {COLOR['azul']}{equipo_encontrado.goles_a_favor}")
        print(f"- {COLOR['default']}Goles en contra: {COLOR['azul']}{equipo_encontrado.goles_en_contra}")
        print(f"- {COLOR['default']}Diferencia de goles: {COLOR['azul']}{equipo_encontrado.diferencia_goles}")
        print(f"- {COLOR['default']}Puntos: {COLOR['azul']}{equipo_encontrado.puntos}")
        print(f"- {COLOR['default']}Resultados:")
        
        for fecha, enfrentamientos in self.calendario.items():
            for partido in enfrentamientos:
                if equipo_encontrado.nombre in partido:
                    local, visitante = list(partido.keys())
                    marcador_local = partido[local]
                    marcador_visitante = partido[visitante]
                    if marcador_local is not None and marcador_visitante is not None:
                        if local == equipo_encontrado.nombre:
                            print(f"  Fecha {fecha}: {local} {COLOR['azul']}{marcador_local} - {marcador_visitante} {COLOR['default']}{visitante}")
                        else:
                            print(f"  Fecha {fecha}: {visitante} {COLOR['azul']}{marcador_visitante} - {marcador_local} {COLOR['default']}{local}")
                    else:
                        if local == equipo_encontrado.nombre:
                            print(f"  Fecha {fecha}: {local} - {visitante} {COLOR['azul']}(Partido no jugado){COLOR['default']}")
                        else:
                            print(f"  Fecha {fecha}: {visitante} - {local} {COLOR['azul']}(Partido no jugado){COLOR['default']}")  

    def terminar_torneo(self, terminar_torneo_anticipado = None):
        
        if terminar_torneo_anticipado:
            if self.fecha_actual < 3:
                print(f"{COLOR['rojo']}\nSe debe completar más de una fecha para poder terminar el torneo.{COLOR['default']}")
                return 

            partidos_fecha_actual = self.calendario[str(self.fecha_actual)]
            partidos_jugados = sum(1 for partido in partidos_fecha_actual if None not in partido.values())
            if 0 < partidos_jugados < len(partidos_fecha_actual):
                print(f"{COLOR['rojo']}\nNo se puede terminar el torneo anticipadamente porque no se han jugado todos los partidos de la fecha actual.{COLOR['default']}")
                return
            
        # Calcular ascensos y descensos
        tabla = sorted(self.equipos.values(), key=lambda x: (x.puntos, x.diferencia_goles, x.goles_a_favor), reverse=True)
        self.campeon = tabla[0].nombre
        self.equipos_ascendidos = [equipo.nombre for equipo in tabla[:3]]
        self.equipos_descendidos = [equipo.nombre for equipo in tabla[-3:]]
        self.torneo_terminado = True

        if terminar_torneo_anticipado:
            self.guardar_datos_json()
        
        self.mostrar_resultado_final_torneo()

    def mostrar_resultado_final_torneo(self):
        print(f"{COLOR['azul']}\n¡El torneo ha terminado, se han completado todas las fechas!{COLOR['default']}")
        print(f"{COLOR['amarillo']}\nCampeón \U0001F3C6: {self.campeon}{COLOR['default']}")
        
        # Mostrar equipos ascendidos
        print(f"{COLOR['verde']}\nAscenso \N{UPWARDS ARROW}{COLOR['default']}")
        for equipo in self.equipos_ascendidos:
            print(f"{COLOR['verde']}- {COLOR['default']}{equipo}")

        # Mostrar equipos descendidos
        print(f"{COLOR['rojo']}\nDescenso \N{DOWNWARDS ARROW}{COLOR['default']}")
        for equipo in self.equipos_descendidos:
            print(f"{COLOR['rojo']}- {COLOR['default']}{equipo}")
        
        print(f"{COLOR['azul']} \nPuede comenzar un nuevo torneo eligiendo la opción en el menú.{COLOR['default']}")

    def cargar_datos_json(self):
        try:
            with open('data/torneo.json', 'r') as f:
                data = json.load(f)
                self.equipos = {nombre: Equipo.from_dict(info) for nombre, info in data["equipos"].items()}
                self.calendario = data.get("calendario", {})
                self.fechas_terminadas = data.get("fechas_terminadas", [])
                self.fecha_actual = data.get("fecha_actual", 1)
                self.torneo_terminado = data.get("torneo_terminado", False)
                self.campeon = data.get("campeon", None)
                self.equipos_ascendidos = data.get("equipos_ascendidos", [])
                self.equipos_descendidos = data.get("equipos_descendidos", [])
        
        except FileNotFoundError:
            self.equipos = {nombre: Equipo(nombre) for nombre in self.EQUIPOS_PREDETERMINADOS}
            self.calendario = {}
            self.fechas_terminadas = []
            self.fecha_actual = 1
            self.torneo_terminado = False
            self.campeon = None
            self.equipos_ascendidos = []
            self.equipos_descendidos = []
            self.guardar_datos_json()

    def guardar_datos_json(self):
        data = {
            "equipos": {equipo.nombre: equipo.to_dict() for equipo in self.equipos.values()},
            "calendario": self.calendario,
            "fechas_terminadas": self.fechas_terminadas,
            "fecha_actual": self.fecha_actual,
            "torneo_terminado": self.torneo_terminado,
            "campeon": self.campeon,
            "equipos_ascendidos": self.equipos_ascendidos,
            "equipos_descendidos": self.equipos_descendidos
        }
        
        if not os.path.exists('data'):
            os.makedirs('data')
        
        with open('data/torneo.json', 'w') as f:
            json.dump(data, f, indent=4)
