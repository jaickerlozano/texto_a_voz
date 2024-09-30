'''La idea de este proyecto es convertir un artículo existente en un archivo de audio reproducible 
en formato mp3. Para ello puedes hacer uso de bibliotecas existenes como nltk (kit de 
herramientas de lenguaje natural), newspaper3k y gtts (puedes seguir las instrucciones de 
instalación de pip). 
Puedes crear un programa al que proporcionarle una URL de un artículo a convertir para 
luego manejar la conversión de texto a voz. '''

# Importamos la librería pyttsx3 para pasar de texto a voz
import pyttsx3
# Librería para analizar textos
import nltk
# Librería para obtener el código URL
import requests
# Librería para extraer el texto de la HTML
from bs4 import BeautifulSoup
# Importa SelectorSyntaxError para manejar errores específicos
from soupsieve import SelectorSyntaxError
# Importamos la librería gTTs para guardar el texto en archivo .mp3
from gtts import gTTS

def abrir_texto(archivo):
    '''Esta función abre el texto que deseamos transformar'''
    try:
        # Abrimos el archivo donde se encuentra el texto
        with open(archivo, 'r', encoding='utf-8') as file:
            texto = file.read()
        return texto
    # Si se genera un error por no encontrar el archivo lo manejamos con este except
    except FileNotFoundError:
        print("Error: No se pudo obtener o leer el texto. Verifica la fuente de entrada.")
        return None
    except AttributeError as e:
        print(f"Error: Se ha producido un error de tipo {e}")

def validar_selector(selector):
    '''Esta función devuelve un True si el selector es válido
    de lo contrario devolverá un False'''

    try:
        # Intentar seleccionar un elemento con el selector proporcionado
        BeautifulSoup('', 'html.parser').select(selector)
        return True
    except SelectorSyntaxError:
        return False


def obtener_texto_de_url(url, selector = 'article h2, article p'):
    '''Con esta función obtenemos el texto o contenido de una url'''
    
    # Si el campo de la url está vacío arroja un mensaje de error y devuelve un None
    if not url.strip():
        print("Error: La URL proporcionada está vacía.")
        return None
    
    # Si el campo del selector está vacío o el selector no está dentro de la lista de selectores válidos, ingresa en este if_statement
    if not selector.strip() or not validar_selector(selector):
        print("Advertencia: No ha ingresado un selector válido, se utilizará el selector 'article h2, article p' por defecto:")
        selector = 'article h2, article p'

    try:
        # Obtener el contenido de la página web
        respuesta = requests.get(url)

        # Analizar el contenido HTML
        soup = BeautifulSoup(respuesta.content, 'html.parser')

        # Dentro de este soup.select se seleccionarán todos los elementos del selector y los guardará
        elementos = soup.select(selector)

        # Extraer el texto del artículo 
        texto = ' '.join([elemento.get_text() for elemento in elementos])

        return texto
    
    # Esta es una lista de excepciones que se maneja en solicitudes http y que arrojará el error en caso de existir
    except requests.exceptions.HTTPError as errh:
        print(f"Error HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error de Conexión: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Error de Tiempo de Espera: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error en la Solicitud: {err}")
    except SelectorSyntaxError as e:
        print(f"Error de Selector CSS: {e}")

    return None

def procesar_texto_a_voz(texto):
    '''Esta función procesa el texto para llevarlo a voz'''
    if not texto.strip():
        print("Error: No ha ingresado un texto para procesar.")
        return None
    
    try:
        if texto:
            # Letras con tilde que reemplazaremos
            vocales_con_tilde = {"á":"a","é":"e",
                                "í":"i","ó":"o",
                                "ú":"u","Á":"A",
                                "É":"E","Í":"I",
                                "Ó":"O","Ú":"U"}
            
            # Procesamos el texto
            
            texto_sin_acentos = ''.join([vocales_con_tilde.get(caracter, caracter) for caracter in texto])

            engine = pyttsx3.init()

            # Configurar la velocidad de de habla
            engine.setProperty('rate', 150)

            # Convertimos el texto a voz
            engine.say(texto_sin_acentos)
            engine.runAndWait()

        # Guardar archivo en formato .mp3
        print("¿Desea guardar el texto reproducido en un archivo .mp3?")
        si_no = input("Si (S) o No (N): ")

        if si_no.lower() == "s":
            nombre_archivo = input("Ingrese el nombre del archivo en formato .mp3: ")
            print(f"Guardando archivo {nombre_archivo}")
            audio_guardado = guardar_texto_a_voz(texto_sin_acentos, nombre_archivo)
            return audio_guardado
        
        else:
            print("Saliendo del programa...")
        return texto_sin_acentos
    
    # Excepciones
    except UnboundLocalError:
        print("Error: No ha ingresado un texto para poder reproducir.")
        return None
    except AttributeError as e:
        print(f"Error: Se ha producido un error de tipo {e}")
        return None

def guardar_texto_a_voz(texto, archivo_salida):
    '''Esta función guarda el texto procesado en voz en un
    archivo .mp3'''

    if not archivo_salida:
        archivo_salida = "audio.mp3"
    if ".mp3" not in archivo_salida:
        archivo_salida = archivo_salida + ".mp3"

    try:
        if texto:
            # Crear el objeto gTTS
            audio_espanol = gTTS(text=texto, lang= 'es',slow=False )

            # Guardar el resultado en un archivo .mp3
            audio_espano_guardado = audio_espanol.save(archivo_salida)
            print(f"El archivo de audio se guardó correctamente como {archivo_salida}")
            return audio_espano_guardado
    except Exception as e:
        print(f"Ocurrió un error al convetir el texto a voz {e}")
    


# Funciones para importar
if __name__ == "__main__":
        
        abrir_texto(archivo)
        validar_selector(selector)
        obtener_texto_de_url(url, selector = 'article h2, article p')
        procesar_texto_a_voz(texto)
        guardar_texto_a_voz(texto, archivo_salida)

    # Ejemplo de uso para este script

    #url = 'https://keepcoding.io/blog/que-es-pygame/'
    # Este selector se utiliza para obtener titulo y parrafos de un texto principal en una página web con etiqueta HTML
    # diferente a la de wikipedia.
    # #selector = 'article h2, article p'

    #url = 'https://es.wikipedia.org/wiki/Pygame'
    # Este selector puede servir para obtener la información principal de una página web con etiqueta HTML 'div.mw-parser-output p'
    # clase de la etiqueta mw-parser-output p
    # Ejemplo de página: Wikipedia
    #selector = 'div.mw-parser-output p'

    #texto = obtener_texto_de_url(url, selector)

