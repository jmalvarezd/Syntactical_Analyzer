import sys
import math

##LETRA = -1
##NUMERO = -2
##CODIGO = ""
##
##tk_mas = 0 
##tk_menos = 1 
##tk_mult = 2 
##tk_div = 3 
##tk_mod = 4 
##tk_asig = 5 
##tk_menor = 6 
##tk_mayor = 7 
##tk_menor_igual = 8 
##tk_mayor_igual = 9 
##tk_igual = 10
##tk_y = 11
##tk_o = 12
##tk_dif = 13
##tk_neg = 14
##tk_dosp = 15
##tk_pyc = 16
##tk_coma = 17
##tk_punto = 18
##tk_par_izq = 19
##tk_par_der = 20
##tk_id = 21
##tk_entero = 22
##tk_real = 23
##tk_caracter = 24
##tk_cadena = 25
##funcion_principal = 26
##fin_principal = 27
##leer = 28
##imprimir = 29
##booleano = 30
##caracter = 31
##entero =  32
##real = 33
##cadena = 34
##si = 35
##entonces = 36
##fin_si = 37
##si_no = 38
##mientras = 39
##hacer = 40
##fin_mientras = 41
##para = 42
##fin_para = 43
##seleccionar = 44
##entre = 45
##caso = 46
##romper = 47
##defecto = 48
##fin_seleccionar = 49
##estructura = 50
##fin_estructura = 51
##funcion = 52
##fin_funcion = 53
##retornar = 54
##falso = 55
##verdadero = 56
##EOF = 57

traduccion_tk = ["+",
				"-",
				"*",
				"/",
				"%",
				"=",
				"<",
				">",
				"<=",
				">=",
				"==",
				"&&",
				"||",
				"!=",
				"!",
				":",
				";",
				",",
				".",
				"(",
				")",
				"identificador",
				"valor_entero",
				"valor_real",
				"valor_caracter",
				"valor_cadena",
				"funcion_principal",
				"fin_principal",
				"leer",
				"imprimir",				
				"booleano",
				"caracter",
				"entero",
				"real",
				"cadena",
				"si",
				"entonces",
				"fin_si",
				"si_no",
				"mientras",
				"hacer",
				"fin_mientras",
				"para",
				"fin_para",
				"seleccionar",
				"entre",
				"caso",
				"romper",
				"defecto",
				"fin_seleccionar",
				"estructura",
				"fin_estructura",
				"funcion",
				"fin_funcion",
				"retornar",				
				"falso",
				"verdadero",
				"EOF"]

keywords = [
  "and", "constantes", "hasta", "matriz", "paso", "registro", "sino", "vector", "archivo",
  "desde", "inicio", "mientras", "subrutina", "repetir", "tipos", "caso", "eval", "lib",
  "not", "programa", "retorna", "var", "const", "fin", "libext", "or", "ref", "si", "variables",
  "numerico", "cadena", "logico", "funcion_principal", "fin_principal",
  
  "dim", "imprimir", "cls", "leer", "set_ifs", "abs", "arctan", "ascii", "cos", "dec",
  "eof", "exp", "get_ifs", "inc", "int", "log", "lower", "mem", "ord", "paramval",
  "pcount", "pos", "random", "sec", "set_stdin", "set_stdout", "sin", "sqrt",
  "str", "strdup", "strlen", "substr", "tan", "upper", "val",
  
  "SI", "NO", "TRUE", "FALSE", 
]
column = 0
row = 0
startingTokenColumn = 0
startingTokenRow = 0
allTokens = []
lines = None
word = ""
throwError = False
errorCol = 0
errorRow = 0
escape = False



class Token:
    ttk = -1
    l = -1
    c = -1
    lexema = ""
    def __init__ (self, _ttk,_c,_l,_lexema = None):
        self.ttk = _ttk
        self.l = _l
        self.c = _c
        self.lexema = _lexema

    def __str__(self):
        if self.lexema == None:
            return (str("<" + str(self.ttk) + "," + str(self.l) + "," + str(self.c) +  ">"))        
        else:
            return (str("<"+ str(self.ttk) + ","+str(self.lexema)+ "," + str(self.l) + "," + str(self.c) + ">"))
          


