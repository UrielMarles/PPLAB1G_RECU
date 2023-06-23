from FuncionesGenerales import *
from FuncionesValidaciones import *
from FuncionesArchivos import *
from Graficos import *
from functools import reduce
import time
        



                 

            
def actualizar_lista() -> list[dict]: 
    lista_dict = convertir_csv_a_lista_dict("insumos.csv","utf-8")
    lista_dict_original = copia_profunda(lista_dict)
    lista_dict = splitear_categoria(lista_dict,"CARACTERISTICAS","|!*|")
    return lista_dict,lista_dict_original

def actualizar_lista_con_respuesta():
    lista_dict,lista_dict_original = actualizar_lista()
    limpiar_consola_imprimir_y_pedir_input(CARTEL+MENSAJE_LISTA_ACTUALIZADA)
    return lista_dict,lista_dict_original,True

def listar_cantidad_insumos_por_marca(lista_dict:list[dict]):
    imprimir = CARTEL + CABECERA_DOS
    diccionario_cantidades = {}
    for marca in obtener_lista_contenidos_unicos_en_llave(lista_dict,"MARCA"): # devuelve una lista con cada marca unica
        dicconarios_de_la_marca = obtener_lista_diccionarios_con_valor_especifico_en_llave(lista_dict,"MARCA",marca)
        cantidad_con_marca = len(dicconarios_de_la_marca)
        diccionario_cantidades[marca] = cantidad_con_marca
    for marca in diccionario_cantidades:
        imprimir += f"\n|{marca:^54}|{diccionario_cantidades[marca]:^54}|"
    imprimir += CIERRE_GENERICO
    limpiar_consola_imprimir_y_pedir_input(imprimir)

def listar_ordenados_por_marca_con_precio(lista_dict:list[dict]):
    imprimir = CARTEL + CABECERA_TRES
    for marca in obtener_lista_contenidos_unicos_en_llave(lista_dict,"MARCA"):
        imprimir += SEPARADOR_GENERICO
        diccionariosDeLaMarca = obtener_lista_diccionarios_con_valor_especifico_en_llave(lista_dict,"MARCA",marca) #devuelve la lista de diccionarios con esa marca
        for diccionario in diccionariosDeLaMarca:
            imprimir += f"\n|{marca:^25}|{diccionario['NOMBRE']:^57}|{diccionario['PRECIO']:^25}|"
    imprimir += CIERRE_GENERICO
    limpiar_consola_imprimir_y_pedir_input(imprimir) 

def buscar_insumos_con_caracteristica(lista_dict:list[dict]):
    lista_dict = sacar_pesos_lista_dict(lista_dict,"PRECIO")
    imprimir = CARTEL + CABECERA_CUATRO
    listaCaracteristicas = reduce(lambda lista,diccionario : lista + diccionario["CARACTERISTICAS"],lista_dict,[]) # obtiene una lista de todas las caracteristicas
    caracteristicasUnicas = set(listaCaracteristicas) 
    for caracteristica in caracteristicasUnicas: 
        imprimir += f"\n|{caracteristica:^109}|"
    imprimir += CIERRE_CUATRO
    caracteristica = limpiar_consola_imprimir_y_pedir_input(imprimir)
    while caracteristica != "atras" and not(caracteristica in list(caracteristicasUnicas)):
        limpiar_consola_imprimir_y_pedir_input(CARTEL+ERROR_CARACTERISTICA_INVALIDA)
        caracteristica = limpiar_consola_imprimir_y_pedir_input(imprimir)
    if caracteristica == "atras":
        return
    imprimir = CARTEL_GRANDE + CABECERA_CINCO
    lista_dict = poner_pesos_lista_dict(lista_dict,"PRECIO")
    diccionariosDeLaCaracteristica =  obtener_lista_diccionarios_con_valor_en_su_lista(lista_dict,"CARACTERISTICAS",caracteristica)
    for diccionario in diccionariosDeLaCaracteristica:
        imprimir += f"\n|{diccionario['ID']:^12}|{diccionario['MARCA']:^18}|{diccionario['PRECIO']:^22}|{diccionario['NOMBRE']:^56}|{caracteristica:^59}|"
    imprimir += CIERRE_CINCO
    limpiar_consola_imprimir_y_pedir_input(imprimir)

