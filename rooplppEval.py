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

    mainMethodStatements = classMap['Program']['methods']['main']["statements"]

    for statement in mainMethodStatements:
        evalStatement(classMap, statement, store['program'], 'Program')

    print("\nSTORE:", store)


def evalExp(thisStore, exp):
    if len(exp) == 1:  # [<int>] or [<varName>]
        if exp[0].isdecimal():
            return int(exp[0])
        else:
            return thisStore[exp[0]]
    else:
        if (exp[1] == '+'):
            return evalExp(thisStore, exp[0]) + evalExp(thisStore, exp[2])
        elif (exp[1] == '-'):
            return evalExp(thisStore, exp[0]) - evalExp(thisStore, exp[2])
        elif (exp[1] == '='):
            return evalExp(thisStore, exp[0]) == evalExp(thisStore, exp[2])
        elif (exp[1] == '!='):
            return evalExp(thisStore, exp[0]) != evalExp(thisStore, exp[2])
        elif (exp[1] == '&'):
            return evalExp(thisStore, exp[0]) and evalExp(thisStore, exp[2])


def evalStatement(classMap, statement, thisStore, thisType):
    
    global invert
    if (statement[0] == '+='):
        if invert:
            thisStore[statement[1]] -= evalExp(thisStore, statement[2])
        else:
            thisStore[statement[1]] += evalExp(thisStore, statement[2])
    elif (statement[0] == '-='):
        if invert:
            thisStore[statement[1]] += evalExp(thisStore, statement[2])
        else:
            thisStore[statement[1]] -= evalExp(thisStore, statement[2])
    elif (statement[0] == '^='):
        thisStore[statement[1]] ^= evalExp(thisStore, statement[2])
    elif (statement[0] == 'new'):
        thisStore[statement[2]] = makeStore(classMap, statement[1])

    elif (statement[0] == 'call' or statement[0] == 'uncall'):
        # ['call', 'tc', 'test', [args]]

        try: # when caller is field
            callerType = classMap[thisType]['fields'][statement[1]]
        except:# when caller is arg
            callerType = thisStore[statement[1]]['type']

        callMethod = classMap[callerType]['methods'][statement[2]]
        stmts = callMethod["statements"]
        args = callMethod["args"]

        for i, a in enumerate(args):
            # ex) args =  [{'name': 'a', 'type': 'int'}, {'name': 'b', 'type': 'int'}]
            if a['type'] == 'int':
                thisStore[statement[1]][a['name']] = thisStore[statement[3][i]]
            else:
                thisStore[statement[1]][a['name']] = thisStore[statement[3][i]]
                thisStore[statement[1]][a['name']]['type'] = a['type']



        if statement[0] == 'call' :
            for stmt in stmts:
                evalStatement(classMap, stmt, thisStore[statement[1]], callerType)
        if statement[0] == 'uncall' :
            invert = True
            for stmt in reversed(stmts):
                evalStatement(classMap, stmt, thisStore[statement[1]], callerType)
            invert = False

        for i, a in enumerate(args):
            # ex) args =  [{'name': 'a', 'type': 'int'}, {'name': 'b', 'type': 'int'}]
            if a['type'] == 'int':
                thisStore[statement[3][i]] = thisStore[statement[1]][a['name']]
                thisStore[statement[1]].pop(a['name'])
            else:
                thisStore[statement[1]][a['name']].pop('type')
                thisStore[statement[3][i]] = thisStore[statement[1]][a['name']]
                thisStore[statement[1]].pop(a['name'])

    elif (statement[0] == 'if'):  # statement[1:4] = [e1, s1, s2, e2]
        if invert :
            e1 = statement[4]
            e2 = statement[1]
        else:
            e1 = statement[1]
            e2 = statement[4]

        e1 = evalExp(thisStore, e1)
        if e1 :
            if invert :
                statements = reversed(statement[2])
            else:
                statements = statement[2]
        else:
            if invert :
                statements = reversed(statement[3])
            else:
                statements = statement[3]

        for s in statements:
            evalStatement(classMap, s, thisStore, thisType)

    elif (statement[0] == 'from'):  # statement[1:4] = [e1, s1, s2, e2]
        if invert :
            e1 = statement[4]
            e2 = statement[1]
        else:
            e1 = statement[1]
            e2 = statement[4]

        result_e1 = evalExp(thisStore, e1)

        if not result_e1:
            raise Exception("Loop initial Condition is False")

        # initially, e1 is true.
        while result_e1:


            for s in statement[2]:
                evalStatement(classMap, s, thisStore, thisType)

            if evalExp(thisStore, e2):
                break
            else:
                for s in statement[3]:
                    evalStatement(classMap, s, thisStore, thisType)

            # after 1st loop, e1 is false.
            result_e1 = not evalExp(thisStore, e1)

            if not result_e1:
                if invert:
                    raise Exception("Loop initial Condition is False")
                else:
                    raise Exception("INVERTED : Loop initial Condition is False")