def skipToNextLine():
    global column, row
    column = -1 ##Tiene que ser -1 para que la siguiente llamada lo haga 0 (TENER CUIDADO)
    row += 1

def isAlphaOrUnderscoreOrNi(stringToCheck):
    return stringToCheck.isalpha() or stringToCheck == "_" or stringToCheck == "ñ" or stringToCheck == "Ñ"

def isAlnumOrUnderscoreOrNi(stringToCheck):
    return stringToCheck.isalnum() or stringToCheck == "_" or stringToCheck == "ñ" or stringToCheck == "Ñ"

def obtenerCaracterSiguiente():
    global column, row, lines
    if not lines:
        with open("test.txt","r", encoding="utf-8") as f:
            lines = f.readlines()
            return lines[0][0]
    column += 1
    if len(lines[row]) <= column:
        column = 0
        row += 1
        if len(lines) <= row:
            return None
    return lines[row][column]

def noAvanzar():
    global column, row,lines
    if(column == 0):
        row = row - 1
        column = len(lines[row])-1
    else:
        column = column-1
 


first_error = True
def error_sintactico(Lista):
  global _token, first_error
  if (first_error):
    first_error = False
    aux = ""
    if(Lista[0] == "funcion_principal" and token() == EOF):
      print("Error sintactico: falta funcion_principal")
    else:
      for l in Lista[:-1]:
        aux += "\"" + str(l) + "\", "
      print(Lista[-1] )
      if type(Lista[-1]) == str:
        aux += "\"" + str(Lista[-1]) + "\""
      else:
        aux += "\"" + Lista[-1].lexema + "\""
      if _token.lexema is not None:
        traduccion = _token.lexema
      else:
        traduccion = _token.ttk
      print( "<" + str(_token.l) + "," + str(_token.c) + "> Error sintactico: se encontro: \"" + traduccion + "\"; se esperaba: " + aux + ".")

def token():
        if(_token == None):
                return None
        return _token.ttk

def emparejar(tk):
	global _token
	if token() == tk:
		_token = nextToken()
	else:
		error_sintactico([tk])
	#print(_token.to_str()) ### PARA DEBUG
		
i = -1