def listar_alfabeticamente_y_por_precio(lista_dict:list[dict]):
    lista_dict = sacar_pesos_lista_dict(lista_dict,"PRECIO")
    imprimir = CARTEL_GRANDE + CABECERA_CINCO
    marcas = obtener_lista_contenidos_unicos_en_llave(lista_dict,"MARCA")
    marcasOrdenadasAlfabeticamente = ordenar_lista_oraciones_alfabeticamente(marcas)
    for marca in marcasOrdenadasAlfabeticamente:
        imprimir += SEPARADOR_LARGO
        diccionariosDeLaMarca = obtener_lista_diccionarios_con_valor_especifico_en_llave(lista_dict,"MARCA",marca)
        diccionariosOrdenados = copia_ordenada_lista_dict(diccionariosDeLaMarca,"PRECIO","DESC")
        diccionariosOrdenadosConPesos = poner_pesos_lista_dict(diccionariosOrdenados,"PRECIO")
        for diccionario in diccionariosOrdenadosConPesos:
            imprimir += f"\n|{diccionario['ID']:^12}|{diccionario['MARCA']:^18}|{diccionario['PRECIO']:^22}|{diccionario['NOMBRE']:^56}|{(diccionario['CARACTERISTICAS'][0]):^59}|"
    imprimir += CIERRE_CINCO
    limpiar_consola_imprimir_y_pedir_input(imprimir)
    lista_dict = poner_pesos_lista_dict(lista_dict,"PRECIO")

