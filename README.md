
----------Proyecto Launcher de Utilidades para Juegos de Rol----------
Descripción general.-
Aplicación en Python con interfaz gráfica para lanzar herramientas de rol, tablas y PDFs.

Este proyecto contiene un launcher general en Tkinter para abrir distintas utilidades de rol (conversor, generador, tablas, etc.) y una segunda aplicación dedicada a mostrar y abrir PDFs de tablas.
Está diseñado para ser modular, portable y fácil de ampliar.

Características principales.-
 -- Launcher principal
    - Intefaz gráfica en Tkinter
    - Carga asíncrona de la imagen de fondo (UI más fluida)
    - Lazamiento de mini-aplicaciones o scripts externos
    - Estilo visual moderno
    - Arquitectura organizada en módulos

 -- Selector de tablas en PDF
    - Carga de fondos con PIL (Pillow)
    - Botones generados dinámicamente
    - Apertura de PDFs directamente desde el visor predeterminado

 -- Conversor para viajes
    - Carga de fondos con PIL (Pillow)
    - Botones generados dinámicamente
    - Muestra el tiempo necesario que requeriría el viaje utilizando variables como pies, vehículo y velocidad
    - Adaptado para el VTT del sistema D&D
    - Posibilidad de ser utilizado en otros VTT

 -- Generador precios aleatorios
    - Carga de fondos con PIL (Pillow)
    - Botones generados dinámicamente
    - Generación de precios aleatorios para cada artículo
    - Listado de seguimiento de los artículos con posibilidad de añadir o quitar

 -- Mecánica de control y gestión de reputación
    - Guardado y carga de datos a través de archivos JSON
    - Gráfica dinámica actualizada a tiempo real
    - Aplica puntos de "reputación" individuales y globales
    - Diseño sencillo pero eficaz

 -- Buenas prácticas implementadas
    - Sin rutas absolutas
    - Uso de os.path.join para compatibilidad entre sistemas
    - Código limpio y bien estructurado
    - Repositorio con buena presentación profesional
