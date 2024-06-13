from torneo import Torneo
from colores import COLOR
def menu_principal():
    print()
    print(f"{COLOR['verde']}*****************************************************************")
    print(f"**    Bienvenido al Sistema de Gestión de Torneos de Fútbol    **")
    print(f"*****************************************************************")
    print(f"**   1.  Iniciar nuevo torneo                                  **")
    print(f"**   2.  Ver calendario de enfrentamientos                     **")
    print(f"**   3.  Ingresar resultado de un partido                      **")
    print(f"**   4.  Simular partidos faltantes por fecha                  **")
    print(f"**   5.  Ver resultados de los partidos jugados                **")
    print(f"**   6.  Ver tabla general del torneo                          **")
    print(f"**   7.  Ver estadísticas gerales del torneo                   **")
    print(f"**   8.  Ver estadísticas por equipo                           **")
    print(f"**   9.  Terminar torneo anticipadamente                       **")
    print(f"**   10. Ver resultado final del torneo                        **")
    print(f"**   0.  Salir                                                 **")
    print(f"*****************************************************************{COLOR['default']}")
        
def main():
    torneo = Torneo()

    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            torneo.iniciar_nuevo_torneo()

        elif opcion == "2":
            if not torneo.calendario:
                print(f"{COLOR['rojo']}\nNo se ha iniciado un torneo, puede hacerlo en la opcion 1 del menú.{COLOR['default']}")
                continue
            torneo.mostrar_calendario()
        
        elif opcion == "3":
            try:
                if not torneo.calendario:
                    print(f"{COLOR['rojo']}\nNo se ha iniciado un torneo, puede hacerlo en la opcion 1 del menú.{COLOR['default']}")
                    continue

                if torneo.torneo_terminado:
                    print(f"{COLOR['rojo']}\nEl torneo ya ha sido terminado, puedes iniciar uno nuevo.{COLOR['default']}")
                    continue

                fecha = input("\nIngrese el número de la fecha: ")
                if not fecha:
                    print(f"{COLOR['rojo']}\nLa fecha {fecha} no puede estar vacia.{COLOR['default']}")
                    continue
                
                if fecha not in torneo.calendario:
                    print(f"{COLOR['rojo']}\nLa fecha {fecha} no se encuentra en el calendario{COLOR['default']}")
                    continue
                
                # Validamos que la fecha anterior ya terminó
                if not torneo.validar_fecha_anterior_terminada(fecha):
                    print(f"{COLOR['rojo']}No se pueden ingresar resultados para esta fecha hasta que se jueguen todos los partidos de las fecha anteriores.{COLOR['default']}")
                    continue
                
                torneo.mostrar_calendario(fecha)
                
                partido = input("\nIngrese el número del partido: ")
                
                if not partido.strip():
                    print(f"{COLOR['rojo']}\nNo puede estar vacio.{COLOR['default']}")
                    continue
                
                try:
                    partido = int(partido)
                except ValueError:
                    print(f"{COLOR['rojo']}\nDebe ingresar un número entero válido.{COLOR['default']}")
                    continue
                
                if partido < 1 or partido > len(torneo.calendario[fecha]):
                    print(f"{COLOR['rojo']}Número de partido no válido. Por favor, intente nuevamente.{COLOR['default']}")
                    continue
                
                equipo_local, equipo_visitante = torneo.calendario[fecha][partido - 1]
                
                goles_local = input(f"Goles del equipo {equipo_local}: ")
                
                if not goles_local.strip():
                    print(f"{COLOR['rojo']}\nNo puede estar vacío.{COLOR['default']}")
                    continue
                
                try:
                    goles_local = int(goles_local)
                except ValueError:
                    print(f"{COLOR['rojo']}\nDebe ingresar un número entero válido.{COLOR['default']}")
                
                if goles_local < 0:
                    print(f"{COLOR['rojo']}\nEl número no puede ser neagtivo.{COLOR['default']}")
                    continue

                goles_visitante = input(f"Goles del equipo {equipo_visitante}: ")
                
                if not goles_visitante.strip():
                    print(f"{COLOR['rojo']}\nNo puede estar vacio.{COLOR['default']}")
                    continue
                
                try:
                    goles_visitante = int(goles_visitante)
                except ValueError:
                    print(f"{COLOR['rojo']}\nDebe ingresar un número entero válido.{COLOR['default']}")
                    continue
                
                if goles_visitante < 0:
                    print(f"{COLOR['rojo']}\nEl número no puede ser neagtivo.{COLOR['default']}")
                    continue

                torneo.ingresar_resultado(fecha,equipo_local, goles_local, equipo_visitante, goles_visitante)
            
            except ValueError:
                print("algooo")
                pass
        
        elif opcion == "4":
            if not torneo.calendario:
                print(f"{COLOR['rojo']}\nNo se ha iniciado un torneo, puede hacerlo en la opcion 1 del menú.{COLOR['default']}")
                continue
            if torneo.torneo_terminado:
                print(f"{COLOR['rojo']}\nEl torneo ya ha sido terminado, puedes iniciar uno nuevo.{COLOR['default']}")
                continue
            fecha = input("\nIngrese el número de la fecha: ")
            torneo.simular_partidos_faltantes_por_fecha(fecha)
        
        elif opcion == "5":
            if not torneo.calendario:
                print(f"{COLOR['rojo']}\nNo se ha iniciado un torneo, puede hacerlo en la opcion 1 del menú.{COLOR['default']}")
                continue
            torneo.mostrar_resultados()
        
        elif opcion == "6":
            if not torneo.calendario:
                print(f"{COLOR['rojo']}\nNo se ha iniciado un torneo, puede hacerlo en la opcion 1 del menú.{COLOR['default']}")
                continue
            torneo.mostrar_tabla_torneo()
        
        elif opcion == "7":
            if not torneo.calendario:
                print(f"{COLOR['rojo']}\nNo se ha iniciado un torneo, puede hacerlo en la opcion 1 del menú.{COLOR['default']}")
                continue
            torneo.mostrar_estadisticas_generales()
        
        elif opcion == "8":
            if not torneo.calendario:
                print(f"{COLOR['rojo']}\nNo se ha iniciado un torneo, puede hacerlo en la opcion 1 del menú.{COLOR['default']}")
                continue
            
            nombre_equipo = input("\nIngrese el nombre del equipo: ")
            if not nombre_equipo:
                print(f"{COLOR['rojo']}\nNo puede estar vacio.{COLOR['default']}")
                continue
            
            torneo.mostrar_estadisticas_por_equipo(nombre_equipo)
        
        elif opcion == "9":
            if not torneo.calendario:
                print(f"{COLOR['rojo']}\nNo se ha iniciado un torneo, puede hacerlo en la opcion 1 del menú.{COLOR['default']}")
                continue
            torneo.terminar_torneo(True)
        
        elif opcion == "10":
            if not torneo.calendario:
                print(f"{COLOR['rojo']}\nNo se ha iniciado un torneo, puede hacerlo en la opcion 1 del menú.{COLOR['default']}")
                continue
            if not torneo.torneo_terminado:
                print(f"{COLOR['rojo']}\nEl torneo no ha terminado, vuelve cuando haya finalizado para que veas el resultado final.{COLOR['default']}")
                continue
            torneo.mostrar_resultado_final_torneo()
        
        elif opcion == "0":
            print("Gracias por utilizar el Sistema de Gestión de Torneos de Fútbol")
            break
        
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()