def realizar_compra_de_uno_o_multiples_productos(lista_dict:list[dict],numero_ticket:int) -> int:
    carritoCompras = []
    agregarOtroProducto = "seguir"
    while agregarOtroProducto in ["seguir","descartar"]: #dentro de este bloque while se elige marca, producto y cantidad
        IdProductoElegido = "atras"
        while IdProductoElegido == "atras": # dentro de este bloque se obtiene marca y producto
            imprimir = CARTEL + PRIMER_CABECERA_SEIS
            marcas = obtener_lista_contenidos_unicos_en_llave(lista_dict, "MARCA")
            for marca in marcas:
                imprimir += f"\n|{marca:^109}|"
            imprimir += PRIMER_CIERRE_SEIS
            marcaElegida = limpiar_consola_imprimir_y_pedir_input(imprimir)
            while not(marcaElegida in marcas) and marcaElegida != "atras":
                limpiar_consola_imprimir_y_pedir_input(CARTEL + ERROR_MARCA_INVALIDA)
                marcaElegida = limpiar_consola_imprimir_y_pedir_input(imprimir) 
            if marcaElegida == "atras":
                break
            imprimir = CARTEL_GRANDE + CABECERA_CINCO                                                
            diccionariosDeLaMarca = obtener_lista_diccionarios_con_valor_especifico_en_llave(lista_dict, "MARCA", marcaElegida)
            for diccionario in diccionariosDeLaMarca:
                imprimir += f"\n|{diccionario['ID']:^12}|{diccionario['MARCA']:^18}|{diccionario['PRECIO']:^22}|{diccionario['NOMBRE']:^56}|{(diccionario['CARACTERISTICAS'][0]):^59}|"
            imprimir += SEGUNDO_CIERRE_SEIS
            idsDeLaMarca = obtener_lista_contenidos_unicos_en_llave(diccionariosDeLaMarca, "ID")
            IdProductoElegido = limpiar_consola_imprimir_y_pedir_input(imprimir)
            while not(IdProductoElegido in idsDeLaMarca) and IdProductoElegido != "atras":
                limpiar_consola_imprimir_y_pedir_input(CARTEL_GRANDE + ERROR_ID_PRODUCTO_INVALIDO)
                IdProductoElegido = limpiar_consola_imprimir_y_pedir_input(imprimir)
        if marcaElegida == "atras":
                break    
        # a partir de aca se elige la cantidad del producto, se calcula el subtotal
        diccionarioProductoElegido = (obtener_lista_diccionarios_con_valor_especifico_en_llave(lista_dict, "ID", IdProductoElegido))[0]
        diccionario = diccionarioProductoElegido.copy()
        imprimir =  CARTEL_GRANDE + CABECERA_CINCO + f"\n|{diccionario['ID']:^12}|{diccionario['MARCA']:^18}|{diccionario['PRECIO']:^22}|{diccionario['NOMBRE']:^56}|{(diccionario['CARACTERISTICAS'][0]):^59}|"
        imprimir += TERCER_CIERRE_SEIS
        cantidadProducto = limpiar_consola_imprimir_y_pedir_input(imprimir)
        while not(validar_entero_mayor_a_cero(cantidadProducto)):
            limpiar_consola_imprimir_y_pedir_input(CARTEL_GRANDE+ERROR_CANTIDAD_INVALIDA)
            cantidadProducto = limpiar_consola_imprimir_y_pedir_input(imprimir)
        diccionario["CANTIDAD"] = cantidadProducto
        sinPesos = sacar_pesos_dict(diccionario,"PRECIO")
        diccionario["SUBTOTAL"] = sinPesos["PRECIO"] * int(cantidadProducto)
        opciones = ["seguir","finalizar","descartar"]
        agregarOtroProducto = limpiar_consola_imprimir_y_pedir_input(CARTEL_GRANDE + CUARTO_CIERRE_SEIS)
        while not(agregarOtroProducto in opciones):
            agregarOtroProducto = limpiar_consola_imprimir_y_pedir_input(CARTEL_GRANDE + CUARTO_CIERRE_SEIS_ERROR)
        if agregarOtroProducto != "descartar":
            carritoCompras.append(diccionario)
    imprimir = CARTEL_GRANDE + SEGUNDA_CABECERA_SEIS
    total = 0
    for diccionario in carritoCompras:
        subtotalTruncado = "{:.2f}".format(diccionario["SUBTOTAL"])
        imprimir+= f"\n|{diccionario['ID']:^12}|{diccionario['MARCA']:^18}|{diccionario['PRECIO']:^22}|{diccionario['NOMBRE']:^56}|{diccionario['CANTIDAD']:^28}|{('$'+str(subtotalTruncado)):^30}|"
        imprimir+= SEPARADOR_LARGO
        total += diccionario["SUBTOTAL"]
    imprimir += SEPARADOR_TOTAL + f"\n|{('$'+str(total)):^171}|" + SEPARADOR_LARGO
    ticket = imprimir
    opciones = ["comprar","cancelar"]
    finalizar = limpiar_consola_imprimir_y_pedir_input(ticket+QUINTO_CIERRE_SEIS)
    while not(finalizar in opciones):
        finalizar = limpiar_consola_imprimir_y_pedir_input(ticket+QUINTO_CIERRE_SEIS_ERROR)
    if finalizar == "comprar":
        limpiar_consola_imprimir_y_pedir_input(ticket+SEXTO_CIERRE_SEIS)
        numero_ticket = numero_ticket + 1
        ruta = "ticket" + str(numero_ticket) + ".txt"
        guardar_string_como_txt(ticket,ruta)
    else:
        limpiar_consola_imprimir_y_pedir_input(ticket+SEPTIMO_CIERRE_SEIS)
    return numero_ticket

def guardar_insumos_json_disco_duro(lista_dict:list[dict]):
    regexDiscoDuro = r'\bDisco\s{1}Duro\b' # esta regex la uso para filtrar los nombres que contengan Disco Duro
    dictsCumplenRegex = obtener_lista_diccionarios_con_categora_que_cumpla_regex(lista_dict,"NOMBRE",regexDiscoDuro)
    guardar_lista_dict_como_json(dictsCumplenRegex,"discoDuro.json")
    limpiar_consola_imprimir_y_pedir_input(CARTEL+MENSAJE_SIETE_BIEN)