def delta(estadoActual, caracterLeido):
    global allTokens, column, row, escape, startingTokenColumn, startingTokenRow, word, throwError, errorCol, errorRow
    
    if(estadoActual == 0): ##Ningun Token actualmente en lectura
        startingTokenColumn = column
        startingTokenRow = row

        if(caracterLeido == None):
            return -1
        if(caracterLeido.lower() == "á" or caracterLeido.lower() == "é" or caracterLeido.lower() == "í" or caracterLeido.lower() == "ó" or caracterLeido.lower() == "ú"):
            throwError = True
            errorCol = startingTokenColumn
            errorRow = startingTokenRow
            return -1
        elif(caracterLeido == "/"):
            return 1
        elif(caracterLeido == "\\"):
            return 3
        
        ##3 maneras de hacer una cadena
        elif(caracterLeido == "\""): 
            word = "\""
            return 4
        elif(caracterLeido == "'"): 
            word = "'"
            return 5
        elif(caracterLeido == "“"):
            word = "“"
            return 6
        ##
        #numeros
        elif(caracterLeido.isdecimal()):
            word = caracterLeido
            return 7
        ##ids y palabras reservadas
        
        elif(isAlphaOrUnderscoreOrNi(caracterLeido)):
            word = caracterLeido
            return 9

        elif(caracterLeido == "<"):
            word = caracterLeido
            return 10
        elif(caracterLeido == ">"):
            word = caracterLeido
            return 11

        elif(caracterLeido == "="):
            word = caracterLeido
            return 12
        
        ##Triviales
        ##TODO: Estos dos primeros no son realmente triviales, 5+3 son 3 tokens, +3 es un token
        elif(caracterLeido == "+"):
            allTokens.append(Token("tk_suma",startingTokenColumn+1,startingTokenRow+1,"+"))
            return 0
        elif(caracterLeido == "-"):
            allTokens.append(Token("tk_resta",startingTokenColumn+1,startingTokenRow+1))
            return 0
        ##
        elif(caracterLeido == "*"):
            allTokens.append(Token("tk_mult",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "^"):
            allTokens.append(Token("tk_exp",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "%"):
            allTokens.append(Token("tk_mod",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "{"):
            allTokens.append(Token("tk_llave_izq",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "}"):
            allTokens.append(Token("tk_llave_der",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "("):
            allTokens.append(Token("tk_par_izq",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == ")"):
            allTokens.append(Token("tk_par_der",startingTokenColumn+1,startingTokenRow+1,")"))
            return 0
        elif(caracterLeido == "["):
            allTokens.append(Token("tk_brac_izq",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "]"):
            allTokens.append(Token("tk_brac_der",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == ":"):
            allTokens.append(Token("tk_dospuntos",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == ";"):
            allTokens.append(Token("tk_pyq",startingTokenColumn+1,startingTokenRow+1,";"))
            return 0
        elif(caracterLeido == ","):
            allTokens.append(Token("tk_coma",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "."):
            allTokens.append(Token("tk_punto",startingTokenColumn+1,startingTokenRow+1))
            return 0
        ##End Triviales

        elif(caracterLeido == " " or caracterLeido == "\n" or caracterLeido == "\t"):
            return 0
        else:
            # print(caracterLeido)
            throwError = True
            errorCol = startingTokenColumn
            errorRow = startingTokenRow
            return -1
        
    if(estadoActual == 1): #El anterior fue un /
        if(caracterLeido == "/"): # //
            skipToNextLine()
            return 0
        elif(caracterLeido == "*"): # /*
            return 2
        else: # / (division)
            noAvanzar() ##Tuvimos que leer un caracter de mas para saber que era este, nos "regresamos" 1 caracter
            allTokens.append(Token("tk_division",startingTokenColumn+1,startingTokenRow+1))
            return 0
            
    if(estadoActual == 2): #Anteriores fueron /*
        if(caracterLeido == "*"):
            return 3
        else: return 2
        
    if(estadoActual == 3): #Anteriores /* y *
        if(caracterLeido == "/"):
            return 0
        else:
            return 2 ##Si el * no estaba seguido de /
        
    if(estadoActual == 4): #Inicio de Cadena Anterior "
        if(caracterLeido == None):
          throwError = True
          errorCol = startingTokenColumn
          errorRow = startingTokenRow
          return -1
        if(caracterLeido == "\"" and not escape):#Fin de cadena "
            word = word + "\""
            allTokens.append(Token("tk_cadena",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido == "\\" ):
            escape = True
            word = word + caracterLeido
            return 4
        if(caracterLeido == "\n"):
            escape = False
            word = word + "\\n"
            return 4
        else: #Continuacion de cadena
            escape = False
            word = word + caracterLeido
            return 4
        
    if(estadoActual == 5): #Inicio de Cadena Anterior '
        if(caracterLeido == None):
            throwError = True
            errorCol = startingTokenColumn
            errorRow = startingTokenRow
            return -1
        if(caracterLeido == "'" and not escape):#Fin de cadena '
            word = word + "'"
            allTokens.append(Token("tk_cadena",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido == "\\" ):
            escape = True
            word = word + caracterLeido
            return 5
        if(caracterLeido == "\n"):
            escape = False
            word = word + "\\n"
            return 5
        else: #Continuacion de cadena
            escape = False
            word = word + caracterLeido
            return 5
        
    if(estadoActual == 6): #Inicio de Cadena Anterior “
        if(caracterLeido == None):
            throwError = True
            errorCol = startingTokenColumn
            errorRow = startingTokenRow
            return -1
        if(caracterLeido == "”" and not escape):#Fin de cadena ”
            word = word + "”"
            allTokens.append(Token("tk_cadena",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido == "\\" ):
            escape = True
            word = word + caracterLeido
            return 6
        if(caracterLeido == "\n"):
            escape = False
            word = word + "\\n"
            return 6
        else: #Continuacion de cadena
            escape = False
            word = word + caracterLeido
            return 6
        
    if(estadoActual == 7): # Inicio de Numero
        if(caracterLeido == None):
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        elif(caracterLeido.isdecimal()):
            word = word + caracterLeido
            return 7
        elif(caracterLeido == "."): #Numero Decimal
            return 8
        elif(caracterLeido == 'e' or caracterLeido == 'E'):
            word = word + caracterLeido
            return 14
        else:
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
            
    if(estadoActual == 8):# Inicio numero con punto decimal
        if(caracterLeido == None):
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            allTokens.append(Token("tk_punto",column+1,row+1))
            return 0
        elif(caracterLeido.isdecimal()):
            word = word + "."
            word = word + caracterLeido
            return 13
        else:
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            allTokens.append(Token("tk_punto",column+1,row+1))
            return 0
        
    if(estadoActual == 9): # Inicio identificador o palabra reservada
        if(caracterLeido == None):
            if word in keywords:
                allTokens.append(Token(word,startingTokenColumn+1,startingTokenRow+1))
                return 0
            else:
                allTokens.append(Token("tk_id",startingTokenColumn+1,startingTokenRow+1, word))
                return 0
        if(len(word) > 32):
            noAvanzar()
            allTokens.append(Token("tk_id",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido.lower() == "á" or caracterLeido.lower() == "é" or caracterLeido.lower() == "í" or caracterLeido.lower() == "ó" or caracterLeido.lower() == "ú"):
            throwError = True
            errorCol = startingTokenColumn
            errorRow = startingTokenRow
            return -1
        if(isAlnumOrUnderscoreOrNi(caracterLeido)):
            word = word + caracterLeido
            return 9
        else:
            noAvanzar()
            if word in keywords:
                allTokens.append(Token(word,startingTokenColumn+1,startingTokenRow+1))
                return 0
            else:
                allTokens.append(Token("tk_id",startingTokenColumn+1,startingTokenRow+1, word))
                return 0
            
    if(estadoActual == 10): #Anterior fue <
        if(caracterLeido == ">"):
            allTokens.append(Token("tk_distinto",startingTokenColumn+1,startingTokenRow+1))
            return 0
        elif(caracterLeido == "="):
            allTokens.append(Token("tk_menorigual",startingTokenColumn+1,startingTokenRow+1))
            return 0
        else:
            noAvanzar()
            allTokens.append(Token("tk_menor",startingTokenColumn+1,startingTokenRow+1))
            return 0
        
    if(estadoActual == 11): #Anterior fue <
        if(caracterLeido == "="):
            allTokens.append(Token("tk_mayorigual",startingTokenColumn+1,startingTokenRow+1))
            return 0
        else:
            noAvanzar()
            allTokens.append(Token("tk_mayor",startingTokenColumn+1,startingTokenRow+1))
            return 0
    if(estadoActual == 12):
        if(caracterLeido == "="):
            allTokens.append(Token("tk_igualdad",startingTokenColumn+1,startingTokenRow+1))
            return 0
        else:
            noAvanzar()
            allTokens.append(Token("tk_asig",startingTokenColumn+1,startingTokenRow+1))
            return 0
        
    if(estadoActual == 13):# Continuacion numero con punto decimal
        if(caracterLeido == None):
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido.isdecimal()):
            word = word+caracterLeido
            return 13
        elif(caracterLeido == 'e' or caracterLeido == 'E'):
            word = word + caracterLeido
            return 14
        else:
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
    if(estadoActual == 14): #Notacion cientifica
        if(caracterLeido == None):
            throwError = True
            errorCol = startingTokenColumn
            errorRow = startingTokenRow
            return -1
        if(caracterLeido == '+' or caracterLeido == '-'):
            word = word + caracterLeido
            return 14
        elif(caracterLeido.isdecimal()):
            word = word+caracterLeido
            return 15
        throwError = True
        errorCol = startingTokenColumn
        errorRow = startingTokenRow
        return -1
    if(estadoActual == 15): # Despues del e+/-num
        if(caracterLeido == None):
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        if(caracterLeido.isdecimal()):
            word = word + caracterLeido
            return 15
        else:
            noAvanzar()
            allTokens.append(Token("tk_num",startingTokenColumn+1,startingTokenRow+1, word))
            return 0
        
def nextToken():
        global i,allTokens
        i = i+1
        if(i>=len(allTokens)):
                return None
        return allTokens[i]

### INICIO CODIGO GENERADO

ListObject_esperados = ['identificador', 'inicio', 'const', 'var', 'tipos']
Assignation_esperados = ['identificador']
OtherExpression_esperados = ['+', '-', '*', '/', '%', '<', '>', '<=', '>=', '==', '!=', '(', ')', 'identificador', 'valor_entero', 'valor_cadena', ']', 'fin', 'inicio', 'const', 'var', 'tipos', 'TRUE', 'FALSE', 'and', 'or']
AssignationVar_esperados = ['identificador']
Constant_esperados = ['identificador', 'valor_entero', 'valor_cadena', 'TRUE', 'FALSE']
Operador_esperados = ['+', '-', '*', '/', '%', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']
OtherObject_esperados = ['identificador', 'registro', 'numerico', 'cadena', 'logico', 'vector']
Object_esperados = ['identificador']
Settings_esperados = ['inicio', 'const', 'var', 'tipos']
ListDeclarations_esperados = ['identificador', 'inicio', 'const', 'var', 'tipos', '{']
SettingsVar_esperados = ['var']
Body_esperados = ['identificador', 'fin']
Tipo_esperados = ['identificador', 'numerico', 'cadena', 'logico', 'vector']
Sentence_esperados = ['identificador']
ListAssignations_esperados = ['identificador', 'inicio', 'const', 'var', 'tipos']
ListExpression_esperados = ['-', '(', ')', 'identificador', 'valor_entero', 'valor_cadena', 'TRUE', 'FALSE']
TipoVector_esperados = ['-', '*', '(', 'identificador', 'valor_entero', 'valor_cadena', 'TRUE', 'FALSE']
CallToFunction_esperados = ['identificador']
ListId_esperados = ['=', ',']
Expression_esperados = ['-', '(', 'identificador', 'valor_entero', 'valor_cadena', 'TRUE', 'FALSE']
AssignationConst_esperados = ['identificador']
SettingsConst_esperados = ['const']
S_esperados = ['inicio', 'const', 'var', 'tipos']
SettingsTypes_esperados = ['tipos']
AssignationTypes_esperados = ['identificador']
Declaration_esperados = ['identificador']

def ListObject():
        global ListObject_esperados
        if(token() == "tk_id" ):
                Object()
                ListObject()
                return
        elif(token() == "const" or token() == "var" or token() == "inicio" or token() == "tipos" ):
                return
        else:
                error_sintactico(ListObject_esperados)
def Assignation():
        global Assignation_esperados
        if(token() == "tk_id" ):
                emparejar("tk_id")
                ListId()
                emparejar("tk_asig")
                Expression()
                return
        else:
                error_sintactico(Assignation_esperados)
def OtherExpression():
        global OtherExpression_esperados
        if(token() == "tk_mayorigual" or token() == "tk_mult" or token() == "tk_menor" or token() == "tk_suma" or token() == "tk_mayor" or token() == "tk_mod" or token() == "tk_resta" or token() == "or" or token() == "and" or token() == "tk_division" or token() == "tk_menorigual" or token() == "tk_igualdad" or token() == "tk_distinto" ):
                Operador()
                Expression()
                return
        elif(token() == "inicio" or token() == "tk_cadena" or token() == "tk_num" or token() == "var" or token() == "const" or token() == "fin" or token() == "tipos" or token() == "tk_resta" or token() == "tk_par_izq" or token() == "TRUE" or token() == "tk_brac_der" or token() == "tk_id" or token() == "tk_par_der" or token() == "FALSE" ):
                return
        else:
                error_sintactico(OtherExpression_esperados)
def AssignationVar():
        global AssignationVar_esperados
        if(token() == "tk_id" ):
                Declaration()
                ListDeclarations()
                return
        else:
                error_sintactico(AssignationVar_esperados)
def Constant():
        global Constant_esperados
        if(token() == "tk_num" ):
                emparejar("tk_num")
                return
        elif(token() == "tk_cadena" ):
                emparejar("tk_cadena")
                return
        elif(token() == "tk_id" ):
                emparejar("tk_id")
                return
        elif(token() == "TRUE" ):
                emparejar("TRUE")
                return
        elif(token() == "FALSE" ):
                emparejar("FALSE")
                return
        else:
                error_sintactico(Constant_esperados)
def Operador():
        global Operador_esperados
        if(token() == "tk_suma" ):
                emparejar("tk_suma")
                return
        elif(token() == "tk_resta" ):
                emparejar("tk_resta")
                return
        elif(token() == "tk_mult" ):
                emparejar("tk_mult")
                return
        elif(token() == "tk_division" ):
                emparejar("tk_division")
                return
        elif(token() == "tk_mod" ):
                emparejar("tk_mod")
                return
        elif(token() == "tk_igualdad" ):
                emparejar("tk_igualdad")
                return
        elif(token() == "tk_distinto" ):
                emparejar("tk_distinto")
                return
        elif(token() == "tk_mayor" ):
                emparejar("tk_mayor")
                return
        elif(token() == "tk_mayorigual" ):
                emparejar("tk_mayorigual")
                return
        elif(token() == "tk_menor" ):
                emparejar("tk_menor")
                return
        elif(token() == "tk_menorigual" ):
                emparejar("tk_menorigual")
                return
        elif(token() == "and" ):
                emparejar("and")
                return
        elif(token() == "or" ):
                emparejar("or")
                return
        else:
                error_sintactico(Operador_esperados)
def OtherObject():
        global OtherObject_esperados
        if(token() == "tk_id" or token() == "vector" or token() == "logico" or token() == "numerico" or token() == "cadena" ):
                Tipo()
                return
        elif(token() == "registro" ):
                emparejar("registro")
                emparejar("tk_llave_izq")
                AssignationVar()
                emparejar("tk_llave_der")
                return
        else:
                error_sintactico(OtherObject_esperados)
def Object():
        global Object_esperados
        if(token() == "tk_id" ):
                emparejar("tk_id")
                emparejar("tk_dospuntos")
                OtherObject()
                return
        else:
                error_sintactico(Object_esperados)
def Settings():
        global Settings_esperados
        if(token() == "const" ):
                SettingsConst()
                Settings()
                return
        elif(token() == "tipos" ):
                SettingsTypes()
                Settings()
                return
        elif(token() == "var" ):
                SettingsVar()
                Settings()
                return
        elif(token() == "inicio" ):
                return
        else:
                error_sintactico(Settings_esperados)
def ListDeclarations():
        global ListDeclarations_esperados
        if(token() == "tk_id" ):
                Declaration()
                ListDeclarations()
                return
        elif(token() == "tk_llave_der" or token() == "inicio" or token() == "var" or token() == "const" or token() == "tipos" ):
                return
        else:
                error_sintactico(ListDeclarations_esperados)
def SettingsVar():
        global SettingsVar_esperados
        if(token() == "var" ):
                emparejar("var")
                AssignationVar()
                return
        else:
                error_sintactico(SettingsVar_esperados)
def Body():
        global Body_esperados
        if(token() == "fin" ):
                return
        elif(token() == "tk_id" ):
                Sentence()
                return
        else:
                error_sintactico(Body_esperados)
def Tipo():
        global Tipo_esperados
        if(token() == "numerico" ):
                emparejar("numerico")
                return
        elif(token() == "cadena" ):
                emparejar("cadena")
                return
        elif(token() == "vector" ):
                emparejar("vector")
                emparejar("tk_brac_izq")
                TipoVector()
                emparejar("tk_brac_der")
                Tipo()
                return
        elif(token() == "logico" ):
                emparejar("logico")
                return
        elif(token() == "tk_id" ):
                emparejar("tk_id")
                return
        else:
                error_sintactico(Tipo_esperados)
def Sentence():
        global Sentence_esperados
        if(token() == "tk_id" ):
                Assignation()
                return
        elif(token() == "tk_id" ):
                Declaration()
                return
        elif(token() == "tk_id" ):
                CallToFunction()
                return
        else:
                error_sintactico(Sentence_esperados)
def ListAssignations():
        global ListAssignations_esperados
        if(token() == "tk_id" ):
                Assignation()
                ListAssignations()
                return
        elif(token() == "const" or token() == "var" or token() == "inicio" or token() == "tipos" ):
                return
        else:
                error_sintactico(ListAssignations_esperados)
def ListExpression():
        global ListExpression_esperados
        if(token() == "tk_cadena" or token() == "tk_num" or token() == "tk_id" or token() == "tk_resta" or token() == "FALSE" or token() == "tk_par_izq" or token() == "TRUE" ):
                Expression()
                ListExpression()
                return
        elif(token() == "tk_par_der" ):
                return
        else:
                error_sintactico(ListExpression_esperados)
def TipoVector():
        global TipoVector_esperados
        if(token() == "tk_cadena" or token() == "tk_num" or token() == "tk_id" or token() == "tk_resta" or token() == "FALSE" or token() == "tk_par_izq" or token() == "TRUE" ):
                Expression()
                return
        elif(token() == "tk_mult" ):
                emparejar("tk_mult")
                return
        else:
                error_sintactico(TipoVector_esperados)
def CallToFunction():
        global CallToFunction_esperados
        if(token() == "tk_id" ):
                emparejar("tk_id")
                emparejar("tk_par_izq")
                ListExpression()
                emparejar("tk_par_der")
                return
        else:
                error_sintactico(CallToFunction_esperados)
def ListId():
        global ListId_esperados
        if(token() == "tk_coma" ):
                emparejar("tk_coma")
                emparejar("tk_id")
                ListId()
                return
        elif(token() == "tk_asig" ):
                return
        else:
                error_sintactico(ListId_esperados)
def Expression():
        global Expression_esperados
        if(token() == "tk_resta" ):
                emparejar("tk_resta")
                Expression()
                return
        elif(token() == "tk_par_izq" ):
                emparejar("tk_par_izq")
                Expression()
                emparejar("tk_par_der")
                OtherExpression()
                return
        elif(token() == "tk_cadena" or token() == "tk_num" or token() == "tk_id" or token() == "FALSE" or token() == "TRUE" ):
                Constant()
                OtherExpression()
                return
        else:
                error_sintactico(Expression_esperados)
def AssignationConst():
        global AssignationConst_esperados
        if(token() == "tk_id" ):
                Assignation()
                ListAssignations()
                return
        else:
                error_sintactico(AssignationConst_esperados)
def SettingsConst():
        global SettingsConst_esperados
        if(token() == "const" ):
                emparejar("const")
                AssignationConst()
                return
        else:
                error_sintactico(SettingsConst_esperados)
def S():
        global S_esperados
        if(token() == "tipos" or token() == "var" or token() == "inicio" or token() == "const" ):
                Settings()
                emparejar("inicio")
                Body()
                emparejar("fin")
                return
        else:
                error_sintactico(S_esperados)
def SettingsTypes():
        global SettingsTypes_esperados
        if(token() == "tipos" ):
                emparejar("tipos")
                AssignationTypes()
                return
        else:
                error_sintactico(SettingsTypes_esperados)
def AssignationTypes():
        global AssignationTypes_esperados
        if(token() == "tk_id" ):
                Object()
                ListObject()
                return
        else:
                error_sintactico(AssignationTypes_esperados)
def Declaration():
        global Declaration_esperados
        if(token() == "tk_id" ):
                emparejar("tk_id")
                emparejar("tk_dospuntos")
                Tipo()
                return
        else:
                error_sintactico(Declaration_esperados)



### FIN CODIGO GENERADO

A1 = "funcion_principal\n entero a = jul(24,sd.x) + 5 \nfin_principal" # SIN ERROR SINTACTICO
A2 = "funcion_principal\n  \n imprimir(3+5)\n\nfin_principal" # ERROR SINTACTICO

B2 = "estructura C\n    entero a;\nfin_estructura\n\nestructura Point\n    entero x;\n    entero y;\n    real a,b,c;\n    C c;\nfin_estructura\n\nfuncion_principal\n   \n    Point p,s = (hola) - 1;\n    S1.x = hola;\n\n    hola(palar,sds,1);\n\n	para ( entero i = 0 ; i < a ; 1 ) hacer\n        imprimir(i);\n    fin_para\n\n    para ( j = 0 ; i < a || j  < 100  ; p ) hacer\n        imprimir(j);\n    fin_para\n\n    seleccionar ( a ) entre\n        caso 0 :\n            imprimir(a);\n            romper;\n        caso 1:\n            imprimir(a*2);\n            romper;\n        defecto:\n    fin_seleccionar\n\n    seleccionar ( a ) entre\n        defecto:\n    fin_seleccionar\n\n    seleccionar ( a ) entre\n        caso 0 :\n            imprimir(a);\n    fin_seleccionar\n\n    hacer\n        a = a/2;\n    mientras( a > 0 );\n\n    si ( (a < 5) && (a>10) ) entonces\n        imprimir(a);\n    si_no\n        imprimir(a-1);\n    fin_si\n\n    si ( a < 5 && a>0 ) entonces\n        imprimir(a);\n   	fin_si\n\n\n    Point s1 = p.y;\n    Point s2 = 'c' + (id - p.c.a + 58 + (hola) - !(estoesFalso)) * func(24,p.c,otrafun())+ !funbool();\n\nfin_principal"
B3 = "funcion_principal\n\n    imprimir \n    ( 10+5);\nfin_principal"
"""
B2 -- Lo que hasta ahora acepta la gramatica
estructura C
    entero a;
fin_estructura

estructura Point
    entero x;
    entero y;
    real a,b,c;
    C c;
fin_estructura

funcion_principal
   
    Point p,s = (hola) - 1;
    Point s1 = p.y;
    Point s2 = 'c' + (id - p.c.a + 58 + (hola) - !(estoesFalso)) * func(24,p.c,otrafun())+ !funbool();

fin_principal

"""

# Entrada para test
# aux = input()
# while (aux != 'ñ'):
# 	CODIGO = CODIGO + aux + '\n'
# 	aux = input()



#for line in sys.stdin: # La que se supone funcionaria en el juez
#   CODIGO += line
c = obtenerCaracterSiguiente()
estado = 0
while (estado != -1):
        estado = delta(estado,c)
        if(c == None):
                break
        c = obtenerCaracterSiguiente()
if(throwError):
        print(">>> Error lexico(linea:"+str(errorRow+1)+",posicion:"+str(errorCol+1)+")")
        
_token = nextToken()
#print(_token.to_str()) ### PARA DEBUG
S()
if(token() is not None or not first_error):
	error_sintactico(["EOF"])
else:
	print("El analisis sintactico ha finalizado exitosamente.")

