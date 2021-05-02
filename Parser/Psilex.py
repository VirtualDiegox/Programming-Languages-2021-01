import lex as lex
from lex import TOKEN
import io, sys
#lines for test local
test = open('test.txt', 'r')
sys.stdin = io.StringIO(test.read())

with open("tokens.txt","r") as file:
        tokens_ = file.readlines()
        tokens = []
        for a in tokens_:
            b = a.rstrip()
            tokens.append(b)
with open("reserved_words.txt","r") as file:
        words_ = file.readlines()
        words = []
        for a in words_:
            b = a.rstrip()
            words.append(b)

tokens = tokens + words


def t_MULTICOMMENT(t):
  r'/[*][^*]*[*]+([^/*][^*]*[*]+)*/|//[^\n]*'
  spaces = t.value.count('\n')
  t.lexer.lineno += spaces
  pass


t_tk_mas = r"\+"
t_tk_menos = r"\-"
t_tk_mult = r"\*"
t_tk_div = r"\/"
t_tk_mod = r"\%"
t_tk_asig = r"\="
t_tk_menor = r"\<"
t_tk_mayor = r"\>"
t_tk_menor_igual = r"\<\="
t_tk_mayor_igual = r"\>\="
t_tk_igual = r"\=\="
t_tk_y = r"\&\&"
t_tk_o = r"\|\|"
t_tk_dif = r"\!\="
t_tk_neg = r"\!"
t_tk_dosp = r"\:"
t_tk_pyc = r"\;"
t_tk_coma = r"\,"
t_tk_punto = r"\."
t_tk_par_izq = r"\("
t_tk_par_der = r"\)"

digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'
identifier       = r'('+identifier + r'|' + r'(' + digit + r'(' + nondigit + r')+)'+r')'


def t_tk_caracter(t):
  r'\'([a-zA-Z0-9_  ]{1})\''
  return t

def t_tk_cadena(t):
  r'\"(.*?)\"'
  return t


def t_id(t):
  r'([a-zA-Z_]+[0-9]*)'
  if t.value in words:
    t.type = t.value
  return t
def t_tk_real(t):
  r'[0-9]+\.[0-9]+'
  return t
def t_tk_entero(t):
  r'[0-9]+'
  return t
def t_id2(t):
  r'([0-9]+[a-zA-Z_]+)'
  t.type = "id"
  return t

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

t_ignore  = ' \t'

def t_CARRIAGE_RETURN(t):
    r'[\r]+'
    pass


def t_newline(t):
    r'[\n]+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    column = find_column(t.lexer.lexdata,t)
    print(">>> Error lexico (linea: {}, posicion: {})".format(t.lexer.lineno,column))
    
    exit()
    
    
    

lexer = lex.lex()
lexer.input(sys.stdin.read())

Tokens = []

class Token:
  def __init__(self,type,value,line,column):
    self.type = type
    self.value = value
    self.line = line
    self.column = column

types_wv = ["tk_entero","tk_real","tk_cadena","tk_caracter","id"]

while True:
    tok = lexer.token()
    if not tok:
        break    # No more input
    column = find_column(lexer.lexdata,tok)
    if tok.type in types_wv:
        Tokens.append(Token(tok.type, tok.value, tok.lineno, column))
    else:
        Tokens.append(Token(tok.type, tok.value, tok.lineno, column))