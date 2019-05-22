import sys
import math

keywords = [
  "and", "constantes", "hasta", "matriz", "paso", "registro", "sino", "vector", "archivo",
  "desde", "inicio", "mientras", "subrutina", "repetir", "tipos", "caso", "eval", "lib",
  "not", "programa", "retorna", "var", "const", "fin", "libext", "or", "ref", "si", "variables",
  "numerico", "cadena", "logico", "funcion_principal", "fin_principal",
  
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
    if(Lista[0] == "funcion_principal" and token() == "EOF"):
      print("Error sintactico: falta funcion_principal")
    else:
      for l in Lista[:-1]:
        aux += "\"" + str(l) + "\", "
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

FunctionDeclaration_esperados = ['identificador']
ListDeclarations_esperados = ['identificador', 'inicio', 'const', 'var', 'tipos', '{']
BodyCase_esperados = ['caso']
ListOfSentencesHasSentence_esperados = [';', 'identificador', 'si', 'sino', 'mientras', 'caso', 'fin', '{', 'eval', 'repetir', 'hasta', 'desde']
Sentence_esperados = ['identificador', 'si', 'mientras', 'eval', 'repetir', 'desde']
FunctionDeclarationParamsNotEmpty_esperados = [',', ')']
AssignationTypes_esperados = ['identificador']
CallToFunction_esperados = ['identificador']
OptionalReturn_esperados = ['inicio', 'const', 'var', 'tipos', 'retorna']
Declaration_esperados = ['identificador']
ListTipoVector_esperados = [',', ']']
SettingsVar_esperados = ['var']
BodyIfSentence_esperados = ['identificador', 'si', 'sino', 'mientras', '{', 'eval', 'repetir', 'desde']
BodyIfElseCase_esperados = ['sino', '{']
Operador_esperados = ['+', '-', '*', '/', '%', '<', '>', '<=', '>=', '==', '!=', '^', 'and', 'or']
S_esperados = ['inicio', 'const', 'var', 'tipos']
SentenceStartsWithId_esperados = ['=', ',', '(', '[']
SettingsTypes_esperados = ['tipos']
LoopSentence_esperados = ['desde']
BodyCase2_esperados = ['sino', 'caso', '{']
IfSentenceStart_esperados = ['si']
FunctionParams_esperados = ['-', '(', ')', 'identificador', 'valor_numerico', 'valor_cadena', 'TRUE', 'FALSE', '}']
AssignationSeenId_esperados = ['=', ',', '[']
DoWhileSentence_esperados = ['repetir']
ConstantSeenId_esperados = ['+', '-', '*', '/', '%', '=', '<', '>', '<=', '>=', '==', '!=', ':', ';', ',', '.', '(', ')', '^', 'identificador', 'valor_numerico', 'valor_cadena', 'si', 'sino', 'mientras', 'caso', '[', ']', 'fin', 'inicio', 'const', 'var', 'tipos', 'TRUE', 'FALSE', '{', '}', 'and', 'or', 'eval', 'repetir', 'hasta', 'desde']
Expression_esperados = ['-', '(', 'identificador', 'valor_numerico', 'valor_cadena', 'TRUE', 'FALSE', '}']
WhileSentence_esperados = ['mientras']
Assignation_esperados = ['-', '(', 'identificador', 'valor_numerico', 'valor_cadena', 'TRUE', 'FALSE', '}']
Subrutine_esperados = ['subrutina']
Object_esperados = ['identificador']
IfElseSentence_esperados = ['sino', '{']
AssignationVar_esperados = ['identificador']
ListId_esperados = ['=', ':', ',']
SettingsConst_esperados = ['const']
ListObject_esperados = ['identificador', 'inicio', 'const', 'var', 'tipos']
Tipo_esperados = ['identificador', 'registro', 'numerico', 'cadena', 'logico', 'vector', 'matriz']
CallToFunctionSeenId_esperados = ['(']
OtherExpression_esperados = ['+', '-', '*', '/', '%', '=', '<', '>', '<=', '>=', '==', '!=', ':', ';', ',', '(', ')', '^', 'identificador', 'valor_numerico', 'valor_cadena', 'si', 'sino', 'mientras', 'caso', '[', ']', 'fin', 'inicio', 'const', 'var', 'tipos', 'TRUE', 'FALSE', '{', '}', 'and', 'or', 'eval', 'repetir', 'hasta', 'desde']
LoopStep_esperados = ['identificador', 'valor_numerico', 'valor_cadena', 'TRUE', 'FALSE']
EvalSentence_esperados = ['eval']
Constant_esperados = ['identificador', 'valor_numerico', 'valor_cadena', 'TRUE', 'FALSE']
FunctionParamsNotEmpty_esperados = [',', ')']
BodyWhile_esperados = ['identificador', 'si', 'mientras', '{', 'eval', 'repetir', 'hasta', 'desde']
AssignationConst_esperados = ['-', '(', 'identificador', 'valor_numerico', 'valor_cadena', 'TRUE', 'FALSE', '}']
TipoVector_esperados = ['-', '*', '(', 'identificador', 'valor_numerico', 'valor_cadena', 'TRUE', 'FALSE', '}']
ListSubrutine_esperados = ['EOF', 'subrutina']
Body_esperados = ['identificador', 'si', 'mientras', 'eval', 'repetir', 'desde']
Settings_esperados = ['inicio', 'const', 'var', 'tipos']
SubrutineStart_esperados = ['subrutina']
ListOfSentences_esperados = ['identificador', 'si', 'sino', 'mientras', 'caso', 'fin', '{', 'eval', 'repetir', 'hasta', 'desde']
ListExpressionNotEmpty_esperados = [',', '{']
ListAssignations_esperados = ['-', '(', 'identificador', 'valor_numerico', 'valor_cadena', 'inicio', 'const', 'var', 'tipos', 'TRUE', 'FALSE', '}']
FunctionDeclarationParams_esperados = [')', 'identificador']
ListExpression_esperados = ['-', '(', 'identificador', 'valor_numerico', 'valor_cadena', 'TRUE', 'FALSE', '{', '}']
BodyEvalSentence_esperados = ['caso']
IfSentence_esperados = ['-', '(', 'identificador', 'valor_numerico', 'valor_cadena', 'TRUE', 'FALSE', '}']

def FunctionDeclaration():
        global FunctionDeclaration_esperados
        if(token() == "tk_id" ):
                emparejar("tk_id")
                emparejar("tk_par_izq")
                FunctionDeclarationParams()
                emparejar("tk_par_der")
                return
        else:
                error_sintactico(FunctionDeclaration_esperados)
def ListDeclarations():
        global ListDeclarations_esperados
        if(token() == "tk_id" ):
                Declaration()
                ListDeclarations()
                return
        elif(token() == "tk_llave_der" or token() == "var" or token() == "inicio" or token() == "const" or token() == "tipos" ):
                return
        else:
                error_sintactico(ListDeclarations_esperados)
def BodyCase():
        global BodyCase_esperados
        if(token() == "caso" ):
                emparejar("caso")
                emparejar("tk_par_izq")
                Expression()
                emparejar("tk_par_der")
                Body()
                BodyCase2()
                return
        else:
                error_sintactico(BodyCase_esperados)
def ListOfSentencesHasSentence():
        global ListOfSentencesHasSentence_esperados
        if(token() == "tk_pyq" ):
                emparejar("tk_pyq")
                ListOfSentences()
                return
        elif(token() == "tk_id" or token() == "repetir" or token() == "sino" or token() == "hasta" or token() == "tk_llave_der" or token() == "si" or token() == "eval" or token() == "fin" or token() == "desde" or token() == "caso" or token() == "mientras" ):
                ListOfSentences()
                return
        else:
                error_sintactico(ListOfSentencesHasSentence_esperados)
def Sentence():
        global Sentence_esperados
        if(token() == "tk_id" ):
                emparejar("tk_id")
                SentenceStartsWithId()
                return
        elif(token() == "si" ):
                IfSentenceStart()
                return
        elif(token() == "mientras" ):
                WhileSentence()
                return
        elif(token() == "repetir" ):
                DoWhileSentence()
                return
        elif(token() == "eval" ):
                EvalSentence()
                return
        elif(token() == "desde" ):
                LoopSentence()
                return
        else:
                error_sintactico(Sentence_esperados)
def FunctionDeclarationParamsNotEmpty():
        global FunctionDeclarationParamsNotEmpty_esperados
        if(token() == "tk_coma" ):
                emparejar("tk_coma")
                Declaration()
                FunctionDeclarationParamsNotEmpty()
                return
        elif(token() == "tk_par_der" ):
                return
        else:
                error_sintactico(FunctionDeclarationParamsNotEmpty_esperados)
def AssignationTypes():
        global AssignationTypes_esperados
        if(token() == "tk_id" ):
                Object()
                ListObject()
                return
        else:
                error_sintactico(AssignationTypes_esperados)
def CallToFunction():
        global CallToFunction_esperados
        if(token() == "tk_id" ):
                emparejar("tk_id")
                CallToFunctionSeenId()
                return
        else:
                error_sintactico(CallToFunction_esperados)
def OptionalReturn():
        global OptionalReturn_esperados
        if(token() == "retorna" ):
                emparejar("retorna")
                Tipo()
                return
        elif(token() == "inicio" or token() == "const" or token() == "tipos" or token() == "var" ):
                return
        else:
                error_sintactico(OptionalReturn_esperados)
def Declaration():
        global Declaration_esperados
        if(token() == "tk_id" ):
                emparejar("tk_id")
                ListId()
                emparejar("tk_dospuntos")
                Tipo()
                return
        else:
                error_sintactico(Declaration_esperados)
def ListTipoVector():
        global ListTipoVector_esperados
        if(token() == "tk_brac_der" ):
                return
        elif(token() == "tk_coma" ):
                emparejar("tk_coma")
                TipoVector()
                return
        else:
                error_sintactico(ListTipoVector_esperados)
def SettingsVar():
        global SettingsVar_esperados
        if(token() == "var" ):
                emparejar("var")
                AssignationVar()
                return
        else:
                error_sintactico(SettingsVar_esperados)
def BodyIfSentence():
        global BodyIfSentence_esperados
        if(token() == "tk_id" or token() == "repetir" or token() == "si" or token() == "eval" or token() == "desde" or token() == "mientras" ):
                Body()
                BodyIfSentence()
                return
        elif(token() == "tk_llave_der" or token() == "sino" ):
                return
        else:
                error_sintactico(BodyIfSentence_esperados)
def BodyIfElseCase():
        global BodyIfElseCase_esperados
        if(token() == "tk_llave_der" ):
                return
        elif(token() == "sino" ):
                emparejar("sino")
                Body()
                return
        else:
                error_sintactico(BodyIfElseCase_esperados)
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
        elif(token() == "tk_exp" ):
                emparejar("tk_exp")
                return
        else:
                error_sintactico(Operador_esperados)
def S():
        global S_esperados
        if(token() == "inicio" or token() == "const" or token() == "tipos" or token() == "var" ):
                Settings()
                emparejar("inicio")
                Body()
                emparejar("fin")
                ListSubrutine()
                return
        else:
                error_sintactico(S_esperados)
def SentenceStartsWithId():
        global SentenceStartsWithId_esperados
        if(token() == "tk_coma" or token() == "tk_brac_izq" or token() == "tk_asig" ):
                AssignationSeenId()
                return
        elif(token() == "tk_par_izq" ):
                CallToFunctionSeenId()
                return
        else:
                error_sintactico(SentenceStartsWithId_esperados)
def SettingsTypes():
        global SettingsTypes_esperados
        if(token() == "tipos" ):
                emparejar("tipos")
                AssignationTypes()
                return
        else:
                error_sintactico(SettingsTypes_esperados)
def LoopSentence():
        global LoopSentence_esperados
        if(token() == "desde" ):
                emparejar("desde")
                Assignation()
                emparejar("hasta")
                LoopStep()
                emparejar("tk_llave_izq")
                Body()
                emparejar("tk_llave_der")
                return
        else:
                error_sintactico(LoopSentence_esperados)
def BodyCase2():
        global BodyCase2_esperados
        if(token() == "caso" ):
                emparejar("caso")
                emparejar("tk_par_izq")
                Expression()
                emparejar("tk_par_der")
                Body()
                BodyCase2()
                return
        elif(token() == "tk_llave_der" or token() == "sino" ):
                return
        else:
                error_sintactico(BodyCase2_esperados)
def IfSentenceStart():
        global IfSentenceStart_esperados
        if(token() == "si" ):
                emparejar("si")
                emparejar("tk_par_izq")
                Expression()
                emparejar("tk_par_der")
                IfSentence()
                return
        else:
                error_sintactico(IfSentenceStart_esperados)
def FunctionParams():
        global FunctionParams_esperados
        if(token() == "tk_par_der" ):
                return
        elif(token() == "tk_llave_izq" or token() == "tk_id" or token() == "FALSE" or token() == "tk_cadena" or token() == "TRUE" or token() == "tk_resta" or token() == "tk_num" or token() == "tk_par_izq" ):
                Expression()
                FunctionParamsNotEmpty()
                return
        else:
                error_sintactico(FunctionParams_esperados)
def AssignationSeenId():
        global AssignationSeenId_esperados
        if(token() == "tk_coma" or token() == "tk_asig" ):
                ListId()
                emparejar("tk_asig")
                Expression()
                return
        elif(token() == "tk_brac_izq" ):
                emparejar("tk_brac_izq")
                Expression()
                emparejar("tk_brac_der")
                ListId()
                emparejar("tk_asig")
                Expression()
                return
        else:
                error_sintactico(AssignationSeenId_esperados)
def DoWhileSentence():
        global DoWhileSentence_esperados
        if(token() == "repetir" ):
                emparejar("repetir")
                BodyWhile()
                emparejar("hasta")
                emparejar("tk_par_izq")
                Expression()
                emparejar("tk_par_der")
                return
        else:
                error_sintactico(DoWhileSentence_esperados)
def ConstantSeenId():
        global ConstantSeenId_esperados
        if(token() == "tk_par_izq" ):
                CallToFunctionSeenId()
                return
        elif(token() == "tk_punto" ):
                emparejar("tk_punto")
                Constant()
                return
        elif(token() == "tk_exp" or token() == "si" or token() == "eval" or token() == "tk_mayorigual" or token() == "const" or token() == "tk_llave_izq" or token() == "tk_coma" or token() == "FALSE" or token() == "tk_mayor" or token() == "tk_cadena" or token() == "tk_resta" or token() == "tk_num" or token()
== "tk_brac_der" or token() == "fin" or token() == "desde" or token() == "repetir" or token() == "tk_pyq" or token() == "tk_mod" or token() == "TRUE" or token() == "tk_igualdad" or token() == "sino" or token() == "tk_dospuntos" or token() == "tk_distinto" or token() == "tk_llave_der" or token() == "var" or token() == "tk_suma" or token() == "mientras" or token() == "and" or token() == "tk_par_der" or token() == "tk_menor" or token() == "tk_division" or token() == "tk_par_izq" or token() == "tipos" or token() == "hasta" or token() == "inicio" or token() == "tk_brac_izq" or token() == "caso" or token() == "tk_mult" or token() == "tk_id" or token() == "tk_menorigual" or token() == "tk_asig" or token() == "or" ):
                return
        else:
                error_sintactico(ConstantSeenId_esperados)
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
                return
        elif(token() == "tk_llave_izq" ):
                emparejar("tk_llave_izq")
                ListExpression()
                emparejar("tk_llave_der")
                return
        elif(token() == "tk_id" or token() == "FALSE" or token() == "TRUE" or token() == "tk_num" or token() == "tk_cadena" ):
                Constant()
                OtherExpression()
                return
        else:
                error_sintactico(Expression_esperados)
def WhileSentence():
        global WhileSentence_esperados
        if(token() == "mientras" ):
                emparejar("mientras")
                emparejar("tk_par_izq")
                Expression()
                emparejar("tk_par_der")
                emparejar("tk_llave_izq")
                BodyWhile()
                emparejar("tk_llave_der")
                return
        else:
                error_sintactico(WhileSentence_esperados)
def Assignation():
        global Assignation_esperados
        if(token() == "tk_llave_izq" or token() == "tk_id" or token() == "FALSE" or token() == "tk_cadena" or token() == "TRUE" or token() == "tk_resta" or token() == "tk_num" or token() == "tk_par_izq" ):
                Expression()
                ListId()
                emparejar("tk_asig")
                Expression()
                return
        else:
                error_sintactico(Assignation_esperados)
def Subrutine():
        global Subrutine_esperados
        if(token() == "subrutina" ):
                SubrutineStart()
                S()
                return
        else:
                error_sintactico(Subrutine_esperados)
def Object():
        global Object_esperados
        if(token() == "tk_id" ):
                emparejar("tk_id")
                emparejar("tk_dospuntos")
                Tipo()
                return
        else:
                error_sintactico(Object_esperados)
def IfElseSentence():
        global IfElseSentence_esperados
        if(token() == "sino" ):
                emparejar("sino")
                BodyIfSentence()
                return
        elif(token() == "tk_llave_der" ):
                return
        else:
                error_sintactico(IfElseSentence_esperados)
def AssignationVar():
        global AssignationVar_esperados
        if(token() == "tk_id" ):
                Declaration()
                ListDeclarations()
                return
        else:
                error_sintactico(AssignationVar_esperados)
def ListId():
        global ListId_esperados
        if(token() == "tk_coma" ):
                emparejar("tk_coma")
                Expression()
                ListId()
                return
        elif(token() == "tk_dospuntos" or token() == "tk_asig" ):
                return
        else:
                error_sintactico(ListId_esperados)
def SettingsConst():
        global SettingsConst_esperados
        if(token() == "const" ):
                emparejar("const")
                AssignationConst()
                return
        else:
                error_sintactico(SettingsConst_esperados)
def ListObject():
        global ListObject_esperados
        if(token() == "tk_id" ):
                Object()
                ListObject()
                return
        elif(token() == "inicio" or token() == "const" or token() == "tipos" or token() == "var" ):
                return
        else:
                error_sintactico(ListObject_esperados)
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
        elif(token() == "matriz" ):
                emparejar("matriz")
                emparejar("tk_brac_izq")
                TipoVector()
                emparejar("tk_brac_der")
                Tipo()
                return
        elif(token() == "registro" ):
                emparejar("registro")
                emparejar("tk_llave_izq")
                AssignationVar()
                emparejar("tk_llave_der")
                return
        elif(token() == "logico" ):
                emparejar("logico")
                return
        elif(token() == "tk_id" ):
                emparejar("tk_id")
                return
        else:
                error_sintactico(Tipo_esperados)
def CallToFunctionSeenId():
        global CallToFunctionSeenId_esperados
        if(token() == "tk_par_izq" ):
                emparejar("tk_par_izq")
                FunctionParams()
                emparejar("tk_par_der")
                return
        else:
                error_sintactico(CallToFunctionSeenId_esperados)
def OtherExpression():
        global OtherExpression_esperados
        if(token() == "tk_exp" or token() == "tk_suma" or token() == "tk_mayorigual" or token() == "tk_mult" or token() == "and" or token() == "tk_mayor" or token() == "tk_menor" or token() == "tk_menorigual" or token() == "tk_mod" or token() == "tk_division" or token() == "tk_igualdad" or token() == "tk_resta" or token() == "or" or token() == "tk_distinto" ):
                Operador()
                Expression()
                return
        elif(token() == "tk_brac_izq" ):
                emparejar("tk_brac_izq")
                Expression()
                emparejar("tk_brac_der")
                return
        elif(token() == "tk_llave_der" or token() == "si" or token() == "var" or token() == "eval" or token() == "mientras" or token() == "const" or token() == "tk_llave_izq" or token() == "tk_coma" or token() == "FALSE" or token() == "tk_par_der" or token() == "tk_resta" or token() == "tk_num" or token() ==
"tk_brac_der" or token() == "tipos" or token() == "tk_par_izq" or token() == "hasta" or token() == "fin" or token() == "desde" or token() == "inicio" or token() == "caso" or token() == "repetir" or token() == "tk_id" or token() == "tk_pyq" or token() == "TRUE" or token() == "tk_asig" or token() == "sino" or token() == "tk_dospuntos" or token() == "tk_cadena" ):
                return
        else:
                error_sintactico(OtherExpression_esperados)
def LoopStep():
        global LoopStep_esperados
        if(token() == "tk_id" or token() == "FALSE" or token() == "TRUE" or token() == "tk_num" or token() == "tk_cadena" ):
                Constant()
                return
        else:
                error_sintactico(LoopStep_esperados)
def EvalSentence():
        global EvalSentence_esperados
        if(token() == "eval" ):
                emparejar("eval")
                emparejar("tk_llave_izq")
                BodyEvalSentence()
                emparejar("tk_llave_der")
                return
        else:
                error_sintactico(EvalSentence_esperados)
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
                ConstantSeenId()
                return
        elif(token() == "TRUE" ):
                emparejar("TRUE")
                return
        elif(token() == "FALSE" ):
                emparejar("FALSE")
                return
        else:
                error_sintactico(Constant_esperados)
def FunctionParamsNotEmpty():
        global FunctionParamsNotEmpty_esperados
        if(token() == "tk_coma" ):
                emparejar("tk_coma")
                Expression()
                FunctionParamsNotEmpty()
                return
        elif(token() == "tk_par_der" ):
                return
        else:
                error_sintactico(FunctionParamsNotEmpty_esperados)
def BodyWhile():
        global BodyWhile_esperados
        if(token() == "tk_id" or token() == "repetir" or token() == "si" or token() == "eval" or token() == "desde" or token() == "mientras" ):
                Body()
                BodyWhile()
                return
        elif(token() == "tk_llave_der" or token() == "hasta" ):
                return
        else:
                error_sintactico(BodyWhile_esperados)
def AssignationConst():
        global AssignationConst_esperados
        if(token() == "tk_llave_izq" or token() == "tk_id" or token() == "FALSE" or token() == "tk_cadena" or token() == "TRUE" or token() == "tk_resta" or token() == "tk_num" or token() == "tk_par_izq" ):
                Assignation()
                ListAssignations()
                return
        else:
                error_sintactico(AssignationConst_esperados)
def TipoVector():
        global TipoVector_esperados
        if(token() == "tk_llave_izq" or token() == "tk_id" or token() == "FALSE" or token() == "tk_cadena" or token() == "TRUE" or token() == "tk_resta" or token() == "tk_num" or token() == "tk_par_izq" ):
                Expression()
                ListTipoVector()
                return
        elif(token() == "tk_mult" ):
                emparejar("tk_mult")
                ListTipoVector()
                return
        else:
                error_sintactico(TipoVector_esperados)
def ListSubrutine():
        global ListSubrutine_esperados
        if(token() == "subrutina" ):
                Subrutine()
                ListSubrutine()
                return
        elif(token() == "subrutina" or token() == "EOF" ):
                return
        else:
                error_sintactico(ListSubrutine_esperados)
def Body():
        global Body_esperados
        if(token() == "tk_id" or token() == "repetir" or token() == "si" or token() == "eval" or token() == "desde" or token() == "mientras" ):
                Sentence()
                ListOfSentences()
                return
        else:
                error_sintactico(Body_esperados)
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
def SubrutineStart():
        global SubrutineStart_esperados
        if(token() == "subrutina" ):
                emparejar("subrutina")
                FunctionDeclaration()
                OptionalReturn()
                return
        else:
                error_sintactico(SubrutineStart_esperados)
def ListOfSentences():
        global ListOfSentences_esperados
        if(token() == "tk_id" or token() == "repetir" or token() == "si" or token() == "eval" or token() == "desde" or token() == "mientras" ):
                Sentence()
                ListOfSentencesHasSentence()
                return
        elif(token() == "hasta" or token() == "tk_llave_der" or token() == "si" or token() == "eval" or token() == "fin" or token() == "desde" or token() == "caso" or token() == "mientras" or token() == "tk_id" or token() == "repetir" or token() == "sino" ):
                return
        else:
                error_sintactico(ListOfSentences_esperados)
def ListExpressionNotEmpty():
        global ListExpressionNotEmpty_esperados
        if(token() == "tk_coma" ):
                emparejar("tk_coma")
                Expression()
                ListExpressionNotEmpty()
                return
        elif(token() == "tk_llave_der" ):
                return
        else:
                error_sintactico(ListExpressionNotEmpty_esperados)
def ListAssignations():
        global ListAssignations_esperados
        if(token() == "tk_llave_izq" or token() == "tk_id" or token() == "FALSE" or token() == "tk_cadena" or token() == "TRUE" or token() == "tk_resta" or token() == "tk_num" or token() == "tk_par_izq" ):
                Assignation()
                ListAssignations()
                return
        elif(token() == "inicio" or token() == "const" or token() == "tipos" or token() == "var" ):
                return
        else:
                error_sintactico(ListAssignations_esperados)
def FunctionDeclarationParams():
        global FunctionDeclarationParams_esperados
        if(token() == "tk_par_der" ):
                return
        elif(token() == "tk_id" ):
                Declaration()
                FunctionDeclarationParamsNotEmpty()
                return
        else:
                error_sintactico(FunctionDeclarationParams_esperados)
def ListExpression():
        global ListExpression_esperados
        if(token() == "tk_llave_der" ):
                return
        elif(token() == "tk_llave_izq" or token() == "tk_id" or token() == "FALSE" or token() == "tk_cadena" or token() == "TRUE" or token() == "tk_resta" or token() == "tk_num" or token() == "tk_par_izq" ):
                Expression()
                ListExpressionNotEmpty()
                return
        else:
                error_sintactico(ListExpression_esperados)
def BodyEvalSentence():
        global BodyEvalSentence_esperados
        if(token() == "caso" ):
                BodyCase()
                BodyIfElseCase()
                return
        else:
                error_sintactico(BodyEvalSentence_esperados)
def IfSentence():
        global IfSentence_esperados
        if(token() == "tk_llave_izq" ):
                emparejar("tk_llave_izq")
                BodyIfSentence()
                IfElseSentence()
                emparejar("tk_llave_der")
                return
        elif(token() == "tk_llave_izq" or token() == "tk_id" or token() == "FALSE" or token() == "tk_cadena" or token() == "TRUE" or token() == "tk_resta" or token() == "tk_num" or token() == "tk_par_izq" ):
                Assignation()
                return
        else:
                error_sintactico(IfSentence_esperados)


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

allTokens.append(Token("EOF",startingTokenColumn+1,startingTokenRow+1,"EOF"))
_token = nextToken()
#print(_token.to_str()) ### PARA DEBUG
S()
emparejar("EOF")
if(token() is not None or not first_error):
	error_sintactico(["EOF"])
else:
	print("El analisis sintactico ha finalizado exitosamente.")

