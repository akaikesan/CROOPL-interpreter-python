# -*- encoding: utf-8 -*-

import ply.yacc as yacc

from rooplppLexer import tokens
from rooplppEval import evalProg  

classMap = {} 

def p_program(p):
    '''
    program :  classes
    '''

def p_classes(p):
    '''
    classes : classes class
    | 
    '''

def p_class(p):
    '''
    class : CLASS className varDeclarations methods
    '''
    classMap[p[2]] = {"fields" : p[3], "methods" : p[4]}
    



def p_className(p):
    '''
    className :  ID 
    '''
    p[0] = p[1]

def p_varDeclarations(p):
    '''
    varDeclarations : varDeclarations varDeclaration
    | 
    '''
    if (len(p) == 3):
        varDecls = p[1]
        varDecls[p[2]["name"]] = p[2]["type"]
        p[0] = varDecls
    else:
        p[0] = {}

def p_varDeclaration(p):
    '''
    varDeclaration : type varName 
    '''
    p[0] = {"name":p[2], "type":p[1]}

def p_type(p):
    '''
    type : INT 
    | className
    '''
    p[0] = p[1]

def p_varName(p):
    '''
    varName :  ID 
    '''
    p[0] = p[1]
def p_methods(p):
    '''
    methods  : methods method 
    | 
    '''
    if len(p) == 3: 
        methods = p[1]
        methods[p[2]["methodName"]] = p[2]["statements"]
        p[0] = methods
    else:
        p[0] = {} 


def p_method(p):
    '''
    method : METHOD ID  LPAREN RPAREN COLON statements
    '''
    p[0] = {"methodName": p[2], "statements": p[6]}

def p_statements(p):
    '''
    statements :  statements statement
    |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        statements = p[1]
        statements.append(p[2]) 
        p[0] = statements


def p_statement(p):
    '''
    statement : ID modOp exp
    | NEW type ID
    | CALL ID WCOLON ID LPAREN RPAREN
    | UNCALL ID WCOLON ID LPAREN RPAREN
    '''
    if len(p) == 4:
        if p[1] == 'new':
            p[0] = [p[1], p[2], p[3]]
        else:
            p[0] = [p[2], p[1], p[3]]
    elif len(p) == 7:
        p[0] = [p[1],p[2], p[4]]





def p_modOp(p):
    '''
    modOp : MODADD 
    | MODSUB 
    | MODXOR
    '''
    if  p[1] == '+=':
        p[0] =  "+=" 
    elif p[1] == '-=':
        p[0] =  "-="
    elif p[1] == '^=':
        p[0] = '^='

def p_exp(p):
    '''
    exp : NUMBER
    | exp MUL exp
    | exp DIV exp
    | exp ADD exp
    | exp SUB exp
    '''

    if (len(p) == 2):
        p[0] = int(p[1])
    elif (len(p) == 4):
        if  p[2] == '+':
            p[0] = [int(p[1]), "+" ,int(p[3])]
        elif p[2] == '-':
            p[0] = [int(p[1]), "-" ,int(p[3])]
        elif p[2] == '*':
            p[0] = [int(p[1]), "*" ,int(p[3])]
        elif p[2] == '/':
            p[0] = [int(p[1]), "/" ,int(p[3])]
        elif p[2] == '%':
            p[0] = [int(p[1]), "%" ,int(p[3])]


def yacc_test():
    f = open('test.rplpp', 'r')
    data = f.read()
    f.close()

    parser = yacc.yacc()
    result = parser.parse(data)
    evalProg(classMap)
    
    print('result: ', result)


if __name__ == '__main__':
    yacc_test()











