import re
import pymongo
import nltk #Procesar lenguaje natural
from nltk.tokenize import word_tokenize #Tokenizar texto
from nltk.corpus import stopwords #Cargar stopwords
from collections import Counter # Contar palbras repetidas
from collections import OrderedDict # Ordenar el conteo de palabras repetdias


palabras_enlace = []
texto_enlace = ''


def conectar_dbms():
    #Referencia a mongoDB
    cliente_mongo = pymongo.MongoClient("mongodb://localhost:27017/")
    #Crear la base de datos
    base_datos = cliente_mongo["motor-db"]
    #Crear la colección
    coleccion = base_datos["motor"]
    return coleccion

def leer_primer_enlace(coleccion):
    try:
        query = { "revisado": False }
        documento = coleccion.find(query).limit(1)
    except Error as e:
        print("Error al conectarse a MongoDB: ", e)
    return documento

def establecer_palabras_repetidas (coleccion, url, palabra1, ranking1, palabra2, ranking2, palabra3, ranking3, contenido):
    try:
        doc = coleccion.find_one_and_update(
            {"_id" : url},
            {"$set":{
                "palabra1": palabra1, 
                "ranking1": ranking1, 
                "palabra2": palabra2, 
                "ranking2": ranking2,
                "palabra3": palabra3, 
                "ranking3": ranking3,
                "contenido": contenido
            }},
            upsert=True
)

    except Error as e:
        print("Error al conectarse a MongoDB")
    
    except OSError as p: 
        print("Error al acutalizar")
    
    return


def obtener_enlaces(coleccion, enlace_actual):
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    url = urlopen(enlace_actual)
    print("\nExtraer los enlaces de la página Web: ", enlace_actual)
    bs = BeautifulSoup(url.read(), 'html.parser')

    for titulos in bs.find_all("h1"):
        texto_limpio = re.sub(r'<.*?>', '', str(titulos)) #Eliminar etiquetas HTML
        texto_limpio=texto_limpio.replace("\n", "")
        texto_limpio=texto_limpio.replace("\t", "")
        texto_limpio = texto_limpio.strip()
        palabras_enlace.append(texto_limpio)

    for titulos in bs.find_all("h2"):
        texto_limpio = re.sub(r'<.*?>', '', str(titulos)) #Eliminar etiquetas HTML
        texto_limpio=texto_limpio.replace("\n", "")
        texto_limpio=texto_limpio.replace("\t", "")
        texto_limpio = texto_limpio.strip()
        palabras_enlace.append(texto_limpio)

    for textos in bs.find_all("p"):
        texto_limpio = re.sub(r'<.*?>', '', str(textos)) #Eliminar etiquetas HTML
        texto_limpio=texto_limpio.replace("\n", "")
        texto_limpio=texto_limpio.replace("\t", "")
        texto_limpio = texto_limpio.strip()
        palabras_enlace.append(texto_limpio)
    
    #Unir todo el texto del enlace
    texto_enlace = " ".join(palabras_enlace)

    #Pasar texto a mínusculas
    texto_minusculas=str.lower(texto_enlace)

    #Eliminar caracteres especiales usando expreciones regulares
    texto_sin_simbolos = re.sub(r'[^\w\s]','', texto_minusculas)

    #Convertir el texto a tokens
    tokens_de_mi_texto = word_tokenize(texto_sin_simbolos)
    
    #Cargar stopwords del español
    palabras_vacias = set(stopwords.words('spanish'))

    lista_final=[]

    #Eliminando stopwords
    for palabra in tokens_de_mi_texto:
        if palabra not in palabras_vacias:
            lista_final.append(palabra)
    
    #print(lista_final)
    #Contar y ordenar palabras repetidas
    contador=Counter(lista_final)

    #Contar las palabras repetidas
    contador_ordenado = OrderedDict(contador)

    #Extraer las palabras más repetidas de todo el texto
    las_mas_repetidas=OrderedDict(contador.most_common((3)))

    lista_repetidas=[]

    for key, value in las_mas_repetidas.items():
        print(key, value)
        lista_repetidas.append(key)
        lista_repetidas.append(value)

    #Establecer palabras y rankings en la base de datos
    establecer_palabras_repetidas(coleccion, enlace_actual, lista_repetidas[0], lista_repetidas[1], lista_repetidas[2], lista_repetidas[3], lista_repetidas[4], lista_repetidas[5], texto_enlace[0:256])


    enlaces_encontrados = []
    
    contador = 0
    for enlaces in bs.find_all("a"):
        enlace = format(enlaces.get("href"))
        if  enlace[-3:]!="jpg" and enlace[-3:]!="png" and enlace[-3:]!="svg" and enlace[-3:]!="pdf" and enlace[-3:]!="ppt" and enlace[-4:]!="pptx" and enlace[-3:]!="txt" and enlace[-3:]!="xls" and enlace[-4:]!="docx" and enlace[-3:]!="doc"  and enlace[-4:]!="xlsx" and enlace[-3:]!="wmv" and enlace[-3:]!="mp3" and enlace[-3:]!="mp4" and enlace[-3:]!="avi":
            if enlace.startswith("http") or enlace.startswith("https"):
                enlaces_encontrados.append("{}".format(enlaces.get("href")))
        contador = contador + 1
    #print("{}".format(enlaces.get("href")))
    print("\nEnlaces encontrados: ", contador)

    palabras_enlace.clear()
    texto_enlace = ''
    lista_final.clear()
    las_mas_repetidas.clear()
    lista_repetidas.clear()
    return enlaces_encontrados


def almacenar_enlaces(coleccion, enlaces_encontrados):
    try:
        for enlace in enlaces_encontrados:
            #Verificar si el registro ya existe
            item_count = coleccion.count_documents({"_id": enlace})
            #Si el documento no existe, lo registramos
            if item_count < 1:
                print("Creando nuevo documento...")
                data = { 
                        "_id": enlace, 
                        "url": enlace,
                        "revisado": False, 
                        "palabra1": "",
                        "ranking1": 0,
                        "palabra2": "",
                        "ranking2": 0,
                        "palabra3": "",
                        "ranking3": 0,
                        "contenido": "" 
                }
                x = coleccion.insert_one(data)
            else:
                print("El documento ya existe")
    except Error as e:
        print("Error al conectarse a MongoDB: ", e)
    return
    

def marcar_enlace_revisado (coleccion, enlace_a_marcar):
    try:
        doc = coleccion.find_one_and_update(
            {"_id" : enlace_a_marcar},
            {"$set":{"revisado": True}},
            upsert=True
)

    except Error as e:
        print("Error al conectarse a MySQL")
    
    except OSError as p: 
        print("Se encontró un enlace repetido")
    
    return



mi_coleccion = conectar_dbms()
for x in range(1):
    primer_enlace = leer_primer_enlace(mi_coleccion)
    for datos_enlace in primer_enlace:
        enlaces_encontrados=obtener_enlaces(mi_coleccion, datos_enlace['_id'])
        almacenar_enlaces(mi_coleccion, enlaces_encontrados)
        marcar_enlace_revisado(mi_coleccion, datos_enlace['_id'])

