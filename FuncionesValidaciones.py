import re

## Recibe una expresion Regular y una string y se fija si la string cumple la regex
def matchear_con_regex(condicion:str,string:str) -> bool:
    valido = False
    if re.match(condicion,string):
        valido = True
    return valido

# Devuelve True si recibe un string que contiene un entero mayor a cero
def validar_entero_mayor_a_cero(string:str)-> bool:
    condicion = r'^[1-9]\d*$'
    return matchear_con_regex(condicion,string)

## devuelve True si la string que recibe tiene unicamente letras o espacios
def validar_string_alfanumerica(string:str)-> bool:
    condicion = r'^[A-Za-z\s]+$'
    return matchear_con_regex(condicion,string)
    
## devuelve true si el string que recibe tiene unicamente numeros del 0 al 9 y un posible signo de menos
def validar_string_int(string:str) -> bool:
    condicion = r'^-?\d+$'
    return matchear_con_regex(condicion,string)

## devuelve true si el string que recibe tiene unicamente numeros, una coma, y un posible menos
def validar_string_float(string:str) -> bool:
    condicion = r'^-?\d*\.\d+$'
    return matchear_con_regex(condicion,string)

## devuelve true si el string que recibe tiene unicamente numeros, maximo una coma y maximo un menos
def validar_string_numerica(string:str) -> bool:
    condicion = r'^-?\d+(\.\d+)?$'
    return matchear_con_regex(condicion,string)

##Identifica si una string contiene un Int o un Float y en caso de ser asi devuelve la string convertida
def normalizar_numeros_en_strings(string:str)-> str|int|float:
    devuelve = string
    if validar_string_int(string):
        devuelve = int(string)
    if validar_string_float(string):
        devuelve = float(string)
    return devuelve

##normaliza el contenido de cada llave de cada diccionario en una lista
def normalizar_numeros_list_dict(lista_dict:list[dict])->list[dict]:
    for dict in lista_dict:
        for llave in dict:
            dict[llave] = normalizar_numeros_en_strings(dict[llave])
    return lista_dict

#saca todos los acentos y vuelve minuscula letras
def sacar_acentos_y_minuscula(letra:str) -> str:
    devuelve = letra.lower()
    VOCALES = ["a","e","i","o","u"]
    ACENTOS = ["á","é","í","ó","ú"]
    if devuelve in ACENTOS:
        indice = ACENTOS.index(devuelve)
        devuelve = VOCALES[indice]
    return devuelve

#Saca los acentos de todas las letras de una oracion y la vuelve minuscula
def sacar_acentos_oracion(oracion:str) -> str:
    devuelve = ""
    for letra in oracion:
        devuelve += sacar_acentos_y_minuscula(letra)
    return devuelve

#convierte strings de letras o espacio a su posicion en el alfabeto, el espacio seria un 0 y el guion un 25
def convertir_oracion_a_posicion_alfabetica(string:str) ->list:
    sin_acentos = sacar_acentos_oracion(string)
    posiciones = []
    LISTA_LETRAS = [" ","a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z","-"]
    for letra in sin_acentos:
        posiciones.append(LISTA_LETRAS.index(letra))
    return posiciones


## esta funcion sirve para comparar listas de numeros y una vez que encuentra un numero en la misma posicion de ambas que es diferente nos devuelve la lista que tiene el numero mayor o menor segun le indiquemos, en caso de empate devuelve la lista mas corta
def comparar_listas_numero_a_numero(lista1:list,lista2:list,modo:str = "menor") -> list:
    largoL1 = len(lista1)
    largoL2 = len(lista2)
    masCorta = lista2
    lenCorto = len(lista2)
    if largoL1 < largoL2:
        masCorta = lista1
        lenCorto = len(lista1)
    for i in range(0,lenCorto):
        if (lista1[i] < lista2[i] and modo == "menor") or (lista1[i] > lista2[i] and modo == "mayor"):
            return lista1
        if (lista2[i] < lista1[i] and modo == "menor") or (lista2[i] > lista1[i] and modo == "mayor"):
            return lista2
    return masCorta

#compara dos oraciones y devuelve la que este antes alfabeticamente, el espacio se considera antes del 0 y dos oraciones que terminan estando empatadas devuelve la oracion mas corta
def comparar_oraciones_alfabeticamente(string1:str,string2:str,modo:str = "menor") -> str:
    lista1 = convertir_oracion_a_posicion_alfabetica(string1)
    lista2 = convertir_oracion_a_posicion_alfabetica(string2)
    return comparar_listas_numero_a_numero(lista1,lista2,modo)


#ordena todas las palabras en una lista de strings que contengan unicamente letras, espacios, o guiones, alfabeticamente
def ordenar_lista_oraciones_alfabeticamente(lista:list,modo:str = "menor") -> list:
    listaOraciones = lista.copy()
    largo = len(listaOraciones) 
    for i in range(0,largo):
        siguiente = i+1
        for j in range(siguiente,largo):
            if (comparar_oraciones_alfabeticamente(listaOraciones[i],listaOraciones[j],modo) == convertir_oracion_a_posicion_alfabetica(listaOraciones[j]) ):
                guardado = listaOraciones[i]
                listaOraciones[i] = listaOraciones[j]
                listaOraciones[j] = guardado
    return listaOraciones

#saca el simbolo de pesos de una categoria y la convierte en numero ya sea int o float
def sacar_pesos_dict(diccionario:dict,categoria:str) -> dict:
    diccionario = diccionario.copy()
    diccionario[categoria] = diccionario[categoria].replace("$","")
    diccionario[categoria] = normalizar_numeros_en_strings(diccionario[categoria])
    return diccionario

#agrega el simbolo de pesos a una categoria y la convierte en string
def poner_pesos_dict(diccionario:dict,categoria:str) -> dict:
    diccionario = diccionario.copy()
    diccionario[categoria] = "$" +str(diccionario[categoria])
    return diccionario

#copia una lista de dict y devuelve la copia con el simbolo de pesos en esa categoria
def poner_pesos_lista_dict(lista_diccionarios:list[dict],categoria:str) -> list[dict]:
    list = []
    for diccionario in lista_diccionarios:
        list.append(poner_pesos_dict(diccionario,categoria))
    return list
