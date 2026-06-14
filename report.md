# **GESTOR DE PARTIDOS DEL FC BARCELONA**



La aplicación se encarga de gestionar la disponibilidad de los jugadores del FC Barcelona de cara a los partidos de la temporada 25/26, es decir, desde la fecha actual

hasta el 31 de julio de 2026. Se eligió esta temática debido a la cada vez mayor cantidad de lesiones en el fútbol profesional. Esto es un hecho muy preocupante, pues no solo se ve afectada la  salud e integridad de los jugadores, sino que la logística y planificación de los equipos se ve perjudicada, resultando muchas veces en una reducción de calidad del equipo en determinado momento de la temporada, en muchas ocasiones, en el momento más importante. Este programa es útil para calcular si es posible que un jugador esté de regreso para determinado partido, y en caso de que sí, se asigne a dicho partido. Elegí el FC Barcelona porque es mi equipo favorito y sobre el que más conocimiento tengo.

En el programa se toma a los jugadores como recursos (activos) y a los partidos como eventos. La funcionalidad elemental es asignar jugadores a cada partido. Los eventos tienen como restricción que no pueden ocurrir dos partidos en un mismo día ni tampoco se pueden planificar partidos para fechas anteriores o que se encuentren fuera de la temporada 25/26. En cuanto a los jugadores, un jugador lesionado no puede estar disponible para un partido, y resulta evidente aclarar que tampoco puede estar convocado.



#### **El programa consta de 3 archivos:**



* ###### **doctor.py:**

    Desde este programa, se podrá trabajar con los jugadores lesionados. Deberán especificarse el jugador, el tipo de lesión y las semanas de baja. Dentro de dicho

    programa, existen operaciones especificadas que permitirán realizar un uso eficiente del mismo. Además, tiene funcionalidades añadidas que permiten gestionar la

&#x20;   información y detalles a voluntad del usuario. Además de añadir un jugador a la lista de lesionados especificando sus detalles, existen las opciones de eliminarlos

&#x20;   de dicha lista; solicitar la lista de lesionados; y modificar los detalles sobre cada lesionado. Al finalizar la sesión, se debe seleccionar la opción de "Guardar

&#x20;   y salir" para registrar los nuevos datos.



* ###### **main.py:**

    Desde este programa, se planificarán todos los eventos, los cuales serán partidos de fútbol. Estos pueden ser tanto añadidos como borrados en cualquier momento.

    Cada partido tiene detalles que pueden ser solicitados, tales como Rival, Fecha, Jugadores disponibles, Jugadores convocados, Cantidad de Convocados y Estado.

    Se puede seleccionar cualquier equipo como rival siempre y cuando no sea el propio "FC Barcelona". Por supuesto, podrían existir equipos que se inspiren del

&#x20;   nombre, o incluso lo copien como ejemplo: "Barcelona" o "Barcelona SC".

    En cuanto a la fecha, debe ser seleccionada en un rango entre la fecha actual y el 31 de julio de 2026. Además, solo puede existir un partido por fecha. Cualquier

    conflicto será informado en caso de ocurrir, notificando al usuario su error y pidiéndole una nueva entrada que esté dentro de las condiciones establecidas..

    Los convocados son la parte más importante del partido, pues son los activos que permitirán la realización del mismo. Existen dos posibles estados para un partido

    dependiendo de la cantidad de jugadores convocados y son denotados como:

    - **"OK"**: El partido tiene **18** jugadores convocados y se puede jugar.

    -  **"!"**: El partido tiene **menos de 18** jugadores convocados, y según la normativa de la UEFA, no se puede realizar, siendo tomado como **derrota por 3 - 0**.

    Ningún partido puede tener más de 18 jugadores convocados. Solo pueden ser convocados los jugadores que no estén lesionados y los lesionados que tengan su regreso

    estimado para una fecha menor o igual que la del partido.



    En el programa existe la opción de hacer modificaciones a cada partido guardado. Se pueden modificar el **Rival**, la **Fecha** y la **lista de Convocados**. Manteniendo las

    restricciones en cada uno. Como detalle importante, al cambiar la fecha, **pueden ocurrir cambios en la lista de Convocados y/o Disponibles**.



