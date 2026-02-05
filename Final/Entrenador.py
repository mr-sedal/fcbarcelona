# Vision del Entrenador
'''
Las funciones deberian ser:
- Mostrar Partidos (ordenados cronológicamente)*
- Añadir Partido (Fecha, Rival, Convocados)
- Eliminar Partido
- Modificar Partido (Fecha, Rival, Convocados)
- Guardar los datos

Nota: Los partidos en los que haya menos de 20 jugadores convocados deben considerarse derrotas por ausencia
Nota: 
'''



from datetime import date, timedelta
import json

def validar_fecha(string):
    #Esta funcion transforma las fechas almacenadas en string en el JSON, en fechas de tipo date.
    
    dia = int(string[0] + string[1])
    mes = int(string[3] + string[4])
    año = int(string[6:])
    nueva_fecha = date(año, mes, dia)
    return nueva_fecha



with open("Proyecto/Final/datos.json") as f:
    data = json.load(f)

for lesionado in data['lesionados']:
    lesionado['regreso_estimado'] = validar_fecha(lesionado['regreso_estimado'])
for partido in data['partidos']:
    partido['fecha'] = validar_fecha(partido['fecha'])

disponibles = data['disponibles']


print("Bienvenido, Entrenador. Usted será el encargado de gestionar los partidos de nuestro club.\n\n\n")
bandera = 0
partidos = data['partidos']

cambios_en_disponibilidad = False
for partido in partidos:
    for convocado in partido['convocados']:
        for lesionado in data['lesionados']:
            if convocado['dorsal'] == lesionado['dorsal']:
                if lesionado['regreso_estimado'] < partido['fecha']:
                    partido['convocados'].remove(convocado)
                    cambios_en_disponibilidad = True
    for disponible in partido['disponibles']:
        for lesionado in data['lesionados']:
            if disponible['dorsal'] == lesionado['dorsal']:
                if lesionado['regreso_estimado'] < partido['fecha']:
                    partido['disponibles'].remove(disponible)
                    cambios_en_disponibilidad = True
if cambios_en_disponibilidad:
    print("\n\n\nADVERTENCIA: Hubo cambios en la disponibilidad de ciertos partidos debido a cambios en la lista de lesionados.")
    print("Se recomienda revisar los detalles de todos los partidos.\n\n\n")



