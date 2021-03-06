import Psilex
from Psilex import Token
Tokens = Psilex.Tokens
# tok in Tokens:
    #print("<{},{},{},{}>".format(tok.type,tok.value, tok.line, tok.column))





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
prediction_sets = []


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

 


def SIGUIENTES(no_terminal,visited):
    follow_ = []
    RULES = grammar
    
    if no_terminal == start:
        follow_.append('EOF')
    if no_terminal in visited:
        return follow_
    for nt,rule in RULES:
        
        if no_terminal in rule:
            
            following_str = rule[rule.index(no_terminal)+1:]
            while True:
                if following_str == []:
                    if nt == no_terminal:
                        break
                    else:
                        visited.append(no_terminal)
                        follow_ = follow_ + SIGUIENTES(nt,visited)
                else:
                    follow_2 = PRIMEROS(following_str)
                    if "EPSILON" in follow_2:
                        follow_2.remove("EPSILON")
                        follow_ = follow_ + follow_2
                        follow_ = follow_ + SIGUIENTES(nt,visited)
                    else:
                        follow_ = follow_ + follow_2

                follow_ = list(dict.fromkeys(follow_))

                if no_terminal not in following_str:
                    break
                else:
                    following_str = following_str[following_str.index(no_terminal)+1:]
            if following_str == []:
                if nt == no_terminal:
                    continue
        
        
            

    return follow_
    
        

        
        





def PREDICT(A):
    nt_regla = A[0]
    REGLA = A[1]
    C_PREDICT = []
    
    if "EPSILON" in PRIMEROS(REGLA):
        
        C = PRIMEROS(REGLA)
        C.remove("EPSILON")
        visited = []
        C_PREDICT = C + SIGUIENTES(nt_regla,visited)
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


tokens_dict = {
    "tk_mas": "+",
    "tk_menos": "-",
    "tk_mult":"*",
    "tk_div":"/",
    "tk_mod":"%",
    "tk_asig":"=",
    "tk_menor":"<",
    "tk_mayor":">",
    "tk_menor_igual":"<=",
    "tk_mayor_igual":">=",
    "tk_igual":"==",
    "tk_y":"&&",
    "tk_o":"||",
    "tk_dif":"!=",
    "tk_neg":"!",
    "tk_dosp":":",
    "tk_pyc":";",
    "tk_coma":",",
    "tk_punto":".",
    "tk_par_izq":"(",
    "tk_par_der":")",
    "id":"identificador",
    "tk_entero":"valor_entero",
    "tk_real":"valor_real",
    "tk_caracter":"valor_caracter",
    "tk_cadena":"valor_cadena",
    "funcion_principal":"funcion_principal",
    "fin_principal":"fin_principal",
    "leer":"leer",
    "imprimir":"imprimir",
    "booleano":"booleano",
    "caracter":"caracter",
    "entero":"entero",
    "real":"real",
    "cadena":"cadena",
    "si":"si",
    "entonces":"entonces",
    "fin_si":"fin_si",
    "si_no":"si_no",
    "mientras":"mientras",
    "hacer":"hacer",
    "fin_mientras":"fin_mientras",
    "para":"para",
    "fin_para":"fin_para",
    "seleccionar":"seleccionar",
    "entre":"entre",
    "caso":"caso",
    "romper":"romper",
    "defecto":"defecto",
    "fin_seleccionar":"fin_seleccionar",
    "estructura":"estructura",
    "fin_estructura":"fin_estructura",
    "funcion":"funcion",
    "fin_funcion":"fin_funcion",
    "retornar":"retornar",
    "falso":"falso",
    "verdadero":"verdadero",
    "EOF":"EOF"
}

lista_tk = list(tokens_dict.keys())
d = {k:v for v,k in enumerate(lista_tk)}



def errorSintactico(esperados):
    if "funcion_principal" in esperados:
        print("Error sintactico: falta funcion_principal",end='')
        exit()
    found = ""
    if token.value != None:
        found = token.value
    else:
        found = token.type
    print("<{},{}> Error sintactico: se encontro: \"{}\"; se esperaba: ".format(token.line,token.column,found),end='')
    
    esperados.sort(key=d.get)
    esperados_t = []
    for e in esperados:
        esperados_t.append(tokens_dict[e])

    esperados_str = ""
    for e in range(0,len(esperados_t)):
        if e == len(esperados_t)-1:
            esperados_str = esperados_str +"\""+ esperados_t[e] +"\""+ "."
        else:
            esperados_str = esperados_str +"\""+ esperados_t[e] +"\""+","+ " "
    print(esperados_str,end="")
    exit()

def State(n_t):

    
    PREDICCIONES = []
    REGLAS = []

    for p in range(0,len(grammar)):   
        if grammar[p][0] == n_t:
            REGLAS.append(grammar[p])
            PREDICCIONES.append(prediction_sets[p][1])
    
    terminals_regla = []
    for p in PREDICCIONES:
        terminals_regla = terminals_regla + p

    for p in range(0,len(PREDICCIONES)):
        if token.type in PREDICCIONES[p]:
            RULE = REGLAS[p][1]
            #print(REGLAS[p])
            for part in RULE:
                if part in no_Terminals:
                    #print("ejecuto")
                    #print(part)
                    State(part)
                if part in terminals:
                    #print("empareje")
                    #print(part)
                    EMPAREJAR(part)
                if part == "EPSILON":
                    pass
            return
    #print(n_t)
    #print(PREDICCIONES)
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



#store production sets for no time consume
#with open("prediction_sets.txt","w") as f:
    #for nt,rule in grammar:
        #prediction = PREDICT([nt,rule])
        #print(prediction)
        #f.write("{} -> ".format(nt))
        #str = ""
        #for e in prediction:
            #str = str + e + " "
        #f.write(str)
        #f.write("\n")





with open("prediction_sets.txt","r") as f:
    predictions = f.readlines()
    for prediction in predictions:
        prediction_type = []
        prediction = prediction.rstrip()
        part_of_prediction = prediction.split(" ")
        nt = part_of_prediction[0]
        prediction_list = part_of_prediction[2:]
        prediction_type.append(nt)
        prediction_type.append(prediction_list)
        prediction_sets.append(prediction_type)











Tokens.append(Token("EOF", None, 0, 0))
token = Tokens.pop(0)


siguientes_set = {i: set() for i in no_Terminals}



#get start
start = no_Terminals[0]

#get first tokens



#begin
State(start)






    

if token.type != "EOF":
    errorSintactico(["EOF"])
else:
    print("El analisis sintactico ha finalizado exitosamente.",end='')

