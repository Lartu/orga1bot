# -*- coding:utf-8 -*-
# Ensamblador de Orga I por Martín del Río (2017)

def binario3(a):
	if a=="0":
		return "000"
	elif a=="1":
		return "001"
	elif a=="2":
		return "010"
	elif a=="3":
		return "011"
	elif a=="4":
		return "100"
	elif a=="5":
		return "101"
	elif a=="6":
		return "110"
	elif a=="7":
		return "111"
	else:
		return "000"
		
def extender(num, n):
	if(len(num) < n):
		num = ("0"*(n-len(num))) + num
	return num
	
def extenderComp(num, n):
	if(len(num) < n):
		if num[0] == "0":
			num = ("0"*(n-len(num))) + num
		else:
			num = ("1"*(n-len(num))) + num
	return num

def pasarABinario(num, n):
	if num>=0:
		#print num
		num = bin(int(num))[2:]
		if(len(num) < n):
			num = "0"+num
			num = extenderComp(num, n)
		#print num
		return num
	else:
		#print num
		num = -num;
		num = bin(int(num))[2:]
		if(len(num) < n):
			num = "1"+num
			num = extenderComp(num, n)
		#print num
		return str(num)

def esARegistro(par):
	for a in range(0, 8):
		if par[0:2] == "R"+str(a):
			return True
		if par[0:3] == "[R"+str(a):
			return True
	return False