* ###### **datos.JSON:**

    En este archivo se almacena toda la información con la que trabaja la aplicación. El plantel, los jugadores disponibles y lesionados, y los partidos se almacenan

    aquí. Es el registro fundamental sobre el cual actúa el programa. Al finalizar la sesión en cualquiera de los programas anteriores, es necesario seleccionar la

&#x20;   opción "Guardar y Salir" para que los nuevos datos sean registrados.





&#x20; Durante el desarrollo del programa se me hizo necesario profundizar en el estudio de Python, utilizando tanto medios proporcionados por la carrera (El Curso Intensivo de Python) como externos (Canales de Youtube sobre el uso de la librería datetime). Desde un inicio opté por priorizar la realización de un programa que funcionara, y a partir de ahí, irlo perfeccionando mediante la resolución de posibles bugs, el añadir más funcionalidades y detalles, y Easter Eggs.

&#x20; Se me presentaron diversas dificultades que con el tiempo fui aprendiendo a solucionar.

&#x20; Una de ellas, fue el uso de la ruta relativa del archivo **datos.JSON**, funcionaba en el directorio sobre el que trabajé el proyecto, sin embargo al moverlo o exportarlo, el programa daba **FileNotFoundError**, lo cual resultaba fatal pues además de un error de compilación, el programa se quedaba sin datos sobre los que trabajar. Fue la primera dificultad en presentarse y la última en solucionarse. Irónicamente la más sencilla, pues ya sé especificar correctamente las rutas de archivos en Python.

&#x20; Otra que se presentó fue un bug que tras determinados pasos, podía ocurrir y resultar en una incoherencia total en el manejo de datos. Pues al crear un partido en **main.py**, añadir jugadores a la lista de convocados, guardar los datos y salir, iniciar una sesión en **doctor.py**, añadir uno de esos jugadores a la lista de lesionados y guardar los datos, ocurría que al regresar a la información del partido, ese jugador aún estaba en la lista de convocados, y el programa informaba que el partido estaba correcto, lo cual viola la restricción de que los jugadores lesionados no están disponibles para ningún partido en su tiempo de lesión. Luego de horas de prueba y error, errores de compilación y varios bloques de código, conseguí solucionar este error y añadir detalles como que los jugadores lesionados estén disponibles o no en dependencia de si hay modificaciones en la fecha de algún partido.

&#x20; También aprendí el uso y modificación de la librería datetime. En un inicio me trajo complicaciones el manejo de los datos de tipo date, pues estas no se pueden guardar en un JSON con su formato original. Esto suponía un problema enorme, pues provocaba un error de compilación y no solo eso, a la hora de guardar los datos en el JSON, cuando llegaba a este tipo de datos, daba el error y el **datos.JSON** quedaba completamente inutilizable pues al interrumpirse el guardado de datos, quedaba incompleto y los otros dos programas también daban error de compilación al intentar leer los datos. Para solucionar esto, creé una función que se encargaba, ya al final del programa, de convertir todas las fechas guardadas en variable date, a strings. Esto a ojos del usuario no cambia nada pero computacionalmente lo cambia todo, pues a partir de ese momento ya se podían guardar las fechas en el JSON. Por supuesto, como viceversa, también tuve que implementar una función que transformara esas strings guardadas, a dates, para que el programa funcionara correctamente y pudiera hacer todos los cálculos y comparaciones de fechas. Fue algo que no llevó muchas líneas de código pero sí mucho pensar y determinación para resolver el problema.

&#x20; Otro error que ocurría era a la hora de determinados jugadores lesionados estuvieran disponible para determinada fecha. La idea consistía en que si un partido ocurre en una fecha para la cual ya debería estar de regreso, entonces ese jugador estaría disponible para el partido. El error que ocurría era de datos incorrectos, es decir, jugadores que no aparecían en la lista de disponibles, o aparecían doble, lo cual evidentemente resulta en una inconsistencia. Para resolverlo creé varios bloques de bucles y condicionales que se encargarían de revisar cada aspecto y que todo estuviera en orden. También usé variables para guardar valores y booleanos que según su valor desencadenarían un reinicio de la operación en caso de ser False, y una continuación en caso de ser True. Finalmente logré implementarlo y tras varios testeos no encontré errores ni inconsistencias.



