from FuncionesValidaciones import validar_string_numerica
from FuncionesValidaciones import validar_string_alfanumerica
from FuncionesValidaciones import normalizar_numeros_en_strings
from FuncionesGenerales import esta_en

## verifica que un entero o float este en un rango y devuelve el entero o float
def pedir_numero_en_rango(mensaje:str = "ingrese un numero: ",min:int|float = None,max:int|float = None, error:str = "no ingresaste un numero que cumpla con las ocondiciones") -> int|float: 
        while True:
            try:
                numero = input(mensaje)
                if not(validar_string_numerica(numero)):
                       raise ValueError
                numero = normalizar_numeros_en_strings(numero) ##me convierte la string en Int o Float
                if min != None:
                    if numero < min:
                        raise  ValueError
                if max != None:
                    if numero > max:
                        raise ValueError
                break
            except ValueError:
                print(error)
        return numero

## pregunta si quiere seguir y devuelve True o False
def pedir_si_no(mensaje:str ="ingrese si quiere seguir si o no: ") -> bool :
    seguir = ""
    valid = True
    while valid:
        seguir = input(mensaje)
        seguir = seguir.upper()
        valid = not(esta_en(["SI","NO"],seguir))
    boolean = (seguir == "SI")
    return boolean


##imprime mensaje hasta obtener string alfaNumerica
def pedir_string_alfanumerica(mensaje:str = "ingrese una string alfanumerica")->str: 
    string = ""
    while not(validar_string_alfanumerica(string)):
        string = input(mensaje)
    return string

## imprime un mensaje pidiendo una string hasta que la string este en la lista diccionario o tupla
def pedir_string_en(iterable:list|dict|tuple,mensaje:str ="Ingrese una string valida entre las opciones") -> str:
    string = ""
    while not(esta_en(iterable,string)):
        string = input(mensaje)
    return string