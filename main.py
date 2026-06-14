# Vision del Entrenador

from datetime import date, timedelta
import json

def validar_fecha(string):
    #Esta funcion transforma las fechas almacenadas en string en el JSON, en fechas de tipo date.
    
    dia = int(string[0] + string[1])
    mes = int(string[3] + string[4])
    año = int(string[6:])
    nueva_fecha = date(año, mes, dia)
    return nueva_fecha


# Importa todos los datos del JSON.
with open("./datos.json") as f: 
    data = json.load(f)


# Este bloque de código se encarga de transformar todas las strings de fechas, a dates.
for lesionado in data['lesionados']:
    lesionado['regreso_estimado'] = validar_fecha(lesionado['regreso_estimado'])
for partido in data['partidos']:
    partido['fecha'] = validar_fecha(partido['fecha'])


# Se crean 2 listas con los jugadores que no están lesionados y los partidos almacenados
# en el JSON.
plantel = data['plantel']
disponibles = data['disponibles']
lesionados = data['lesionados']
partidos = data['partidos']

# Mensaje de bienvenida.
print("Bienvenido, Entrenador. Usted será el encargado de gestionar los partidos de nuestro club.\n\n\n")
bandera = 0


# El siguiente bloque elimina los jugadores que no estarán disponibles para partidos a los que
# habían sido asignados:
cambios_en_disponibilidad = False
for partido in partidos:
    for convocado in partido['convocados']:
        for lesionado in data['lesionados']:
            if convocado['dorsal'] == lesionado['dorsal']:
                if lesionado['regreso_estimado'] > partido['fecha']:
                    partido['convocados'].remove(convocado)
                    partido['cantidad_convocados'] = len(partido['convocados'])
                    cambios_en_disponibilidad = True
    for disponible in partido['disponibles']:
        for lesionado in data['lesionados']:
            if disponible['dorsal'] == lesionado['dorsal']:
                if lesionado['regreso_estimado'] > partido['fecha']:
                    partido['disponibles'].remove(disponible)
                    cambios_en_disponibilidad = True
# Este bloque se encarga de añadir los que fueron eliminados de la lista de lesionados a la de disponibles.
for disponible in disponibles:
    nuevo_disponible = {'dorsal': disponible['dorsal'], 'nombre' : disponible['nombre']}
    for partido in partidos:
        if not(nuevo_disponible in partido['convocados']) and not(nuevo_disponible in partido['disponibles']):
            partido['disponibles'].append(nuevo_disponible)
            cambios_en_disponibilidad = True
# Se encarga de avisar si hubo cambios en algun partido debido a los lesionados.
if cambios_en_disponibilidad:
    print("\n\n\nADVERTENCIA: Hubo cambios en la disponibilidad de ciertos partidos debido a cambios en la lista de lesionados.")
    print("Se recomienda revisar los detalles de todos los partidos.\n\n\n")