def listar_insumos_json(ruta:str):
    if verificar_existencia_archivo(ruta):
        listaOcho = abrir_json_como_lista_dict(ruta)
        imprimir = CARTEL_GRANDE + CABECERA_CINCO
        for diccionario in listaOcho:
            imprimir += f"\n|{diccionario['ID']:^12}|{diccionario['MARCA']:^18}|{diccionario['PRECIO']:^22}|{diccionario['NOMBRE']:^56}|{(diccionario['CARACTERISTICAS'][0]):^59}|"
        imprimir += CIERRE_CINCO
        limpiar_consola_imprimir_y_pedir_input(imprimir)
    else:
        limpiar_consola_imprimir_y_pedir_input(CARTEL+ERROR_OCHO_NO_CARGADO)

def aumentar_precios_y_guardar(lista_dict_original:list[dict]):
    originalSinPesos = sacar_pesos_lista_dict(lista_dict_original,"PRECIO")
    preciosAumentados = list(map(lambda diccionario: diccionario["PRECIO"]*1.084,originalSinPesos))
    largo = len(preciosAumentados)
    listaFinal = []
    for i in range(0,largo):
        diccionario = lista_dict_original[i]
        precioAumentado = preciosAumentados[i]
        precioAumentadoDosDecimales = "{:.2f}".format(precioAumentado)
        diccionario["PRECIO"] = precioAumentadoDosDecimales
        diccionario = poner_pesos_dict(diccionario,"PRECIO")
        listaFinal.append(diccionario)
    guardar_lista_dict_como_csv(listaFinal,"insumos.csv")
    limpiar_consola_imprimir_y_pedir_input(CARTEL+MENSAJE_NUEVE_BIEN)
    ##ACTUALIZAR LISTA DICT Y LISTA DICT ORIGINAL
    return actualizar_lista()

def ingresar_nuevo_producto(lista_dict_original:list[dict],lista_dict:list[dict]) -> list[dict]:
    imprimir = CARTEL + PRIMER_CABECERA_SEIS
    listaMarcas = convertir_txt_a_lista_strings("marcas.txt","utf-8")
    for marca in listaMarcas:
        imprimir += f"\n|{marca:^109}|"  
    imprimir += PRIMER_CIERRE_ONCE
    marcaElegida = limpiar_consola_imprimir_y_pedir_input(imprimir)   
    while not(marcaElegida in listaMarcas) and marcaElegida != "atras":
        limpiar_consola_imprimir_y_pedir_input(CARTEL + ERROR_MARCA_INVALIDA)
        marcaElegida = limpiar_consola_imprimir_y_pedir_input(imprimir)
    if marcaElegida != "atras":
        todosLosId = list(map(lambda a: a["ID"],lista_dict))
        idElegido = len(todosLosId) + 1
        imprimir = CARTEL + TERCER_CABECERA_ONCE
        seguir = "no"
        while seguir != "si":
            nombre = limpiar_consola_imprimir_y_pedir_input(imprimir)
            seguir = limpiar_consola_imprimir_y_pedir_input(CARTEL +"\n el nombre elegido es: " + nombre+ " estas seguro que quieres ese nombre para el producto? \n para confirmar ingresa 'si'")
        imprimir = CARTEL + CUARTA_CABECERA_ONCE
        precio = limpiar_consola_imprimir_y_pedir_input(imprimir)
        esFloat = validar_string_float(precio)
        while not(esFloat):
            limpiar_consola_imprimir_y_pedir_input(CARTEL+ERROR_PRECIO)
            precio = limpiar_consola_imprimir_y_pedir_input(imprimir)
            esFloat = validar_string_float(precio)
        caracteristicas = limpiar_consola_imprimir_y_pedir_input(CARTEL + QUINTA_CABECERA_ONCE)
        seguir = limpiar_consola_imprimir_y_pedir_input(CARTEL + SEXTA_CABECERA_ONCE)
        cantidad = 1
        while seguir == "si" and cantidad <= 3:
            cantidad += 1
            nueva = limpiar_consola_imprimir_y_pedir_input(CARTEL+QUINTA_CABECERA_ONCE)
            caracteristicas = caracteristicas + "|!*|" +nueva
            seguir = limpiar_consola_imprimir_y_pedir_input (CARTEL +SEXTA_CABECERA_ONCE)
        nuevoDict = {}
        nuevoDict["ID"] = idElegido
        nuevoDict["NOMBRE"] = nombre
        nuevoDict["MARCA"] = marcaElegida
        nuevoDict["PRECIO"] = "$" + precio
        nuevoDict["CARACTERISTICAS"] = caracteristicas
        lista_dict_original.append(nuevoDict)
        lista_dict = copia_profunda(lista_dict_original)
        lista_dict = splitear_categoria(lista_dict,"CARACTERISTICAS","|!*|")
        guardar_lista_dict_como_csv(lista_dict_original,"insumos.csv")    
    return actualizar_lista()

