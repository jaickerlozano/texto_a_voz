'''Este script es el menú principal para ingresar el texto que
deseamos transformar de texto a voz'''

import texto_a_voz

# Opciones para elegir ingreso del texto
menu = {
    '1':'Ingresar texto manualmente',
    '2':'Abrir un archivo',
    '3':'Ingresar una URL',
    '4':'Salir'
}

def elegir_ingreso_de_texto():
    '''Esta función permite elegir de que forma ingresará el texto
    para reproducir a voz el usuario'''

    while True:
        print("\nSelecciona la fuente de ingreso del texto:\n")
        for key, value in menu.items():
            print(f"{key}.- {value}")

        opcion = input("\nElige una opción (1, 2, 3, 4): ")

        if opcion in menu.keys():
            return opcion
        else:
            print("Error. Debe elegir una opción disponible. Intente nuevamente\n")

# Se llama a la función para iniciar el programa
eleccion = elegir_ingreso_de_texto()

texto = None

if eleccion == '1':
    print("\nIngrese el texto manualmente: ")
    texto = input("")
    #texto_a_voz.procesar_texto_a_voz(texto)
    
elif eleccion == '2':
    print("\nIngrese nombre del archivo o la ruta donde se encuentra ubicado: ")
    archivo = input("")
    texto = texto_a_voz.abrir_texto(archivo)

elif eleccion == '3':
    url = input("\nIngrese la URL: ")
    selector = input("Ingresa el selector CSS para extraer el texto (por ejemplo, 'p' para párrafos): ")  
    texto = texto_a_voz.obtener_texto_de_url(url, selector)
    #url = 'https://keepcoding.io/blog/que-es-pygame/'
   
elif eleccion == '4':
    print("\nSaliendo del programa...")

# Verificación del texto antes de procesar
if texto:
    texto_a_voz.procesar_texto_a_voz(texto)