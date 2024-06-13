# Sistema de Gestión de Torneos de Fútbol

Este proyecto implementa un sistema de gestión de torneos de fútbol utilizando Python. Permite la organización de equipos, calendario de partidos, ingreso de resultados, simulación de partidos, estadísticas generales del torneo, etc.

## Funcionalidades

**1.  Iniciar nuevo torneo**: Permite dar inicio a un nuevo torneo y crear el json con la estrucutra necesaria.
**2.  Ver calendario de enfrentamientos**: Muestra el calendario completo de todos los partidos a disputar por cada fecha.
**3.  Ingresar resultado de un partido**: Permite ingresar los resultados de los partidos jugados.
**4.  Simular partidos faltantes por fecha**: Permite simular los resultados de los partidos que aún no se han jugado de una fecha especificada.
**5.  Ver resultados de los partidos jugados**: Muestra los resultados de los partidos jugados hasta la fecha actual.
**6.  Ver tabla general del torneo**: Muestra la tabla de posiciones con estadísticas de los equipos.
**7.  Ver estadísticas generales del torneo**: Muestra las estadísticas generales del torneo como la cantidad de partidos jugados, el total de goles, los equipos con mas vistorias, etc.
**8.  Ver estadísticas por equipo**: Muestra las estadísticas específicas de un equipo dado.
**9.  Terminar torneo anticipadamente**: Permite finalizar el torneo antes de que se jueguen todos los partidos, siempre y cuando se hayan jugado al menos 2 fechas y no haya una fecha iniciada con partidos pendientes.
**10. Ver resultado final del torneo**: Muestra el resultado del torneo, una vez finalizado.
**0. Salir**: Finaliza la ejecución del programa.

## Requisitos de Instalación

Para ejecutar este proyecto, es necesario tener instalado Python (versión 3.X.X)

## Uso

1. **Clonar el repositorio:**

git clone https://github.com/tu_usuario/tu_proyecto.git
cd tu_proyecto

2. **Ejecutar el programa:**

python main.py

3. **Seleccionar una opción del menú principal:**

- Selecciona una opción ingresando el número correspondiente y presionando Enter.

4. **Seguir las instrucciones en pantalla:**

- Sigue las instrucciones para interactuar con las diferentes funcionalidades del sistema.

# Consideraciones extras

- El torneo se inicia con un total de 20 equipos los cuales se encuentran por defecto y pueden ser mofificados en el archivo torneo.py
- Se establecieron 6 fechas de forma prederteminada para no hacer demasiado extenso y agobiante el uso del programa pero este numero de fechas tambien se puede modificar en la constante NUMERO_FECHAS en el archivo torneo.py

## Créditos

Este proyecto fue desarrollado por [Juan Romero](https://github.com/JuanRomero2000).