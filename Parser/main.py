import Psilex

Tokens = Psilex.Tokens
#for tok in Tokens:
    #print("<{},{},{}>".format(tok.type, tok.line, tok.column))

token = Tokens.pop(0)



grammar = [
    ['A',["B","C"]],
    ['A',["ant","A","all"]],
    ['B',["big","C"]],
    ['B',["bus","A","boss"]],
    ['B',["EPSILON"]],
    ['C',["cat"]],
    ['C',["cow"]]
]

terminals = ["ant","all","big","bus","boss","cat","cow"]
no_Terminals = ["A","B","C"]
start = "A"



def CALCULAR_PRIMEROS(no_terminal):
    conjunto_final = []
    REGLAS = [rule for rule in grammar if rule[0]==no_terminal]
    for R in REGLAS:
        REGLA = R[1]
        conjunto_final = conjunto_final + PRIMEROS(REGLA)
    return conjunto_final
        

def PRIMEROS(REGLA):
    #1
    if REGLA == ["EPSILON"]:
        return ["EPSILON"]
    if "EPSILON" not in REGLA:
    #2
        #a
        if REGLA[0] in terminals:
            return [REGLA[0]]
        if REGLA[0] in no_Terminals:
            primeros = []
            #b
            primeros = CALCULAR_PRIMEROS(REGLA[0])
            if "EPSILON" in CALCULAR_PRIMEROS(REGLA[0]):
                primeros.remove("EPSILON")
            #c
            if "EPSILON" in CALCULAR_PRIMEROS(REGLA[0]):
                if len(REGLA) == 1:
                    primeros.append("EPSILON")
                if len(REGLA) > 1:
                    cadena = REGLA[1:]
                    p = []
                    if len(cadena)>1:
                        p = PRIMEROS(cadena)
                    else:
                        p = CALCULAR_PRIMEROS(cadena[0])
                    primeros = primeros + p
            return primeros
        

def CALCULAR_SIGUIENTES(no_terminal):
    conjunto_final = []
    if no_terminal == start:
        conjunto_final.append("$")
    
    REGLAS = []
    for rule in grammar:
        if no_terminal in rule[1]:
            REGLAS.append(rule)
    #REGLAS = [rule for rule in grammar if (no_terminal in rule[1])]
    
    for R in REGLAS:
        REGLA = R
        conjunto_final = conjunto_final + SIGUIENTES(REGLA,no_terminal)
    return conjunto_final


def SIGUIENTES(R,no_terminal):
    siguientes = []
    nt_regla = R[0]
    REGLA = R[1]
    
    index_nt = REGLA.index(no_terminal)
    cadena_b = REGLA[index_nt+1:]
    
    if cadena_b == []:
        cadena_b.append("EPSILON")
    
    if "EPSILON" in PRIMEROS(cadena_b):
        primeros_b = PRIMEROS(cadena_b)
        primeros_b.remove("EPSILON")
        siguientes = siguientes + primeros_b
        if "EPSILON" in PRIMEROS(cadena_b):
            siguientes = siguientes + CALCULAR_SIGUIENTES(nt_regla)
    else:
        siguientes = siguientes + PRIMEROS(cadena_b)
    return siguientes


def PREDICT(A):
    nt_regla = A[0]
    REGLA = A[1]
    C_PREDICT = []
    
    if "EPSILON" in PRIMEROS(REGLA):
        C = PRIMEROS(REGLA)
        C.remove("EPSILON")
        C_PREDICT = C + CALCULAR_SIGUIENTES(nt_regla)
        return C_PREDICT
    else:
        C = PRIMEROS(REGLA)
        C_PREDICT = C
        return C_PREDICT


#for x in range(0, len(grammar)):
    #print(PREDICT(grammar[x]))

def EMPAREJAR(token_esperado):
    if token == token_esperado:
        token = Tokens.pop(0)
    else:
        errorSintactico([token_esperado])

def errorSintactico(token):
    print("Error sintactico")

def State(n_t):
    REGLAS = [rule for rule in grammar if rule[0]==n_t]
    PREDICCIONES = []
    for rule in REGLAS:
        PREDICCIONES.append(PREDICT(rule))
    for p in range(0,len(PREDICCIONES)):
        if token in PREDICCIONES[p]:
            RULE = REGLAS[p][1]
            for part in RULE:
                if part in no_Terminals:
                    State(part)
                if part in terminals:
                    EMPAREJAR(part)
                if part == "EPSILON":
                    pass
        return
    
    errorSintactico(PREDICCIONES[p])

def print_predictions():

    firstSets = {}
    for c in no_Terminals:
        firstSets[c] = [] 
    followingSets = {}
    for c in no_Terminals:
        followingSets[c] = []
    predictionsSets = []
    for c in grammar:
        predictionsSets.append(PREDICT(c))

    print(predictionsSets)

print_predictions()
