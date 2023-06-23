import os
from FuncionesValidaciones import *

## devuelve True si encuentra el elemento en el iterable
def esta_en(iterable: list ,buscado: str|int|float|dict|list|tuple) -> bool:
    vuelta = False
    for cosa in iterable:
        if cosa == buscado:
            vuelta = True
            break
    return vuelta

## itera una lista y la va agregando a un string si es una lista vacia devuelve un mensaje
def convertir_lista_a_string(lista:list,vacio:str = "no hay") -> str:
    ultimo_elemento = len(lista)
    if ultimo_elemento == 0:
        return vacio
    else:
        iteracion = 0
        for palabra in lista:
            iteracion +=1
            if iteracion == 1:
                string_largo = palabra
            elif iteracion == ultimo_elemento:
                string_largo = string_largo + " y " + palabra
            else:
                string_largo = string_largo + ", " + palabra
        return string_largo
    
## limpia consola
def limpiar_consola():
    os.system("cls")

## copia profunda de una lista de diccionarios o listas 
def copia_profunda(lista:list[dict]) -> list[dict]:
    nuevaLista = []
    for iterable in lista:
        nuevoIterable = iterable.copy()
        nuevaLista.append(nuevoIterable)
    return nuevaLista

## Ordena una lista de numeros de mayor a menor y devuelve una copia
def copia_ordenada_lista_dict(listaNumeros:list,modo:str = "DESC")->list:
    listaNumeros = listaNumeros.copy()
    largo = len(listaNumeros) 
    for i in range(0,largo):
        siguiente = i+1
        for j in range(siguiente,largo):
            if (listaNumeros[i] < listaNumeros[j] and modo == "DESC") or (listaNumeros[i] > listaNumeros[j] and modo == "ASC"):
                guardado = listaNumeros[i]
                listaNumeros[i] = listaNumeros[j]
                listaNumeros[j] = guardado
    return listaNumeros

#ordena una lista de diccionarios segun el valor de una categoria
def copia_ordenada_lista_dict(lista_dict:list[dict],cat:str,modo:str = "DESC")->list[dict]:
    lista_dict = copia_profunda(lista_dict)
    largo = len(lista_dict) 
    for i in range(0,largo):
        siguiente = i+1
        for j in range(siguiente,largo):
            valorDictI = (lista_dict[i])[cat]
            valorDictj = (lista_dict[j])[cat]
            if (valorDictI < valorDictj and modo == "DESC") or (valorDictI > valorDictj and modo == "ASC"):
                guardado = lista_dict[i]
                lista_dict[i] = lista_dict[j]
                lista_dict[j] = guardado
    return lista_dict

#en cada linea reemplaza la letra en esa posicion por el valor indicado
def reemplazar_indice_por_valor(string: str, i: int, valor: str) -> str:
    lineas = string.splitlines()
    lineas_modificadas = []
    for linea in lineas:
        if i < len(linea):
            copia = list(linea)
            copia[i] = valor
            linea_modificada = "".join(copia)
            lineas_modificadas.append(linea_modificada[i+1:])
        else:
            lineas_modificadas.append(linea)
    return "\n".join(lineas_modificadas)

##Copia una lista de dict y obtiene una categoria sin simbolo de pesos y normalizada 
def sacar_pesos_lista_dict(lista_diccionarios:list[dict],categoria:str) -> list[dict]:
    list = []
    for diccionario in lista_diccionarios:
        list.append(sacar_pesos_dict(diccionario,categoria))
    return list


#devuelve una lista con todos los contenidos posibles de los diccionarios dentro de una llave, sin repetir
def obtener_lista_contenidos_unicos_en_llave(lista_diccionarios:list[dict],categoria:str) -> list:
    todos_los_contenidos = map(lambda a: a[categoria],lista_diccionarios)
    lista_contenidos_unicos = list(set(todos_los_contenidos))
    return lista_contenidos_unicos

#devuelve una lista de diccionarios que tienen el valor indicado en la llave indicada
def obtener_lista_diccionarios_con_valor_especifico_en_llave(lista_diccionarios:list[dict],categoria:str,valor:str) -> list[dict]:
    lista_diccionarios = list((filter(lambda diccionario: diccionario[categoria] == valor,lista_diccionarios)))
    return lista_diccionarios

# recorre la lista de diccionarios y se fija si en la lista que hay dentro de una llave , esta el valor buscado, de ser asi, agrega el diccionario a la lista que devuelve
def obtener_lista_diccionarios_con_valor_en_su_lista(lista_dict:list[dict],categoria:str,valor:str) -> list[dict]:
    lista_filtrada = []
    for diccionario in lista_dict:
        if valor in diccionario[categoria]:
            lista_filtrada.append(diccionario)
    return lista_filtrada

#recorre una lista de diccionarios y si su categoria cumple con la regex lo deja pasar
def obtener_lista_diccionarios_con_categora_que_cumpla_regex(lista_dict:list[dict],categoria:str,regex:str) -> list[dict]:
    lista_diccionarios = list((filter(lambda diccionario: matchear_con_regex(regex,diccionario[categoria]),lista_dict)))
    return lista_diccionarios

#limpia la consola, imprime lo solicitado y devuelve el input que llega
def limpiar_consola_imprimir_y_pedir_input(imprime:str)-> str:
    limpiar_consola()
    recibe = input(imprime)
    return recibe

#splitea todos los diccionarios con el separador indicado en una categoria
def splitear_categoria(lista_dict:list[dict],categoria:str,separador:str) -> list[dict]:
    for diccionario in lista_dict:
        diccionario[categoria] = diccionario[categoria].split(separador)
    return lista_dict