def ensamblar(codigo, devolverEnHexa):
	listaTags = []
	numeroPalabra = 0
	ensambladoTotal = ""
	resultado = ""
	for linea in codigo:
		try:
			ensamblado = ""
			tag = ""
			ensHex = ""
			constante = []
			linea = linea.upper()
			if ":" in linea:
				tag = linea[0:linea.find(":")]
				linea = linea[linea.find(":")+1:]
				listaTags.append([tag, numeroPalabra])
			if "#" in linea:
				linea = linea[0:linea.find("#")]
			if ";" in linea:
				linea = linea[0:linea.find(";")]
			linea = linea.strip()
			tag = tag.strip()
			if len(linea) == 0:
				continue
			parametro = linea.split()
			if(len(parametro) > 3):
				return "\""+linea+"\": Linea mal formada. La máxima cantidad de parámetros que puede recibir un comando es dos. Revisá que no tengas espacios de más."
				break
			#DOS OPERANDOS / UN OPERANDO DESTINO / UN OPERANDO FUENTE
			if parametro[0] in ["MOV", "ADD", "SUB", "AND", "OR", "CMP", "ADDC", "NEG", "NOT", "JMP", "CALL", "RET"]:
				operandos = [1,2]
				fuente = False
				numeroPalabra += 1;
				if parametro[0] == "MOV":
					ensamblado += "0001"
				elif parametro[0] == "ADD":
					ensamblado += "0010"
				elif parametro[0] == "SUB":
					ensamblado += "0011"
				elif parametro[0] == "AND":
					ensamblado += "0100"
				elif parametro[0] == "OR":
					ensamblado += "0101"
				elif parametro[0] == "CMP":
					ensamblado += "0110"
				elif parametro[0] == "ADDC":
					ensamblado += "1101"
				elif parametro[0] == "NEG":
					ensamblado += "1000"
					operandos  = [1];
				elif parametro[0] == "NOT":
					ensamblado += "1001"
					operandos = [1];
				elif parametro[0] == "JMP":
					ensamblado += "1010"
					operandos = [1];
					fuente = True
				elif parametro[0] == "CALL":
					ensamblado += "1011"
					operandos = [1];
					fuente = True
				elif parametro[0] == "RET":
					operandos = [];
					ensamblado += "1100000000000000";
				#Para un operando fuente
				if fuente:
					ensamblado += "000000"
				for a in operandos:
					if a == 1 and operandos==[1,2]:
						if parametro[a][-1:] == ",":
							parametro[a] = parametro[a][:-1] #le saco la coma de XXX A, B
					if esARegistro(parametro[a]): #A registro
						if parametro[a][0] == "[": #Indirecto o indexado
							if "+" in parametro[a]: #Indexado
								ensamblado+="111"+binario3(parametro[a][2])
								constante.append(parametro[a][4:][:-1])
							else: #Indirecto
								ensamblado+="110"+binario3(parametro[a][2])
						else: #Registro
							ensamblado+="100"+binario3(parametro[a][1])
					else: #A constante
						if parametro[a][0] == "[": #Directo o indirecto
							if parametro[a][1] == "[": #Indirecto
								ensamblado+="011000"
								constante.append(parametro[a][2:][:-2])
							else: #Directo
								ensamblado+="001000"
								constante.append(parametro[a][1:][:-1])
						else: #Inmediato
							ensamblado+="000000"
							constante.append(parametro[a])
				#Para un operando destino
				if operandos == [1] and not(fuente):
					ensamblado += "000000"
				#print "Constantes:", constante
				for c in constante:
					numeroPalabra += 1;
					if c[0:2] == "0X":
						ensamblado += " "+extender(str(bin(int(c,16)))[2:],16)
					else:
						ensamblado += " %"+c+"%"
			elif parametro[0] in ["JE", "JNE", "JLE", "JG", "JL", "JGE", "JLEU", "JGU", "JCS", "JNEG", "JVS"]:
				if parametro[0] == "JE":
					ensamblado += "11110001"
				elif parametro[0] == "JNE":
					ensamblado += "11111001"
				elif parametro[0] == "JLE":
					ensamblado += "11110010"
				elif parametro[0] == "JG":
					ensamblado += "11111010"
				elif parametro[0] == "JL":
					ensamblado += "11110011"
				elif parametro[0] == "JGE":
					ensamblado += "11111011"
				elif parametro[0] == "JLEU":
					ensamblado += "11110100"
				elif parametro[0] == "JGU":
					ensamblado += "11111100"
				elif parametro[0] == "JCS":
					ensamblado += "11110101"
				elif parametro[0] == "JNEG":
					ensamblado += "11110110"
				elif parametro[0] == "JVS":
					ensamblado += "11110111"
				if parametro[1][0:2] == "0X":
					if len(parametro[1]) > 4:
						#Crashea si hago un return con tildes. Ver por qué.
						return "\""+linea+"\": Los saltos condicionales reciben valores de 2 bytes, no "+str(len(parametro[1])-2)+"."
					else:	
						ensamblado += extender(str(bin(int(parametro[1], 16)))[2:], 8)
				else:
					ensamblado += "&"+parametro[1]+"&"
				numeroPalabra += 1;
			elif parametro[0] == "DW":
				if parametro[1][0:2] == "0X":
					ensamblado += extender(str(bin(int(parametro[1], 16)))[2:], 16)
				else:
					ensamblado += "%"+parametro[1]+"%"
				numeroPalabra += 1;
			else:
				return "\""+linea+"\": Comando desconocido."
		except:
			return "Error en la linea: " + linea +"\n"
		#print "("+linea+"):"
		#print "Tag:", tag
		#print "Bin:", ensamblado
		#print "Tags:", listaTags
		ensambladoTotal+=" "+ensamblado
		#print ""
	palabras = ensambladoTotal.split()
	ensambladoTotal = ""
	ensambladoHexa = ""
	posicionPalabra = 0
	#Reemplazo tags
	for p in palabras:
		posicionPalabra+=1
		if "%" in p:
			tag = p[1:-1]
			for t in range(len(listaTags)):
				if tag==listaTags[t][0]:
					ensambladoTotal += " " + pasarABinario(int(listaTags[t][1]), 16)
					break
				if t == len(listaTags)-1:
					return "Tag no encontrado: "+ tag+"\n"
		elif "&" in p:
			comienzo = p[0:p.find("&")]
			tag = p[p.find("&")+1:-1]
			reemplazo = ""
			for t in range(len(listaTags)):
				if tag==listaTags[t][0]:
					reemplazo = pasarABinario(int(listaTags[t][1])-posicionPalabra, 8)
					break
				if t == len(listaTags)-1:
					return "Tag no encontrado: "+ tag+"\n"
			ensambladoTotal += " " + str(comienzo)+str(reemplazo)
		else:
			ensambladoTotal += " " + p
	ensambladoTotal = ensambladoTotal.strip()
	for p in ensambladoTotal.split():
		ensambladoHexa += " " + extender(hex(int(p, 2))[2:], 4).upper()
	ensambladoHexa = ensambladoHexa.strip()
	#Ensamblado binario
	if devolverEnHexa:
		
		return ensambladoHexa.replace(" ","\n")
	else:
		lineas = ensambladoTotal.split()
		ensambladoBinario = ""
		bitsEscritos = 0
		for l in lineas:
			for a in l:
				ensambladoBinario += a
				bitsEscritos+=1
				if bitsEscritos%4 == 0:
					ensambladoBinario+=" "
			ensambladoBinario+='\n'
		return ensambladoBinario
			
def cargarArchivo(archivo):
	codigo = []
	with open(archivo) as file:
		for line in file:
			codigo.append(line)
	return codigo

#print ensamblar(cargarArchivo("fibo.asm"), True)
#print ensamblar(["JE 0x0000"], True)
#print ensamblar(["JE main","MOV R0, r1","main: MOV r0, r1", "JE main", "this: JE this"], False)
