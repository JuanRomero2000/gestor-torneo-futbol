class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.partidos_jugados = 0
        self.partidos_ganados = 0
        self.partidos_empatados = 0
        self.partidos_perdidos = 0
        self.goles_a_favor = 0
        self.goles_en_contra = 0
        self.puntos = 0
    
    @property
    def diferencia_goles(self):
        return self.goles_a_favor - self.goles_en_contra
    
    def actualizar_estadisticas(self, goles_a_favor, goles_en_contra):
        self.partidos_jugados += 1
        self.goles_a_favor += goles_a_favor
        self.goles_en_contra += goles_en_contra
        
        if goles_a_favor > goles_en_contra:
            self.partidos_ganados += 1
            self.puntos += 3
        elif goles_a_favor == goles_en_contra:
            self.partidos_empatados += 1
            self.puntos += 1
        else:
            self.partidos_perdidos += 1
    
    # Función para revertir las estadisticas anteriores de un partido ya jugado
    def revertir_estadisticas(self, goles_a_favor, goles_en_contra):
        self.partidos_jugados -= 1
        self.goles_a_favor -= goles_a_favor
        self.goles_en_contra -= goles_en_contra

        if goles_a_favor > goles_en_contra:
            print("ganado")
            self.partidos_ganados -= 1
            self.puntos -= 3
        elif goles_a_favor == goles_en_contra:
            self.partidos_empatados -= 1
            self.puntos -= 1
        else:
            self.partidos_perdidos -= 1
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "partidos_jugados": self.partidos_jugados,
            "partidos_ganados": self.partidos_ganados,
            "partidos_empatados": self.partidos_empatados,
            "partidos_perdidos": self.partidos_perdidos,
            "goles_a_favor": self.goles_a_favor,
            "goles_en_contra": self.goles_en_contra,
            "diferencia_goles": self.diferencia_goles,
            "puntos": self.puntos
        }

    @staticmethod
    def from_dict(data):
        equipo = Equipo(data['nombre'])  # Corrección de la clave 'name' a 'nombre'
        equipo.partidos_jugados = data['partidos_jugados']
        equipo.partidos_ganados = data['partidos_ganados']
        equipo.partidos_empatados = data['partidos_empatados']
        equipo.partidos_perdidos = data['partidos_perdidos']
        equipo.goles_a_favor = data['goles_a_favor']
        equipo.goles_en_contra = data['goles_en_contra']
        equipo.puntos = data['puntos']
        return equipo