&#x20; 

&#x20; Para entender el funcionamiento del programa no es necesario tener un gran conocimiento sobre fútbol ni nada parecido, simplemente es entender la disponibilidad de los activos de cara a los eventos que se planifiquen. Para esto el programa se divide en dos archivos descritos anteriormente. La idea de uso es que el usuario opere desde **doctor.py** la disponibilidad de dichos activos. Por ejemplo, supongamos que Lamine Yamal tiene una molestia muscular que le impide estar en el terreno de juego durante 2 semanas. El usuario debe seleccionar la opción de "Añadir lesionado", ver la lista de jugadores y seleccionar el dorsal, en este caso el 10. A continuación el usuario debe especificar en Tipo de lesión, "Molestia muscular". Y en semanas de baja, el usuario debe digitar 2. Luego de esto, el programa calculará su fecha de regreso estimada, sumándole a la fecha actual esas 2 semanas de baja. Una vez añadida toda la información, el usuario debe guardar los datos para que todo el programa general sepa que Lamine Yamal va a estar lesionado durante 2 semanas.

&#x20; A continuación, supongamos que en 10 días el FC Barcelona juega contra su clásico rival, el Real Madrid. El usuario deberá abrir **main.py** y planificar dicho evento. Debe seleccionar "Añadir partido", especificar en rival que es el Real Madrid, debe seleccionar la fecha, y después de que el programa verifique que es válida, se dispondrá la lista de jugadores disponibles para que el usuario seleccione los 18 convocados. Revisando esta lista, se mostrará a todos los jugadores de la plantilla menos Lamine Yamal, el cual en este ejemplo es el único lesionado. Luego de seleccionar a los 18 y guardar los datos, LaLiga notifica que el Clásico será pospuesto, y en lugar de 10 días, ahora será en 20. El usuario debe modificar la información con los nuevos datos, y al modificar la fecha, el programa modifica que Lamine Yamal ya está disponible para el partido, por lo que se puede desconvocar a un jugador y convocar a Lamine Yamal si así lo desea el usuario. Por supuesto, es un regreso estimado, no es algo que sea totalmente seguro, pero si todo se mantiene bien, se debería dar el regreso, y si existe una recaída, entonces la ficha de lesionado de Lamine Yamal debe ser modificada por el usuario con la nueva cantidad de semanas de baja.

&#x20; Que todos los jugadores estén lesionados es un escenario casi totalmente improbable, pero en caso de que se diera, el FC Barcelona tendría que subir a canteranos al primer equipo o fichar agentes libres, es decir, inscribir nuevos jugadores los cuales no están en el plantel original, siendo esto una tarea destinada a la dirección deportiva del club y no al usuario.





&#x20; Con el proyecto finalizado, la Programación ahora me resulta un mundo aún más fascinante. Me impresiona la idea de que tengas que lograr un equilibrio entre cada línea de código, función y detalle que se te ocurra, pues un solo error puede provocar un efecto dominó que es capaz de que el programa termine haciendo algo totalmente distinto para lo que fue pensado inicialmente. También me gusta la idea de que con unas líneas de código bien estructuradas, muchas líneas de código, puedas hacer prácticamente cualquier cosa. Es como ser Dios pero en un entorno controlado únicamente por ti mismo, es un mundo que me apasiona y lo que más me gusta de la carrera. Obviamente recién estoy comenzando y me faltan muchísimas cosas por aprender, pero siento que este proyecto que aunque no es algo grande ni mucho menos profesional, es un buen comienzo y un paso en la dirección correcta. Espero hacer más proyectos como este e incluso mejores en el futuro, al igual que aprender a trabajar en equipo, pues es algo fundamental en este mundo.

