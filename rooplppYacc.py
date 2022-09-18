# -*- encoding: utf-8 -*-

import ply.yacc as yacc

from rooplppLexer import tokens


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
    class : CLASS className 
    '''

def p_className(p):
    '''
    className :  ID 
    '''

"""
def p_varDeclarations(p):
    '''
    varDeclarations : varDeclarations varDeclaration
    | 
    '''

def p_varDeclaration(p):
    '''
    varDeclaration : type varName 
    '''

def p_methods(p):
    '''
    methods  : methods method 
    | 
    '''


def p_method(p):
    '''
    method : METHOD ID  LPAREN RPAREN COLON statements
    '''


def p_statements(p):
    '''
    statements : statement 
    | statement statements
    '''


def p_statement(p):
    '''
    statement : ID modOp exp
    '''

def p_modOp(p):
    '''
    modOp : MODADD 
    | MODSUB 
    | MODXOR
    '''

def p_exp(p):
    '''
    exp : NUMBER
    | exp MUL exp
    | exp DIV exp
    | exp ADD exp
    | exp SUB exp
    '''


def p_varName(p):
    '''
    varName :  ID 
    '''




def p_type(p):
    '''
    type : INT 
    | className
    '''

"""

def yacc_test():
    f = open('test.rplpp', 'r')
    data = f.read()
    f.close()

    parser = yacc.yacc()
    result = parser.parse(data)
    print('result: ', result)


if __name__ == '__main__':
    yacc_test()












