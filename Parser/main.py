import Psilex
from Psilex import Token
Tokens = Psilex.Tokens
#for tok in Tokens:
    #print("<{},{},{}>".format(tok.type, tok.line, tok.column))





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

 


def SIGUIENTES(no_terminal):
    follow_ = []

    RULES = grammar
    if no_terminal == start:
        follow_.append('$')
    for nt,rule in RULES:
        if no_terminal in rule:
            n = len(follow_)
            following_str = rule[rule.index(no_terminal)+1:]
            if following_str == []:
                if nt == no_terminal:
                    continue
                else:
                    follow_ = follow_ + SIGUIENTES(nt)
            else:
                follow_2 = PRIMEROS(following_str)
                if "EPSILON" in follow_2:
                    follow_2.remove("EPSILON")
                    follow_ = follow_ + follow_2
                    follow_ = follow_ + SIGUIENTES(nt)
                else:
                    follow_ = follow_ + follow_2

            follow_ = list(dict.fromkeys(follow_))
            if n != len(follow_):
                return follow_
    return follow_
    
        

        
        





def PREDICT(A):
    nt_regla = A[0]
    REGLA = A[1]
    C_PREDICT = []
    
    if "EPSILON" in PRIMEROS(REGLA):
        
        C = PRIMEROS(REGLA)
        C.remove("EPSILON")
        C_PREDICT = C + SIGUIENTES(nt_regla)
        return C_PREDICT
    else:
        C = PRIMEROS(REGLA)
        C_PREDICT = C
        return C_PREDICT


def EMPAREJAR(token_esperado):
    global token
    if token.type == token_esperado:
        token = Tokens.pop(0)
    else:
        errorSintactico([token_esperado])

def errorSintactico(esperados):
    print(token.value)
    print(token.type)
    print(esperados)
    print("Error sintactico")
    exit()

def State(n_t):
    
    
    PREDICCIONES = []
    REGLAS = []
    for nt,rule in grammar:
        
        if nt == n_t:
            REGLAS.append([nt,rule])
            PREDICCIONES.append(PREDICT([nt,rule]))
    for p in range(0,len(PREDICCIONES)):
        if token.type in PREDICCIONES[p]:
            RULE = REGLAS[p][1]
            for part in RULE:
                if part in no_Terminals:
                    State(part)
                if part in terminals:
                    print("empareje")
                    print(part)
                    EMPAREJAR(part)
                if part == "EPSILON":
                    pass
            return
    terminals_regla = []
    for p in PREDICCIONES:
        terminals_regla = terminals_regla + p
    errorSintactico(terminals_regla)

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
    for p in predictionsSets:
        print(p)

################################################################Parsing################################

#get grammar
with open("Psigrammar.txt", "r") as f:
    new_grammar = []
    rules = f.readlines()
    for rule in rules:
        rule_type = []
        rule = rule.rstrip()
        part_of_rule = rule.split(" ")
        nt = part_of_rule[0]
        rule_list = part_of_rule[2:]
        rule_type.append(nt)
        rule_type.append(rule_list)
        new_grammar.append(rule_type)
    clean_grammar = []
    for rule in new_grammar:
        if rule[0] != "":
            clean_grammar.append(rule)
    grammar = clean_grammar



#get not_terminals
no_Terminals = []
for rule in clean_grammar:  
    nt = rule[0]
    if nt not in no_Terminals:
        no_Terminals.append(nt)

#get terminals
from Psilex import tokens
terminals = tokens

#Tokens = []
#Tokens.append(Token("ant",None,0,0))
#Tokens.append(Token("cat",None,0,0))
#Tokens.append(Token("all",None,0,0))

Tokens.append(Token("EOF", None, 0, 0))
token = Tokens.pop(0)

primeros_set = {i: set() for i in no_Terminals}
siguientes_set = {i: set() for i in no_Terminals}



#get start
start = no_Terminals[0]

#get first tokens



#begin
State(start)







    

if token.type != "EOF":
    print(token)
    errorSintactico(["EOF"])
else:
    print("El analisis sintactico ha finalizado exitosamente.")