def exportar_datos_de_forma_elegida(lista_dict_original:list[dict]):
    imprimir = CARTEL + PRIMER_CABECERA_ONCE
    formato = limpiar_consola_imprimir_y_pedir_input(imprimir)
    while not(formato in [".csv",".json"]):
        limpiar_consola_imprimir_y_pedir_input(CARTEL+ERROR_FORMATO)
        formato = limpiar_consola_imprimir_y_pedir_input(imprimir)
    correcto = "no"
    while correcto != "si":
        nombre = limpiar_consola_imprimir_y_pedir_input(CARTEL +SEGUNDA_CABECERA_ONCE)
        correcto = limpiar_consola_imprimir_y_pedir_input(CARTEL +"\n el nombre elegido es: " + nombre+ "estas seguro que quieres ese nombre para el archivo? \n para confirmar ingresa 'si'")
    if formato == ".csv":
        guardar_lista_dict_como_csv(lista_dict_original,(nombre+formato))
    else:
        guardar_lista_dict_como_json(lista_dict_original,(nombre+formato))

def salir_y_saludar(mensaje:str):
        salir = limpiar_consola_imprimir_y_pedir_input(CARTEL+MENSAJE_DIEZ_CONFIRMAR)
        if salir == "si":
            saludo = mensaje
            limpiar_consola()
            print(saludo)
            time.sleep(1)
            for i in range(0,115):
                limpiar_consola()
                saludo = reemplazar_indice_por_valor(saludo,0," ")
                print(saludo)
                time.sleep(0.05)
            return False
        return True
    
def main() -> None:
    numero_ticket = 0
    seguir = True
    actualizada = False
    saltear = True
    while seguir:
        numero = limpiar_consola_imprimir_y_pedir_input(CARTEL+MENSAJE_DEFAULT+MENU)
        match numero:
            case "1":
                lista_dict,lista_dict_original,actualizada = actualizar_lista_con_respuesta()
            case "2": #Lista todas las marcas 
                if actualizada:
                    listar_cantidad_insumos_por_marca(lista_dict)
            case "3":
                if actualizada:
                    listar_ordenados_por_marca_con_precio(lista_dict)
            case "4":
                if actualizada:
                    buscar_insumos_con_caracteristica(lista_dict)
            case "5":
                if actualizada:
                    listar_alfabeticamente_y_por_precio(lista_dict)
            case "6":
                if actualizada:
                    numero_ticket = realizar_compra_de_uno_o_multiples_productos(lista_dict,numero_ticket)
            case "7":
                if actualizada:
                    guardar_insumos_json_disco_duro(lista_dict)
            case "8":
                if actualizada:
                    listar_insumos_json("discoDuro.json")
            case "9":
                if actualizada:
                    lista_dict,lista_dict_original = aumentar_precios_y_guardar(lista_dict_original)
            case "10":
                if actualizada:
                    lista_dict,lista_dict_original = ingresar_nuevo_producto(lista_dict_original,lista_dict)
            case "11":
                if actualizada:
                    exportar_datos_de_forma_elegida(lista_dict_original)
            case "12":
                if actualizada:
                    seguir = salir_y_saludar(DESPEDIDA)
            case _:
                limpiar_consola_imprimir_y_pedir_input(CARTEL+ERROR_NUMERO_INVALIDO)
                saltear = False
        if not(actualizada) and saltear:
            limpiar_consola_imprimir_y_pedir_input(CARTEL+ERROR_LISTA_DESACTUALIZADA)
        saltear = True
            
                