# Bucle principal:
while (bandera != 5):

    print("Operaciones disponibles: \n\t"
      "1. Solicitar lista de partidos.\n\t2. Añadir partido.\n\t" 
      "3. Eliminar partido.\n\t4. Modificar detalles de partido.\n\t"
      "5. Guardar y Salir.")
    
    # Evita que el programa se detenga al detectar una entrada inválida.
    try:
        bandera = int(input("Introduzca el número de la operación deseada: "))
    except ValueError:
        print("Entrada Inválida. Debe digitar un número entre 1 y 5.")
        continue
    
    # Evita que se introduzca una operación no definida.
    if (bandera <= 0) or (bandera > 5):
        print("Entrada Inválida. Debe digitar un número entre 1 y 5.")
        continue
    
    # Operación 1: Solicitar lista de partidos.
    if (bandera == 1):

        # Avisa si no hay partidos.
        if not(partidos):
            print("\nNo hay partidos establecidos actualmente.")
        # Imprime la lista de partidos en caso de tener elementos.    
        else:
            print("LISTA DE PARTIDOS:\n\n\n")
            for partido in partidos:
                print(f"ID: {partido['id']} || Rival: {partido['rival']} ({partido['fecha']}) || Estado: {partido['estado']}")
            
            # Este bloque permite al usuario pedir detalles sobre algún partido
            respuesta = ""    
            respuesta_correcta = False
            while not(respuesta_correcta):
                respuesta = input("\n¿Desea obtener detalles de algún partido? (Sí/No)\n ---> ").lower()
                if (respuesta.strip() == "si") or (respuesta.strip() == "sí"):   
                    id_partido = input("Digite la ID del partido del cual desea obtener detalles: ")
                    for partido in partidos:
                        if id_partido == partido['id']:
                            print(f"Detalles del partido ID: ({id_partido}):\n")
                            print(f"Rival: {partido['rival']}")
                            print(f"Fecha: {partido['fecha']}")
                            print(f"Estado: {partido['estado']}")
                            print(f"\nConvocados({partido['cantidad_convocados']}): \n")
                            for convocado in partido['convocados']:
                                print(f"|{convocado['dorsal']} - {convocado['nombre']}|")
                            print(f"\nDisponibles: \n")
                            for disponible in partido['disponibles']:
                                print(f"|{disponible['dorsal']} - {disponible['nombre']}")
                            respuesta_correcta = True
                    if not(respuesta_correcta):
                        print(f"Error. No existe ningún partido con la ID ({id_partido}).")
                        continue
                elif(respuesta.strip() == "no"):
                    respuesta_correcta = True
                # Verifica que solo se pueda responder (Sí) o (No).
                else:
                    print("Entrada Inválida. Debe digitar (Sí) o (No).")
                    continue
        
    # Operación 2: Añadir partido.
    if (bandera == 2):
        
        # Crea la variable que almacenará los datos del nuevo partido.
        nuevo_partido = {'id': None, 'rival': None, 'fecha': None, 'cantidad_convocados' : None, 'convocados': [], 'disponibles': [], 'estado': None}
        
        # Permite escribir el nuevo nombre y evita que se ponga al FC Barcelona como rival.
        nombre_correcto = False
        while not(nombre_correcto):
            nuevo_partido['rival'] = input("Escriba el nombre del equipo rival: ")
            if nuevo_partido['rival'].strip() == "FC Barcelona":
                print("Debes coleccionar muchos cromosomas, pero no podemos jugar contra nosotros mismos.")
                continue
            else:
                nombre_correcto = True
                print("Nombre guardado con éxito.")
                break

        # Este bloque se encarga de crear la fecha del nuevo partido.
        print("\nA continuación, introduzca la fecha en el formato (Día/Mes). Al finalizar se registrará como (Año-Mes-Día)") 
        la_fecha_tiene_sentido = False
        while not(la_fecha_tiene_sentido):
            repetir = False
            
            # Permite escribir la fecha y evita que se ponga algún valor que no sea numérico
            try:
                dia = int(input("Digite el número de día: "))
                mes = int(input("Digite el número de mes: "))
            except ValueError:
                print("Entrada Inválida. Debe digitar números.")
                continue
            
            # Verifica que la fecha introducida sea válida
            try:
                nuevo_partido["fecha"] = date(2026, mes, dia)
            except ValueError:
                print(f"Entrada Inválida. La fecha ({dia}/{mes}) no existe.")
                continue
            
            # Verifica que no exista otro partido en la misma fecha.
            for partido in partidos:
                if nuevo_partido['fecha'] == partido['fecha']:
                    print(f"Fecha inválida. Ya existe un partido contra ({partido['rival']}) en esta misma fecha.")
                    repetir = True
                    break
            if repetir:
                continue
            
            # Verifica que la fecha esté en el rango del resto de la temporada 25/26.
            if nuevo_partido["fecha"] < date.today():
                print("Error. Usted ha introducido una fecha que ya pasó.")
                continue
            elif nuevo_partido['fecha'] >= date(2026, 8, 1):
                print("Entrada Inválida. Usted ha introducido una fecha que corresponde a la temporada 26/27.")
                continue
            else:
                la_fecha_tiene_sentido = True
            
            # Guarda la fecha y asigna una ID única al partido.
            nuevo_partido['id'] = nuevo_partido['fecha'].strftime("%Y%m%d") 
            print(f"\nDatos correctos. Usted ha seleccionado el {nuevo_partido['fecha']} como fecha del partido. (ID: {nuevo_partido['id']})")
        
        print("\nA continuación, se le asignará la lista de jugadores disponibles para convocar.")
        
        # Añade los jugadores que no están lesionados a la lista de disponibles.
        disponibles_para_jugar = []
        for jugador in disponibles:            
            informacion_jugador = {'dorsal': None, 'nombre': None}
            informacion_jugador['dorsal'] = jugador['dorsal']
            informacion_jugador['nombre'] = jugador['nombre']
            disponibles_para_jugar.append(informacion_jugador)
            
        # Añade los lesionados que deberían estar de regreso para la fecha a la lista de disponibles.
        for lesionado in data['lesionados']:
            if lesionado['regreso_estimado'] <= nuevo_partido['fecha']:
                informacion_jugador = {'dorsal': None, 'nombre': None}
                informacion_jugador['dorsal'] = lesionado['dorsal']
                informacion_jugador['nombre'] = lesionado['nombre']
                disponibles_para_jugar.append(informacion_jugador)                   

        # Este bloque añade varias opciones referentes a la lista de convocados.            
        convocados = []
        los_convocados_tienen_sentido = False
        while not(los_convocados_tienen_sentido):
            operacion = None
            
            # Imprime la lista de jugadores disponibles para convocar.
            print("\n\nJugadores Disponibles:\n")
            for jugador in disponibles_para_jugar:
                print(f"\t{jugador['dorsal']} - {jugador['nombre']}")
           
            # Gestiona las operaciones con respecto a la lista de convocados.
            while (operacion != 4):
                print("\n\nDigite (1) para añadir un jugador a la lista de convocados.",
                  "\nDigite (2) para eliminar un jugador de la lista de convocados.",
                  "\nDigite (3) para solicitar la lista de convocados.",
                  "\nDigite (4) para guardar los datos.")
                
                # Verifica que se introduzca un número de operación válido.
                try:
                    operacion = int(input("---> "))
                except ValueError:
                    print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                    continue
                if not((operacion == 1) or (operacion == 2) or (operacion == 3) or (operacion == 4)):
                    print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                    continue
                
                # Operación 1: Añadir a la lista de convocados.
                if (operacion == 1):
                    print("Usted ha seleccionado la opción de añadir a la lista de Convocados.")
                    
                    # Verifica que aún haya capacidad para añadir convocados.
                    if len(convocados) == 18:
                        print("Sin embargo ya se ha alcanzado el máximo de convocados (18).")
                        continue
                    
                    # Imprime la lista de jugadores disponibles para el partido.
                    print("\n\nJUGADORES DISPONIBLES:\n")
                    if not(disponibles_para_jugar):
                        print("\tNo hay más jugadores disponibles para este partido.")
                        continue
                    else:
                        for jugador in disponibles_para_jugar:
                            print(f"\t{jugador['dorsal']} - {jugador['nombre']}")

                    # Añade al jugador seleccionado a la lista de convocados y deja de mostrarlo en la lista de disponibles.
                    la_convocatoria_tiene_sentido = False
                    while not(la_convocatoria_tiene_sentido):
                        try:
                            dorsal_seleccionado = int(input("Digite el dorsal del jugador que desea convocar: "))
                        except ValueError:
                            print("Entrada Inválida. Debe digitar un número")
                            continue
                        for jugador in disponibles_para_jugar:
                            if dorsal_seleccionado == jugador['dorsal']:
                                la_convocatoria_tiene_sentido = True
                                convocados.append(jugador)
                                disponibles_para_jugar.remove(jugador)
                                print(f"\n>>> {jugador['nombre']} ha sido añadido a la lista de convocados.")
                                break
                        if not(la_convocatoria_tiene_sentido):
                            el_jugador_existe = False
                            for jugador in plantel:
                                if dorsal_seleccionado == jugador['dorsal']:
                                    if jugador in nuevo_partido['convocados']:
                                        print(f"¡{jugador['nombre']}({jugador['dorsal']}) ya está convocado para este partido!")
                                    if not(jugador in nuevo_partido['disponibles']) and not(jugador in nuevo_partido['convocados']):
                                        print(f"{jugador['nombre']}({jugador['dorsal']}) no está en la lista de disponibles.")
                                    el_jugador_existe = True
                                    break
                            if not(el_jugador_existe):
                                print("Error. Ningún jugador usa ese dorsal.")
                            continue
                
                # Operación 2: Eliminar de la lista de convocados.
                if (operacion == 2):
                    print("Usted ha seleccionado la opción de eliminar jugador de la lista de convocados.")
                    
                    # Imprime la lista de convocados.
                    if not(convocados):
                        print("Sin embargo, actualmente no hay jugadores convocados.")
                        continue                    
                    print("\n\nLISTA DE CONVOCADOS:\n\n")
                    for jugador in convocados:
                        print(f"\t|{jugador['dorsal']} - {jugador['nombre']}|")

                    # Solicita el dorsal del jugador que se desea eliminar.
                    la_eliminacion_tiene_sentido = False
                    while not(la_eliminacion_tiene_sentido):
                        try:
                            dorsal_seleccionado = int(input("Digite el dorsal del jugador que desea eliminar de la lista de convocados: "))
                        except ValueError:
                            print("Entrada Inválida. Debe digitar un número.")
                            continue
                        
                        # Verifica que el jugador esté en la lista y lo elimina en caso de estar.
                        for jugador in convocados:
                            if dorsal_seleccionado == jugador['dorsal']:
                                la_eliminacion_tiene_sentido = True
                                disponibles_para_jugar.append(jugador)
                                convocados.remove(jugador)
                                print(f"\n >>> {jugador['nombre']} ha sido eliminado de la lista de convocados.")
                                break
                        if not(la_eliminacion_tiene_sentido):
                            print("El jugador seleccionado no está en la lista de convocados.")
                            continue
                
                # Operación 3: Solicitar lista de convocados.
                if (operacion == 3):
                    print("Usted ha solicitado la lista de convocados.")

                    # Imprime la lista de convocados.
                    if not(convocados):
                        print("Sin embargo, actualmente no hay jugadores convocados.")
                        continue
                    else:
                        print("\n\nLISTA DE CONVOCADOS:\n\n")
                        for jugador in convocados:
                            print(f"\t|{jugador['dorsal']} - {jugador['nombre']}|")

                # Operación 4: Guardar datos.
                if (operacion == 4):
                    repetir = False

                    # Este bloque lanza una advertencia en caso de que la lista de convocados no esté
                    # completa. Da opciones al usuario de seguir editando o guardarla de todas formas.
                    if (len(convocados) < 18):
                        print("¡ADVERTENCIA! La lista de convocados no está completa, si aún está incompleta el día del partido, se contará como derrota por 3 - 0.")
                        respuesta_correcta = False
                        while not(respuesta_correcta):
                            respuesta = input("¿Desea guardar los datos de todas formas? (Sí/No) ---> ").lower()
                            if (respuesta.strip() == "sí") or (respuesta.strip() == "si"):
                                respuesta_correcta = True
                                nuevo_partido["convocados"] = convocados
                                nuevo_partido['cantidad_convocados'] = len(convocados)
                                nuevo_partido['estado'] = "!"
                                print("Datos guardados.")
                            elif (respuesta.strip() == "no"):
                                respuesta_correcta = True
                                repetir = True
                            else:
                                print("Entrada Inválida. Debe responder (Sí) o (No).")
                                continue
                    if repetir:
                        continue
                    
                    # Guarda los datos.
                    if len(convocados) == 18:
                        nuevo_partido["convocados"] = convocados
                        nuevo_partido['cantidad_convocados'] = len(convocados)
                        nuevo_partido['estado'] = "OK"
                    
                    los_convocados_tienen_sentido = True
        # Se añade el nuevo partido a la lista de partidos.
        nuevo_partido['disponibles'] = disponibles_para_jugar
        partidos.append(nuevo_partido)          
    
    # Operación 3: Eliminar partidos.                          
    if (bandera == 3):
 
        # Verifica que existan partidos y los imprime.
        if not(partidos):
            print("Actualmente no hay partidos planificados.")
            continue        
        print("\n\n")
        for partido in partidos:
            print(f"ID: {partido['id']} || Rival: {partido['rival']} ({partido['fecha']}) || Estado: {partido['estado']}")
        
        # Este bloque se encarga de eliminar el partido cuya ID sea digitada.
        eliminacion_correcta = False
        while not(eliminacion_correcta):
            id_partido = input("Escriba la ID del partido que desea eliminar de la lista: ")
            for partido in partidos:
                if id_partido == partido['id']:
                    partidos.remove(partido)
                    print("Partido removido exitosamente.")
                    eliminacion_correcta = True
                    break
            if not(eliminacion_correcta):
                print("Error. Esa ID no coincide con la de ningún partido.")
                continue

    # Operación 4: Modificar partido.
    if (bandera == 4):

        # Verifica que existan partidos y los imprime.
        if not(partidos):
            print("Actualmente no hay partidos planificados.")
            continue        
        print("\n\n")
        for partido in partidos:
            print(f"ID: {partido['id']} || Rival: {partido['rival']} ({partido['fecha']}) || Convocados: {partido['cantidad_convocados']} || Estado: {partido['estado']}")
        
        # Este bloque se encarga de gestionar la modificación general.
        partido_seleccionado = None
        la_modificacion_tiene_sentido = False
        while not(la_modificacion_tiene_sentido):
            repetir = True

            # Se solicita la ID del partido seleccionado y se verifica si coincide con algun partido.
            id_partido = input("Digite la ID del partido que desea modificar: ")            
            for partido in partidos:
                if id_partido == partido['id']:
                    partido_seleccionado = partido
                    print(f"Usted ha seleccionado el partido de ID: {partido['id']}")
                    repetir = False
                    break
            salva = partido['id']
            if repetir:
                print(f"Error. Ningún partido coincide con la ID ({id_partido})")
                continue
            
            # Este bloque se encarga de la modificación de cada detalle.
            print("\nA continuación, seleccione el detalle que desea modificar.\n")
            operacion = 0
            while (operacion != 4):

                # Imprime los detalles del partido y las operaciones que se pueden elegir.
                print(f"\nDetalles del partido (ID: {partido_seleccionado['id']})\n")
                print(f"Rival: {partido_seleccionado['rival']}\n",
                      f"Fecha: {partido_seleccionado['fecha']}\n",
                      f"Convocados: {partido_seleccionado['cantidad_convocados']}\n",
                      f"Estado: {partido_seleccionado['estado']}")            
                print(f"\n\nDigite (1) para cambiar el nombre del rival.",
                  "\nDigite (2) para cambiar la fecha del partido.",
                  "\nDigite (3) para realizar cambios sobre la lista de convocados.",
                  "\nDigite (4) para guardar los datos.")
                
                # Verifica que se introduzca una operación válida.
                try:
                    operacion = int(input("---> "))
                except ValueError:
                    print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                    continue
                if not((operacion == 1) or (operacion == 2) or (operacion == 3) or (operacion == 4)):
                    print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                    continue

                # Operación 1: Cambiar nombre del rival:
                if (operacion == 1):
                    nombre_correcto = False
                    
                    # Verifica que el FC Barcelona no sea elegido como rival.
                    while not(nombre_correcto):
                        partido_seleccionado['rival'] = input("Escriba el nuevo nombre del equipo rival: ")
                        if partido_seleccionado['rival'].strip() == "FC Barcelona":
                            print("Debes coleccionar muchos cromosomas, pero no podemos jugar contra nosotros mismos.")
                            continue
                        else:
                            nombre_correcto = True
                            print("Nombre guardado con éxito.")
                            break
                
                # Operación 2: Cambiar fecha del partido.
                if (operacion == 2):
                    print("\nA continuación, introduzca la nueva fecha en el formato (Día/Mes). Al finalizar se registrará como (Año-Mes-Día)") 
                    la_fecha_tiene_sentido = False

                    # Este bloque se encarga de gestionar la modificación de la fecha.
                    while not(la_fecha_tiene_sentido):
                        repetir = False

                        # Verifica que se introduzca una fecha válida.
                        try:
                            dia = int(input("Digite el número de día: "))
                            mes = int(input("Digite el número de mes: "))
                        except ValueError:
                            print("Entrada Inválida. Debe digitar números.")
                            continue            
                        try:
                            partido_seleccionado["fecha"] = date(2026, mes, dia)
                        except ValueError:
                            print(f"Entra Inválida. La fecha ({dia}/{mes}) no existe.")
                            continue
            
                        # Verifica que no exista otro partido en la misma fecha.
                        for partido in partidos:
                            if partido_seleccionado['id'] != partido['id']:
                                if partido_seleccionado['fecha'] == partido['fecha']:
                                    print(f"Fecha inválida. Ya existe un partido contra ({partido['rival']}) en esta misma fecha.")
                                    repetir = True
                                    break
                        if repetir:
                            continue

                        
                        # Verifica que la fecha esté en el rango del resto de la temporada 25/26
                        if partido_seleccionado["fecha"] < date.today():
                            print("Error. Usted ha introducido una fecha que ya pasó.")
                            continue
                        elif partido_seleccionado['fecha'] >= date(2026, 8, 1):
                            print("Entrada Inválida. Usted ha introducido una fecha que corresponde a la temporada 26/27.")
                            continue
                        else:
                            la_fecha_tiene_sentido = True
            
                        
                        print(f"\nModificación exitosa. Usted ha seleccionado el {partido_seleccionado['fecha']} como nueva fecha del partido.")
                
                # Añade los jugadores que no están lesionados a la lista de disponibles.
                disponibles_para_jugar = []                
                for jugador in disponibles:            
                    informacion_jugador = {'dorsal': None, 'nombre': None}
                    informacion_jugador['dorsal'] = jugador['dorsal']
                    informacion_jugador['nombre'] = jugador['nombre']
                    disponibles_para_jugar.append(informacion_jugador)   
                
                # Añade a los lesionados que ya deberían estar de regreso a la lista de disponibles.
                for lesionado in data['lesionados']:
                    if lesionado['regreso_estimado'] <= partido_seleccionado['fecha']:
                        informacion_jugador = {'dorsal': None, 'nombre': None}
                        informacion_jugador['dorsal'] = lesionado['dorsal']
                        informacion_jugador['nombre'] = lesionado['nombre']
                        print(f"{informacion_jugador['nombre']}({informacion_jugador['dorsal']}) ahora está disponible para este partido.")
                        disponibles_para_jugar.append(informacion_jugador)
                
                
                # Elimina de la lista de convocados a los lesionados que no estarán de regreso para la nueva fecha.
                for convocado in partido_seleccionado['convocados']:
                    la_disponibilidad_tiene_sentido = False
                    for jugador in disponibles_para_jugar:
                        if convocado['dorsal'] == jugador['dorsal']:
                            la_disponibilidad_tiene_sentido = True
                            break
                    if not(la_disponibilidad_tiene_sentido):
                        print(f"Aviso: {convocado['nombre']}({convocado['dorsal']}) ya no está disponible para este partido.")
                        partido_seleccionado['convocados'].remove(convocado)
                
                # Elimina de la lista de disponibles a los lesionados que no estarán de regreso para la nueva fecha.      
                for disponible in partido_seleccionado['disponibles']:
                    la_disponibilidad_tiene_sentido = False
                    for jugador in disponibles_para_jugar:
                        if disponible['dorsal'] == jugador['dorsal']:
                            la_disponibilidad_tiene_sentido = True
                            break
                    if not(la_disponibilidad_tiene_sentido):
                        print(f"Aviso: {convocado['nombre']}({convocado['dorsal']}) ya no está disponible para este partido.")
                        partido_seleccionado['disponibles'].remove(disponible)
                
                ya_estan_disponibles = []
                for jugador in disponibles_para_jugar:
                    if not((jugador in partido_seleccionado['disponibles']) or (jugador in partido_seleccionado['convocados'])):
                        ya_estan_disponibles.append(jugador)
                disponibles_para_jugar = ya_estan_disponibles

                partido_seleccionado['disponibles'] += disponibles_para_jugar
                # Operación 3: Modificar lista de convocados.
                if (operacion == 3):
                    print("\nUsted ha decidido realizar cambios sobre la lista de convocados.")

                    # Notifica en caso de que no haya jugadores convocados.
                    if not(partido_seleccionado['convocados']):
                        print("Sin embargo, no hay jugadores convocados para este partido.")
                                                
                    # Este bloque gestiona todas las operaciones con respecto a la lista de convocados.
                    opcion = 0
                    while (opcion != 4):
                        print("\n\nDigite (1) para añadir un jugador a la lista de convocados.",
                            "\nDigite (2) para eliminar un jugador de la lista de convocados.",
                            "\nDigite (3) para solicitar la lista de convocados.",
                            "\nDigite (4) para guardar los datos.")
                
                        # Verifica que se seleccione una opción válida.
                        try:
                            opcion = int(input("---> "))
                        except ValueError:
                            print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                            continue
                        if not((opcion == 1) or (opcion == 2) or (opcion == 3) or (opcion == 4)):
                            print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                            continue

                        # Opción 1: Añadir a la lista de lesionados.
                        if (opcion == 1):
                            print("Usted ha seleccionado la opción de añadir a la lista de Convocados.")

                            # Verifica que aún haya capacidad para convocar jugadores.
                            if (len(partido_seleccionado['convocados']) == 18):
                                print("Sin embargo ya se ha alcanzado el máximo de convocados (18).")
                                continue
                            
                            # Imprime la lista de jugadores disponibles para el partido.
                            print("\n\nJUGADORES DISPONIBLES:\n")
                            if not(partido_seleccionado['disponibles']):
                                print("\tNo hay más jugadores disponibles para este partido.")
                                continue
                            else:
                                for jugador in partido_seleccionado['disponibles']:
                                    print(f"\t{jugador['dorsal']} - {jugador['nombre']}")

                            # Verifica que el jugador seleccionado esté disponible para añadir al partido.
                            la_convocatoria_tiene_sentido = False
                            while not(la_convocatoria_tiene_sentido):                               
                                try:
                                    dorsal_seleccionado = int(input("Digite el dorsal del jugador que desea convocar: "))
                                except ValueError:
                                    print("Entrada Inválida. Debe digitar un número")
                                    continue
                                for jugador in partido_seleccionado['disponibles']:
                                    if dorsal_seleccionado == jugador['dorsal']:
                                        la_convocatoria_tiene_sentido = True
                                        partido_seleccionado['convocados'].append(jugador)
                                        partido_seleccionado['disponibles'].remove(jugador)
                                        print(f"\n>>> {jugador['nombre']} ha sido añadido a la lista de convocados.")
                                        break
                                if not(la_convocatoria_tiene_sentido):
                                    el_jugador_ya_esta_convocado = False 
                                    el_jugador_existe = False        
                                    for convocado in partido_seleccionado['convocados']:
                                        if dorsal_seleccionado == convocado['dorsal']:
                                            el_jugador_ya_esta_convocado = True
                                            print(f"¡{convocado['nombre']}({convocado['dorsal']}) ya está convocado para este partido!")  
                                            el_jugador_existe = True                                 
                                                                   
                                    if not(el_jugador_ya_esta_convocado):
                                        for jugador in data['plantel']:
                                            if dorsal_seleccionado == jugador['dorsal']:
                                                el_jugador_existe = True
                                                print(f"{jugador['nombre']}({jugador['dorsal']}) no está disponible para este partido.")
                                                break
                                    if not(el_jugador_existe):
                                        print(f"Error. Ningún jugador usa el dorsal {dorsal_seleccionado}.")
                                    continue

                        # Opción 2: Eliminar jugador de la lista de convocados.
                        if (opcion == 2):
                            print("Usted ha seleccionado la opción de eliminar jugador de la lista de convocados.")
                            
                            # Verifica que la lista de convocados no esté vacía y la imprime.
                            if not(partido_seleccionado['convocados']):
                                print("Sin embargo, actualmente no hay jugadores convocados.")
                                continue                    
                            print("\n\nLISTA DE CONVOCADOS:\n\n")
                            for jugador in partido_seleccionado['convocados']:
                                print(f"\t|{jugador['dorsal']} - {jugador['nombre']}|")

                            # Verifica que el jugador seleccionado esté en la lista de convocados.
                            la_eliminacion_tiene_sentido = False
                            while not(la_eliminacion_tiene_sentido):
                                try:
                                    dorsal_seleccionado = int(input("Digite el dorsal del jugador que desea eliminar de la lista de convocados: "))
                                except ValueError:
                                    print("Entrada Inválida. Debe digitar un número.")
                                    continue                        
                                for jugador in partido_seleccionado['convocados']:
                                    if dorsal_seleccionado == jugador['dorsal']:
                                        la_eliminacion_tiene_sentido = True
                                        partido_seleccionado['disponibles'].append(jugador)
                                        partido_seleccionado['convocados'].remove(jugador)
                                        print(f"\n >>> {jugador['nombre']} ha sido eliminado de la lista de convocados.")
                                        break
                                if not(la_eliminacion_tiene_sentido):
                                    print("El jugador seleccionado no está en la lista de convocados.")
                                    continue

                        # Opción 3: Solicitar lista de convocados.
                        if (opcion == 3):
                            print("Usted ha solicitado la lista de convocados.")

                            # Imprime la lista de convocados.
                            if not(partido_seleccionado['convocados']):
                                print("Sin embargo, actualmente no hay jugadores convocados.")
                                continue
                            else:
                                print("\n\nLISTA DE CONVOCADOS:\n\n")
                                for jugador in partido_seleccionado['convocados']:
                                    print(f"\t|{jugador['dorsal']} - {jugador['nombre']}|")

                        # Opción 4: Guardar cambios sobre la lista de convocados.
                        if (opcion == 4):
                            repetir = False

                            # Se notifica en caso de no estar completa la lista de convocados.
                            # El usuario puede elegir si seguir editando o guardar de todas formas.
                            if (len(partido_seleccionado['convocados']) < 18):
                                print("¡ADVERTENCIA! La lista de convocados no está completa, si aún está incompleta el día del partido, se contará como derrota por 3 - 0.")
                                respuesta_correcta = False
                                while not(respuesta_correcta):
                                    respuesta = input("¿Desea guardar los datos de todas formas? (Sí/No) ---> ").lower()
                                    if (respuesta.strip() == "sí") or (respuesta.strip() == "si"):
                                        respuesta_correcta = True                                    
                                        partido_seleccionado['cantidad_convocados'] = len(partido_seleccionado['convocados'])
                                        partido_seleccionado['estado'] = "!"
                                        print("Datos guardados.")
                                    elif (respuesta.strip() == "no"):
                                        respuesta_correcta = True
                                        repetir = True
                                    else:
                                        print("Entrada Inválida. Debe responder (Sí) o (No).")
                                        continue
                            if repetir:
                               continue
                            if len(partido_seleccionado['convocados']) == 18:                                
                                partido_seleccionado['cantidad_convocados'] = len(partido_seleccionado['convocados'])
                                partido_seleccionado['estado'] = "OK"
                    
                            los_convocados_tienen_sentido = True                    

                # Operación 4: Guardar cambios.
                if (operacion == 4):
                    
                    # Se asigna una nueva ID al partido modificado y se sobrescriben los datos del anterior.
                    for partido in partidos:
                        if partido_seleccionado['id'] == partido['id']:                
                            partido_seleccionado['id'] = partido_seleccionado['fecha'].strftime("%Y%m%d")
                            print(f"Datos guardados con éxito. La ID del partido ({salva}) ahora es ({partido_seleccionado['id']}).")
                            partido = partido_seleccionado
                            la_modificacion_tiene_sentido = True
                                     
    # Operación 5: Guardar y salir.
    if (bandera == 5):

        # Se guardan todos los datos en el archivo JSON
        data['partidos'] = partidos               
        for partido in data['partidos']:
            partido['fecha'] = partido['fecha'].strftime("%d-%m-%Y")
        for lesionado in data['lesionados']:
            lesionado['regreso_estimado'] = lesionado['regreso_estimado'].strftime("%d-%m-%Y")
        with open("./datos.json", 'w') as f:
            json.dump(data, f, indent=2)

print("Sesión terminada.")