while (bandera != 5):

    print("Operaciones disponibles: \n\t"
      "1. Solicitar lista de partidos.\n\t2. Añadir partido.\n\t" 
      "3. Eliminar partido.\n\t4. Modificar detalles de partido.\n\t"
      "5. Guardar y Salir.")
    
    try:
        bandera = int(input("Introduzca el número de la operación deseada: "))
    except ValueError:
        print("Entrada Inválida. Debe digitar un número entre 1 y 5.")
        continue

    if (bandera <= 0) or (bandera > 5):
        print("Entrada Inválida. Debe digitar un número entre 1 y 5.")
        continue

    if (bandera == 1):
        if not(partidos):
            print("\nNo hay partidos establecidos actualmente.")
        else:
            print("LISTA DE PARTIDOS:\n\n\n")
            for partido in partidos:
                print(f"ID: {partido['id']} || Rival: {partido['rival']} ({partido['fecha']}) || Estado: {partido['estado']}")
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
                else:
                    print("Entrada Inválida. Debe digitar (Sí) o (No).")
                    continue
        

    if (bandera == 2):

        nuevo_partido = {'id': None, 'rival': None, 'fecha': None, 'cantidad_convocados' : None, 'convocados': [], 'disponibles': [], 'estado': None}
        
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

        print("\nA continuación, introduzca la fecha en el formato (Día/Mes). Al finalizar se registrará como (Año-Mes-Día)") 
        la_fecha_tiene_sentido = False
        while not(la_fecha_tiene_sentido):
            repetir = False
            try:
                dia = int(input("Digite el número de día: "))
                mes = int(input("Digite el número de mes: "))
            except ValueError:
                print("Entrada Inválida. Debe digitar números.")
                continue
            
            try:
                nuevo_partido["fecha"] = date(2026, mes, dia)
            except ValueError:
                print(f"Entra Inválida. La fecha ({dia}/{mes}) no existe.")
                continue
            
            for partido in partidos:
                if nuevo_partido['fecha'] == partido['fecha']:
                    print(f"Fecha inválida. Ya existe un partido contra ({partido['rival']}) en esta misma fecha.")
                    repetir = True
                    break
            
            if repetir:
                continue

            if nuevo_partido["fecha"] < date.today():
                print("Error. Usted ha introducido una fecha que ya pasó.")
                continue
            elif nuevo_partido['fecha'] >= date(2026, 8, 1):
                print("Entrada Inválida. Usted ha introducido una fecha que corresponde a la temporada 26/27.")
                continue
            else:
                la_fecha_tiene_sentido = True
            
            nuevo_partido['id'] = nuevo_partido['fecha'].strftime("%Y%m%d") 
            print(f"\nDatos correctos. Usted ha seleccionado el {nuevo_partido['fecha']} como fecha del partido.")
        
        print("\nA continuación, se le asignará la lista de jugadores disponibles para convocar.")
        
        disponibles_para_jugar = []
        for jugador in disponibles:            
            informacion_jugador = {'dorsal': None, 'nombre': None}
            informacion_jugador['dorsal'] = jugador['dorsal']
            informacion_jugador['nombre'] = jugador['nombre']
            disponibles_para_jugar.append(informacion_jugador)
            
        

        for lesionado in data['lesionados']:

            if lesionado['regreso_estimado'] <= nuevo_partido['fecha']:
                informacion_jugador = {'dorsal': None, 'nombre': None}
                informacion_jugador['dorsal'] = lesionado['dorsal']
                informacion_jugador['nombre'] = lesionado['nombre']
                disponibles_para_jugar.append(informacion_jugador)
                       
        
            
        convocados = []
        los_convocados_tienen_sentido = False
        while not(los_convocados_tienen_sentido):
            
            print("\n\nJugadores Disponibles:\n")
            for jugador in disponibles_para_jugar:
                print(f"\t{jugador['dorsal']} - {jugador['nombre']}")

            operacion = None
            
            while (operacion != 4):
                print("\n\nDigite (1) para añadir un jugador a la lista de convocados.",
                  "\nDigite (2) para eliminar un jugador de la lista de convocados.",
                  "\nDigite (3) para solicitar la lista de convocados.",
                  "\nDigite (4) para guardar los datos.")
                
                try:
                    operacion = int(input("---> "))
                except ValueError:
                    print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                    continue
                if not((operacion == 1) or (operacion == 2) or (operacion == 3) or (operacion == 4)):
                    print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                    continue
                
                if (operacion == 1):
                    print("Usted ha seleccionado la opción de añadir a la lista de Convocados.")
                    if len(convocados) == 20:
                        print("Sin embargo ya se ha alcanzado el máximo de convocados (20).")
                        continue
                    
                    print("\n\nJUGADORES DISPONIBLES:\n")
                    if not(disponibles_para_jugar):
                        print("\tNo hay más jugadores disponibles para este partido.")
                        continue
                    else:
                        for jugador in disponibles_para_jugar:
                            print(f"\t{jugador['dorsal']} - {jugador['nombre']}")

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
                            print("El jugador seleccionado no está disponible para este partido.")
                            continue
                
                
                if (operacion == 2):
                    print("Usted ha seleccionado la opción de eliminar jugador de la lista de convocados.")
                    if not(convocados):
                        print("Sin embargo, actualmente no hay jugadores convocados.")
                        continue
                    
                    print("\n\nLISTA DE CONVOCADOS:\n\n")
                    for jugador in convocados:
                        print(f"\t|{jugador['dorsal']} - {jugador['nombre']}|")

                    la_eliminacion_tiene_sentido = False
                    while not(la_eliminacion_tiene_sentido):
                        try:
                            dorsal_seleccionado = int(input("Digite el dorsal del jugador que desea eliminar de la lista de convocados: "))
                        except ValueError:
                            print("Entrada Inválida. Debe digitar un número.")
                            continue
                        
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
                

                if (operacion == 3):
                    print("Usted ha solicitado la lista de convocados.")
                    if not(convocados):
                        print("Sin embargo, actualmente no hay jugadores convocados.")
                        continue
                    else:
                        print("\n\nLISTA DE CONVOCADOS:\n\n")
                        for jugador in convocados:
                            print(f"\t|{jugador['dorsal']} - {jugador['nombre']}|")


                if (operacion == 4):
                    repetir = False
                    if (len(convocados) < 20):
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
                    
                    if len(convocados) == 20:
                        nuevo_partido["convocados"] = convocados
                        nuevo_partido['cantidad_convocados'] = len(convocados)
                        nuevo_partido['estado'] = "OK"
                    
                    los_convocados_tienen_sentido = True
        nuevo_partido['disponibles'] = disponibles_para_jugar
        partidos.append(nuevo_partido)          
    
                                                  
    if (bandera == 3):

        if not(partidos):
            print("Actualmente no hay partidos planificados.")
            continue
        
        print("\n\n")
        for partido in partidos:
            print(f"ID: {partido['id']} || Rival: {partido['rival']} ({partido['fecha']}) || Estado: {partido['estado']}")
        
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
                print("Esa ID no coincide con la de ningún partido.")
                continue

    if (bandera == 4):

        if not(partidos):
            print("Actualmente no hay partidos planificados.")
            continue
        
        print("\n\n")
        for partido in partidos:
            print(f"ID: {partido['id']} || Rival: {partido['rival']} ({partido['fecha']}) || Convocados: {partido['cantidad_convocados']} || Estado: {partido['estado']}")
        
        partido_seleccionado = None
        la_modificacion_tiene_sentido = False
        while not(la_modificacion_tiene_sentido):
            repetir = True

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
            
           
            print("\nA continuación, seleccione el detalle que desea modificar.\n")
            operacion = 0
            while (operacion != 4):

                print(f"\nDetalles del partido (ID: {partido_seleccionado['id']})\n")
                print(f"Rival: {partido_seleccionado['rival']}\n",
                      f"Fecha: {partido_seleccionado['fecha']}\n",
                      f"Convocados: {partido_seleccionado['cantidad_convocados']}\n",
                      f"Estado: {partido_seleccionado['estado']}")
            
                print(f"\n\nDigite (1) para cambiar el nombre del rival.",
                  "\nDigite (2) para cambiar la fecha del partido.",
                  "\nDigite (3) para realizar cambios sobre la lista de convocados.",
                  "\nDigite (4) para guardar los datos.")
                
                try:
                    operacion = int(input("---> "))
                except ValueError:
                    print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                    continue
                if not((operacion == 1) or (operacion == 2) or (operacion == 3) or (operacion == 4)):
                    print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                    continue

                if (operacion == 1):
                    nombre_correcto = False
                    while not(nombre_correcto):
                        partido_seleccionado['rival'] = input("Escriba el nuevo nombre del equipo rival: ")
                        if partido_seleccionado['rival'].strip() == "FC Barcelona":
                            print("Debes coleccionar muchos cromosomas, pero no podemos jugar contra nosotros mismos.")
                            continue
                        else:
                            nombre_correcto = True
                            print("Nombre guardado con éxito.")
                            break
                
                if (operacion == 2):

                    print("\nA continuación, introduzca la nueva fecha en el formato (Día/Mes). Al finalizar se registrará como (Año-Mes-Día)") 
                    la_fecha_tiene_sentido = False
                    while not(la_fecha_tiene_sentido):
                        repetir = False
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
            
                        for partido in partidos:
                            if partido_seleccionado['fecha'] == partido['fecha']:
                                print(f"Fecha inválida. Ya existe un partido contra ({partido['rival']}) en esta misma fecha.")
                                repetir = True
                                break
            
                        

                        if partido_seleccionado["fecha"] < date.today():
                            print("Error. Usted ha introducido una fecha que ya pasó.")
                            continue
                        elif partido_seleccionado['fecha'] >= date(2026, 8, 1):
                            print("Entrada Inválida. Usted ha introducido una fecha que corresponde a la temporada 26/27.")
                            continue
                        else:
                            la_fecha_tiene_sentido = True
            
                        if repetir:
                            continue

                        print(f"\nModificación exitosa. Usted ha seleccionado el {partido_seleccionado['fecha']} como nueva fecha del partido.")
                
                disponibles_para_jugar = []
                for jugador in disponibles:            
                    informacion_jugador = {'dorsal': None, 'nombre': None}
                    informacion_jugador['dorsal'] = jugador['dorsal']
                    informacion_jugador['nombre'] = jugador['nombre']
                    disponibles_para_jugar.append(informacion_jugador)                  

                for lesionado in data['lesionados']:
                    if lesionado['regreso_estimado'] <= partido_seleccionado['fecha']:
                        informacion_jugador = {'dorsal': None, 'nombre': None}
                        informacion_jugador['dorsal'] = lesionado['dorsal']
                        informacion_jugador['nombre'] = lesionado['nombre']
                        disponibles_para_jugar.append(informacion_jugador)
                
                
                for convocado in partido_seleccionado['convocados']:
                    la_disponibilidad_tiene_sentido = False
                    for jugador in disponibles_para_jugar:
                        if convocado['dorsal'] == jugador['dorsal']:
                            la_disponibilidad_tiene_sentido = True
                            break
                    if not(la_disponibilidad_tiene_sentido):
                        print(f"Aviso: {convocado['nombre']}({convocado['dorsal']}) ha sido tomado como lesionado.")
                        partido_seleccionado['convocados'].remove(convocado)
                
                for disponible in partido_seleccionado['disponibles']:
                    la_disponibilidad_tiene_sentido = False
                    for jugador in disponibles_para_jugar:
                        if disponible['dorsal'] == jugador['dorsal']:
                            la_disponibilidad_tiene_sentido = True
                            break
                    if not(la_disponibilidad_tiene_sentido):
                        print(f"Aviso: {convocado['nombre']}({convocado['dorsal']}) ha sido tomado como lesionado.")
                        partido_seleccionado['disponibles'].remove(disponible)
                        


                if (operacion == 3):

                    print("\nUsted ha decidido realizar cambios sobre la lista de convocados.")
                    if not(partido_seleccionado['convocados']):
                        print("Sin embargo, no hay jugadores convocados para este partido.")
                        

                    opcion = 0
                    while (opcion != 4):
                        print("\n\nDigite (1) para añadir un jugador a la lista de convocados.",
                            "\nDigite (2) para eliminar un jugador de la lista de convocados.",
                            "\nDigite (3) para solicitar la lista de convocados.",
                            "\nDigite (4) para guardar los datos.")
                
                        try:
                            opcion = int(input("---> "))
                        except ValueError:
                            print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                            continue
                        if not((opcion == 1) or (opcion == 2) or (opcion == 3) or (opcion == 4)):
                            print("Entrada Inválida. Debe digitar un número entre 1 y 4.")
                            continue

                        if (opcion == 1):

                            print("Usted ha seleccionado la opción de añadir a la lista de Convocados.")
                            if (len(partido_seleccionado['convocados']) == 20):
                                print("Sin embargo ya se ha alcanzado el máximo de convocados (20).")
                                continue
                    
                            print("\n\nJUGADORES DISPONIBLES:\n")
                            if not(partido_seleccionado['disponibles']):
                                print("\tNo hay más jugadores disponibles para este partido.")
                                continue
                            else:
                                for jugador in partido_seleccionado['disponibles']:
                                    print(f"\t{jugador['dorsal']} - {jugador['nombre']}")

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
                                    print("El jugador seleccionado no está disponible para este partido.")
                                    continue


                        if (opcion == 2):
                            print("Usted ha seleccionado la opción de eliminar jugador de la lista de convocados.")
                            if not(partido_seleccionado['convocados']):
                                print("Sin embargo, actualmente no hay jugadores convocados.")
                                continue
                    
                            print("\n\nLISTA DE CONVOCADOS:\n\n")
                            for jugador in partido_seleccionado['convocados']:
                                print(f"\t|{jugador['dorsal']} - {jugador['nombre']}|")

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


                        if (opcion == 3):
                            print("Usted ha solicitado la lista de convocados.")
                            if not(partido_seleccionado['convocados']):
                                print("Sin embargo, actualmente no hay jugadores convocados.")
                                continue
                            else:
                                print("\n\nLISTA DE CONVOCADOS:\n\n")
                                for jugador in partido_seleccionado['convocados']:
                                    print(f"\t|{jugador['dorsal']} - {jugador['nombre']}|")


                        if (opcion == 4):
                            repetir = False
                            if (len(partido_seleccionado['convocados']) < 20):
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
                            if len(partido_seleccionado['convocados']) == 20:                                
                                partido_seleccionado['cantidad_convocados'] = len(partido_seleccionado['convocados'])
                                partido_seleccionado['estado'] = "OK"
                    
                            los_convocados_tienen_sentido = True                    


                if (operacion == 4):

                    for partido in partidos:
                        if partido_seleccionado['id'] == partido['id']:
                
                            partido_seleccionado['id'] = partido_seleccionado['fecha'].strftime("%Y%m%d")
                            print(f"Datos guardados con éxito. La ID del partido ({salva}) ahora es ({partido_seleccionado['id']}).")
                            partido = partido_seleccionado
                            la_modificacion_tiene_sentido = True
                                     

    if (bandera == 5):
        data['partidos'] = partidos               
        for partido in data['partidos']:
            partido['fecha'] = partido['fecha'].strftime("%d-%m-%Y")
        for lesionado in data['lesionados']:
            lesionado['regreso_estimado'] = lesionado['regreso_estimado'].strftime("%d-%m-%Y")
        with open("Proyecto/Final/datos.json", 'w') as f:
            json.dump(data, f, indent=2)


            





                


        

