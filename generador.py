import sys

#TODO: La Mayoria de nombres de token son diferentes, encontrar un acercamiento mas general 
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
				"sino",
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
				"EOF",
				"[",
				"]",
				"fin",
				"inicio",
				"const",
				"var",
				"tipos",
				"registro",
				"TRUE",
				"FALSE",
				"{",
				"}","and","or","numerico","cadena","logico","vector", "eval", "repetir", "hasta", "desde"]

terminales = [  "tk_suma",
				"tk_resta",
				"tk_mult",
				"tk_division",
				"tk_mod",
				"tk_asig",
				"tk_menor",
				"tk_mayor",
				"tk_menorigual",
				"tk_mayorigual",
				"tk_igualdad",
				"tk_y",
				"tk_o",
				"tk_distinto",
				"tk_neg",
				"tk_dospuntos",
				"tk_pyq",
				"tk_coma",
				"tk_punto",
				"tk_par_izq",
				"tk_par_der",
				"tk_id",
				"tk_num",
				"tk_real",
				"tk_caracter",
				"tk_cadena",
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
				"sino",
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
				"EOF",
				"tk_brac_izq",
				"tk_brac_der",
				"fin",
				"inicio",
				"const",
				"var",
				"tipos",
				"registro",
				"TRUE",
				"FALSE",
				"tk_llave_der",
				"tk_llave_izq","and","or","numerico","cadena","logico","vector", "eval", "repetir", "hasta", "desde"]


def union(primeros, begins):
    n = len(primeros)
    primeros |= begins
    return len(primeros) != n

def cont(S):
	aux = ""
	for i in S:
		aux = aux + i + " "
	return aux

def pred_set(reglas):
	global prediccion,reglas_index
	primeros = {i: set() for i in noterminales}
	primeros.update((i, {i}) for i in terminales)
	siguientes = {i: set() for i in noterminales}
	epsilon = set()
	
	siguientes[sim_inicial] |= {'EOF'}

	while True:

		updated = False

		for regla in reglas:
			nt = regla[0]

			# Primeros
			for simbolo in (regla[2:]):
				updated |= union(primeros[nt], primeros[simbolo])
				if simbolo not in epsilon:
					break
			else:
				updated |= union(epsilon, {nt})
			    
			# Siguientes
			aux = siguientes[nt]
			for simbolo in reversed(regla[2:]):
				if simbolo in siguientes:
					updated |= union(siguientes[simbolo], aux)
				if simbolo in epsilon:
					aux = aux.union(primeros[simbolo])
				else:
					aux = primeros[simbolo]

		if not updated:

			i = 0

			for regla in reglas:
				nt = regla[0]
				reglas_index[nt].append(i)

				eps = True
				for simbolo in regla[2:] :					
					if simbolo not in epsilon:
						prediccion[i] |= primeros[simbolo]
						eps = False
						break	
					else:
						prediccion[i] |= primeros[simbolo]
				if (eps) :
					prediccion[i] |= siguientes[nt]

				i += 1

			break
	"""
	print("EPSILON")
	print("PREDICCION")
	for i in range(0,len(prediccion)):
		print(i)
		print(prediccion[i])
	print("PRIMEROS")
	for i in primeros:
		print(i)
		print(primeros[i])
	print("SIGUIENTES")
	for i in siguientes:
		print(i)
		print(siguientes[i])
	"""



N = int(input())


#noterminales = ["A","B","S"] # Segun la gramatica
#terminales = ["uno","dos","tres","cuatro","cinco","seis","EOF"]
noterminales = set()
sim_inicial = "S"
reglas = []
orden_terminales = {terminales[i] : i for i in range(0,len(terminales))}


for i in range(0,N):
	reglas.append(sys.stdin.readline().strip().split(' '))
	noterminales |= {reglas[i][0]}

noterminales = list(noterminales)
reglas_index = {i : [] for i in noterminales}
prediccion = [set() for i in range(0,len(reglas))]
pred_set(reglas)




funcion = ""
cabezera = ""

for nt in noterminales:

	funcion += "def " + nt + "(): \n"
	#funcion += "\tprint(\" USANDO: + "  + nt + "\") \n" ### PARA DEBUG
	funcion += "\tglobal "+ nt + "_esperados\n\tif("

	predicciones_todas_regla = prediccion[reglas_index[nt][0]]
	tokens = list(prediccion[reglas_index[nt][0]])
	for token in tokens[:-1]:
		funcion += "token() == \"" + token + "\" or "
	funcion += "token() == \"" + tokens[-1] + "\" ): \n"
	for token in reglas[reglas_index[nt][0]][2:]:
		if (token in noterminales):
			funcion += "\t\t" + token +  "()\n"
		else:
			#funcion += "\t\tprint(\" EMPAREJAR : + "  + cont(reglas[reglas_index[nt][0]]) + "EL TOKEN" + token + "\") \n" ### PARA DEBUG
			funcion += "\t\t" + "emparejar(\"" + token + "\")\n" 
	funcion += "\t\treturn\n"

	for indx in reglas_index[nt][1:]:
		funcion += "\telif("

		predicciones_todas_regla |= prediccion[indx]
		tokens = list(prediccion[indx])
		for token in tokens[:-1]:
			funcion += "token() == \"" + token + "\" or "
		funcion += "token() == \"" + tokens[-1] + "\" ): \n"
		for token in reglas[indx][2:]:
			if (token in noterminales):
				funcion += "\t\t" + token +  "()\n"
			else:
				#funcion += "\t\tprint(\" EMPAREJAR : + "  + cont(reglas[indx]) + "EL TOKEN" + token + "\") \n" ### PARA DEBUG

				funcion += "\t\t" + "emparejar(\"" + token + "\")\n" 
		funcion += "\t\treturn\n"
	funcion += "\telse: \n"
	#funcion += "\t\tprint(\" ERROR EN : + "  + nt + "\") \n" ### PARA DEBUG
	funcion += "\t\terror_sintactico("+nt+"_esperados)\n"

	esperados = list(predicciones_todas_regla)
	esperados.sort(key = lambda x: orden_terminales[x])
	esperados = list(map(lambda x: traduccion_tk[orden_terminales[x]],esperados))
	cabezera += nt + "_esperados = " + str(esperados ) + " \n"


print("\n -- INICIO DEL CODIGO --\n")
print(cabezera)
print(funcion)	
print("\n -- FIN DEL CODIGO --\n")


""" Ejemplo de entrada
11
S -> A uno B C
S -> S dos
A -> B C D
A -> A tres
A ->
B -> D cuatro C tres
B ->
C -> cinco D B
C ->
D -> seis
D ->

EJEMPO PARA LA CADENA A1 A2
3
S -> funcion_principal A 
A -> imprimir tk_par_izq tk_entero tk_mas tk_entero tk_par_der B
B -> tk_pyc fin_principal


	"""

