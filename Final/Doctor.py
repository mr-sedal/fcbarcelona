'''

El programa se encarga de gestionar la disponibilidad de los jugadores del FC Barcelona
en los partidos de LaLiga 25/26

'''

from datetime import datetime, date, timedelta
import json


with open("Proyecto/Final/datos.json" , 'r') as f:
    data = json.load(f)

plantel = data['plantel']

lesionados = data['lesionados']
cantidad_lesionados = 0

print("Bienvenido al gestor de lesionados del FC Barcelona, doctor.\n")

bandera = 0

while (bandera != 5):
    
    print("Operaciones disponibles: \n\t"
      "1. Solicitar lista de lesionados\n\t2. Añadir lesionado/s.\n\t" 
      "3. Quitar lesionado/s.\n\t4. Modificar información de lesionado.\n\t"
      "5. Guardar y Salir.")
    try: 
        bandera = int(input("Introduzca el número asignado a la operación deseada: "))
        nuevo_lesionado = {'dorsal' : 0, 'nombre' : "Jugador", 'tipo_lesion' : "Desconocida", 'semanas_de_baja' : 0, 'regreso_estimado' : 0} 
        if (bandera < 1) or (bandera > 5):  # Esta  le indica al usuario que su operacion no esta definida
            print("¡ERROR! Debe digitar un número entre 1 y 5.")
        elif (bandera == 1): # Esta se va a encargar de mostrar la lista lesionados
            if not(lesionados):
                print("No hay jugadores lesionados en este momento.")
            else:
                print("LISTA DE LESIONADOS:\n\t")
                for lesionado in lesionados:
                    print(f"|{lesionado['nombre']}({lesionado['dorsal']})|",
                          f"|Tipo de lesion: {lesionado['tipo_lesion']}|",
                          f"|Regreso estimado: {lesionado['regreso_estimado']}|")
    except ValueError:
        print("Entrada inválida. Digite un número entre 1 y 5.")
        continue
    
    
    if (bandera == 2):  # Esta se va a encargar de añadir lesionados
 
        
        
        
        las_semanas_de_baja_tienen_sentido = False
        el_nombre_es_correcto = False
        while not(el_nombre_es_correcto):  # Este bloque será para poner el nombre del jugador lesionado
            el_jugador_esta_en_el_plantel = False
            el_jugador_no_estaba_lesionado = True
            
            try:
                dorsal_lesionado = int(input("Introduzca el dorsal del jugador lesionado: "))
                nuevo_lesionado['dorsal'] = dorsal_lesionado
                for jugador in plantel:
                    if (dorsal_lesionado == jugador['dorsal']):
                        nuevo_lesionado['nombre'] = jugador['nombre']
                        el_jugador_esta_en_el_plantel = True
                        break
            except ValueError:
                print("Entrada Inválida. Debe digitar un número.")
                continue    
            if not(el_jugador_esta_en_el_plantel):
                print("¡ERROR! Ningún jugador usa ese dorsal.")
                continue
            for lesionado in lesionados:
                if (dorsal_lesionado == lesionado['dorsal']):
                    print("¡ERROR! Ya indicó que ese jugador está lesionado.")
                    el_jugador_no_estaba_lesionado = False
                    break
            if (el_jugador_no_estaba_lesionado == False):
                continue
                   
            if (el_jugador_esta_en_el_plantel and el_jugador_no_estaba_lesionado):
                el_nombre_es_correcto = True
            print(f"Se ha añadido a {nuevo_lesionado['nombre']}({dorsal_lesionado}) a la lista de lesionados.")
        
        nuevo_lesionado['tipo_lesion'] = input("Tipo de lesión: ")

        while not(las_semanas_de_baja_tienen_sentido):

            try:
                nuevo_lesionado['semanas_de_baja'] = int(input("Semanas de baja estimadas: "))
                if (nuevo_lesionado['semanas_de_baja'] <= 0):
                    print("¡Error! Debe digitar un número mayor que 0.")
                    continue
                else:
                    las_semanas_de_baja_tienen_sentido = True
            except ValueError:
                print("Entrada Inválida. Debe digitar un número.")
                continue
            nuevo_lesionado['regreso_estimado'] = date.today() + timedelta(nuevo_lesionado['semanas_de_baja'] * 7)
            nuevo_lesionado['regreso_estimado'] = nuevo_lesionado['regreso_estimado'].strftime("%d-%m-%Y")
        lesionados.append(nuevo_lesionado)
        print("Los datos del lesionado se han registrado con éxito.")

    if (bandera == 3):  # Esta se va a encargar de remover jugadores de la lista de lesionados

        if not(lesionados):
            print("No hay jugadores lesionados en este momento.")
            continue
        el_jugador_no_estaba_lesionado = True
        
        while el_jugador_no_estaba_lesionado:
            
            el_jugador_esta_en_el_plantel = False
            try:
                dorsal_lesionado = int(input("Digite el dorsal del jugador que desea eliminar de la lista de lesionados: "))
            except ValueError:
                print("Entrada Inválida. Debe digitar un número.")    
                continue
            for jugador in plantel:
                if (jugador['dorsal'] == dorsal_lesionado):
                    el_jugador_esta_en_el_plantel = True
                    nombre_lesionado = jugador['nombre']
                    break
            if not(el_jugador_esta_en_el_plantel):
                print("¡ERROR! Ningún jugador usa ese dorsal.")
                continue
            for lesionado in lesionados:
                if lesionado['dorsal'] == dorsal_lesionado:
                    print(f"{lesionado['nombre']} ha sido removido con éxito de la lista de lesionados.")
                    for jugador in plantel:
                        if lesionado['dorsal'] == jugador['dorsal']:
                            jugador['lesion'] = "N/A"
                            break
                    lesionados.remove(lesionado)
                    el_jugador_no_estaba_lesionado = False
                    break
            if el_jugador_no_estaba_lesionado:
                print(f"{nombre_lesionado} no está en la lista de lesionados.")
    
    if (bandera == 4):  # Esta se va a encargar de modificar informacion de los lesionados

        if not(lesionados):  # Esto se encarga de verificar si no existen jugadores lesionados
            print("No hay jugadores lesionados en este momento.")
            continue

        los_datos_están_correctos = False
        while not(los_datos_están_correctos):
            el_jugador_no_estaba_lesionado = True
            el_jugador_esta_en_el_plantel = False
            repetir = False  
            print("LESIONADOS: \n")
            for lesionado in lesionados:
                print( f"|Nombre: {lesionado['nombre']}({lesionado['dorsal']})|", 
                      f"|Tipo de lesión: {lesionado['tipo_lesion']}|", 
                      f"|Semanas de baja: {lesionado['semanas_de_baja']}|",
                      f"|Regreso estimado: {lesionado['regreso_estimado']}|")
            try:  # Pide el dorsal del jugador lesionado
                dorsal_lesionado = int(input("Seleccione el dorsal del jugador lesionado para cambiar sus datos: "))
            except ValueError: # Verifica que la entrada sea un numero
                print("Entrada inválida. Debe digitar un número.")
                continue
            for jugador in plantel: # Recorre el plantel buscando un jugador cuyo dorsal coincida con el selccionado
                if jugador['dorsal'] == dorsal_lesionado:
                    el_jugador_esta_en_el_plantel = True
                    nombre_lesionado = jugador['nombre']
                    break
            if not(el_jugador_esta_en_el_plantel): # Si no se encontró ningun jugador, lo indica y se reinicia el bucle
                print("¡ERROR! Ningún jugador usa ese dorsal.")
                continue

            for lesionado in lesionados: # Verifica que el jugador seleccionado ya estuviera lesionado
                if lesionado['dorsal'] == dorsal_lesionado:
                    nuevo_lesionado = lesionado
                    el_jugador_no_estaba_lesionado = False
                    break
            if el_jugador_no_estaba_lesionado: # Si el jugador no estaba lesionado, reinicia el bucle
                print(f"{nombre_lesionado} no está en la lista de lesionados.")
                continue
            operacion = 0
            while (operacion != 1) or (operacion != 2):
                print("Ficha del lesionado:", f"\n\tNombre: {nuevo_lesionado['nombre']}({nuevo_lesionado['dorsal']})",
                      f"\n\tTipo de lesión: {nuevo_lesionado['tipo_lesion']}", f"\n\tSemanas de baja: {nuevo_lesionado['semanas_de_baja']}",
                      f"\n\tRegreso estimado: {nuevo_lesionado['regreso_estimado']}")
                try:
                    operacion = int(input("\nDigite (1) para modificar el tipo de lesion. \nDigite (2) para cambiar las semanas de baja.\n---> "))
                except ValueError:
                    print("Entrada Inválida. Debe digitar un número entre 1 y 2.")
                    continue
                if (operacion == 1) or (operacion == 2):
                    break
                else:
                    print("¡ERROR! Esa operación no está definida.")
                    continue
                    
                    
            if (operacion == 1):
                print("Usted ha seleccionado el tipo de lesion")
                nuevo_lesionado['tipo_lesion'] = input("Escriba la nueva lesión: ")
                print("Datos guardados con éxito")
            if (operacion == 2):
                las_semanas_de_baja_tienen_sentido = False
                print("Usted ha seleccionado las semanas de baja.")
                while not(las_semanas_de_baja_tienen_sentido):
                    try:
                        nuevo_lesionado['semanas_de_baja'] = int(input("Digite la nueva cantidad de semanas de baja: "))
                    except ValueError:
                        print("Entrada Inválida. Debe digitar un número.")
                        continue
                    if (nuevo_lesionado['semanas_de_baja'] <= 0):
                        print("La nueva cantidad de semanas de baja es inferior a 1.")
                        respuesta = "x"
                        while (respuesta != "si") or (respuesta != "no"): #Esto no está completo. Estoy intentando perfeccionarlo
                            respuesta = input("Desea eliminar a este jugador de la lista de lesionados(Si/No) >>> ").lower()
                            if (respuesta.strip() == "si") or (respuesta.strip == "sí"):
                                for lesionado in lesionados:
                                    if lesionado['nombre'] == nuevo_lesionado['nombre']:
                                        print(f"{lesionado['nombre']} ha sido eliminado de la lista de lesionados.")
                                        lesionados.remove(lesionado)
                                        las_semanas_de_baja_tienen_sentido = True
                                        break
                                break    
                       
                            elif (respuesta.strip() == "no"):

                                print("Las semanas de baja deben ser mayor o igual a 1. Digite una nueva operación.")
                                las_semanas_de_baja_tienen_sentido = False
                                break
                            else:
                                print("Entrada inválida. Debe digitar 'Sí' o 'No'.")
                                continue
                       
                    else:
                        las_semanas_de_baja_tienen_sentido = True
                        for lesionado in lesionados:
                            if lesionado['nombre'] == nuevo_lesionado['nombre']:
                                lesionado['semanas_de_baja'] = nuevo_lesionado['semanas_de_baja']
                                lesionado['regreso_estimado'] = date.today() + timedelta(nuevo_lesionado['semanas_de_baja'] * 7)
                                lesionado['regreso_estimado'] = lesionado['regreso_estimado'].strftime("%d-%m-%Y")
                        print(f"Los datos sobre la lesión de {nuevo_lesionado['nombre']} han sido modificados con éxito.")
            
            while (operacion != "sí") or (operacion != "si") or (operacion != "no"):
                operacion = input("¿Desea modificar la informacion de otro jugador? (Sí/No) >>> ").lower() 
                if (operacion.strip() == "si") or (operacion.strip() == "sí"):
                    repetir = True
                    break
                if operacion.strip() == "no":
                    repetir = False
                    break
                else:
                    print("Entrada inválida. Debe digitar 'Sí' o 'No'.")
                    continue

            if repetir:
                continue
            elif not(repetir):
                break    




                    
    if (bandera != 5):
        print("\n¿Desea realizar otra operación?\n")
    
for lesionado in lesionados:
    for jugador in plantel:
        if lesionado['dorsal'] == jugador['dorsal']:
            jugador['lesion'] = lesionado['tipo_lesion']
            break

disponibles = []
for jugador in plantel:
    el_jugador_esta_sano = True
    for lesionado in lesionados:
        if jugador['dorsal'] == lesionado['dorsal']:
            el_jugador_esta_sano = False
            break
    if el_jugador_esta_sano:    
        disponibles.append(jugador)

datos = {"plantel" : plantel, "lesionados": lesionados, "disponibles": disponibles, "partidos": data['partidos']}

print("Sesión terminada. Datos guardados.")

with open("Proyecto/Final/datos.json", 'w') as f:
    json.dump(datos, f, indent=2)
    

