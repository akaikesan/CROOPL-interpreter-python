store = {}


def makeStore(classMap, className):

    st = {}
    for f in classMap[className]['fields'].keys():
        if classMap[className]['fields'][f] == 'int':
            # 0 initialized
            st[f] = 0
        else:
            # TODO: ex) AクラスのfieldをAクラス内で宣言したら、エラーを出す。
            #          現在は無限再帰のpython側のエラーとなっている。
            #st[f] = makeStore(classMap, classMap[className]['fields'][f])
            pass

    return st


def evalProg(classMap):

    global invert
    invert = False
    print(classMap)
    store = {'program': makeStore(classMap, 'Program')}

    mainMethodStatements = classMap['Program']['methods']['main']

    for statement in mainMethodStatements:
        evalStatement(classMap, statement, store['program'], 'Program')

    print("\nSTORE:", store)


def evalExp(exp):
    if type(exp) is int:
        return exp
    else:
        if (exp[1] == '+'):
            return evalExp(exp[0]) + evalExp(exp[2])
        elif (exp[1] == '-'):
            return evalExp(exp[0]) - evalExp(exp[2])


def evalStatement(classMap, statement, thisStore, thisType):

    global invert
    if (statement[0] == '+='):
        if invert:
            thisStore[statement[1]] -= evalExp(statement[2])
        else:
            thisStore[statement[1]] += evalExp(statement[2])
    elif (statement[0] == '-='):
        if invert:
            thisStore[statement[1]] += evalExp(statement[2])
        else:
            thisStore[statement[1]] -= evalExp(statement[2])
    elif (statement[0] == '^='):
        thisStore[statement[1]] ^= evalExp(statement[2])
    elif (statement[0] == 'new'):
        thisStore[statement[2]] = makeStore(classMap, statement[1])
    elif (statement[0] == 'call'): # ['call', 'tc', 'test']
        calleeType = classMap[thisType]['fields'][statement[1]]
        stmts = classMap[calleeType]['methods'][statement[2]]
        for stmt in stmts:
            evalStatement(classMap, stmt, thisStore[statement[1]], calleeType)
    elif (statement[0] == 'uncall'): # ['call', 'tc', 'test']
        invert = True
        calleeType = classMap[thisType]['fields'][statement[1]]
        stmts = classMap[calleeType]['methods'][statement[2]]
        for stmt in stmts:
            evalStatement(classMap, stmt, thisStore[statement[1]], calleeType)
        invert = False

