import json
import os


#convierte un TXT a lista Strings
def convertir_txt_a_lista_strings(ruta:str,encodeado:str) -> list:
    with open(ruta,"r",encoding= encodeado) as archivo:
        contenido = archivo.read()
    lineas = contenido.split('\n')
    return lineas


#convierte el Csv a ListaDict
def convertir_csv_a_lista_dict(ruta:str,encodeado:str)-> list[dict]:
    with open(ruta,"r",encoding= encodeado) as archivo:
        contenido = archivo.read()
    lineas = contenido.split('\n')
    lista = []
    primera = True
    for linea in lineas:
        listaValores = linea.split(',')
        if primera:
            llaves = listaValores
            cantidadLlaves = len(llaves)
            primera = False
        else:
            diccionario = {}
            for i in range(0,cantidadLlaves):
                diccionario[llaves[i]] = listaValores[i]
            lista.append(diccionario)
    return lista

#guarda una lista dict como Csv en la ruta especificada
def guardar_lista_dict_como_csv(listaDict:list[dict],ruta:str) -> None:
    encabezado = ""
    for llave in listaDict[0]:
        encabezado = encabezado + str(llave) + ","
    encabezado = encabezado[:-1] # saca la coma
    ultima = len(listaDict)
    with open(ruta,"w",encoding='utf-8') as archivo:
        archivo.write(encabezado + '\n')
        iteracion = 0
        for dict in listaDict:
            iteracion += 1
            linea = ""
            for llave in dict:
                linea = linea + str(dict[llave]) + ","
            linea = linea[:-1]
            if iteracion != ultima:
                archivo.write(linea + '\n')
            else:
                archivo.write(linea)

#guarda una lista dict como Json en la ruta especificada
def guardar_lista_dict_como_json(listaDict:list[dict],ruta:str) -> None:
    with open(ruta,"w",encoding='utf-8') as archivo:
        json.dump(listaDict, archivo, indent=4,ensure_ascii=False)

#verificar que el archivo exista antes de intentar abrirlo
def verificar_existencia_archivo(ruta:str) -> bool:
    existe = True
    if not(os.path.exists(ruta)):
        existe = False
    return existe

#Recibe una ruta de Un json y devuelve una lista de diccionarios
def abrir_json_como_lista_dict(ruta:str) -> list[dict]:
    with open(ruta, 'r',encoding='utf-8') as archivo:
        listaDiccionarios = json.load(archivo)
    return listaDiccionarios

#guarda un string en un TXT
def guardar_string_como_txt(string:str,ruta:str) -> None:
    with open(ruta,"w",encoding='utf-8') as txt:
        txt.write(string)
