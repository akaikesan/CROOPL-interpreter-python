import copy
store = {}


def makeStore(classMap, className):

    st = {}
    if isinstance(className, list):  # Array
        if className[0][0] == 'int':
            st = [0] * int(className[0][1][0])
        else:
            st = [{}] * int(className[0][1][0])
    else:
        for f in classMap[className]['fields'].keys():

            if classMap[className]['fields'][f] == 'int':
                # 0 initialized
                st[f] = 0
            else:
                # TODO: ex) AクラスのfieldをAクラス内で宣言したら、エラーを出す。
                #          現在は無限再帰のpython側のエラーとなっている。
                # st[f] = makeStore(classMap, classMap[className]['fields'][f])
                st[f] = {}

    return st


def evalProg(classMap, argOption):

    if argOption == "--map":
        print(classMap)
    store = {'program': makeStore(classMap, 'Program')}

    mainMethodStatements = classMap['Program']['methods']['main']["statements"]

    startStatement = ['call', 'main', []]

    invert = False

    evalStatement(classMap, startStatement, store['program'], 'Program', invert)

    print("\nSTORE:", store)


def checkNil(object):
    if isinstance(object, int):
        return object
    if len(object) == 0:
        return {}
    elif len(object) == 1:
        if 'type' in object:
            return {}
    else:
        return object


def evalExp(thisStore, exp):
    if len(exp) == 1:  # [<int>] or [<varName>]
        if isinstance(exp[0], list):
            return thisStore[exp[0][0]]['value'][int(exp[0][1][0])]

        if exp[0].isdecimal():
            return int(exp[0])
        else:
            # keyがtypeだけのものも{}でreturnする必要がある。
            if exp[0] == 'nil':
                return {}
            return thisStore[exp[0]]
    else:
        if (exp[1] == '+'):
            return evalExp(thisStore, exp[0]) + evalExp(thisStore, exp[2])
        elif (exp[1] == '-'):
            return evalExp(thisStore, exp[0]) - evalExp(thisStore, exp[2])
        elif (exp[1] == '='):

            e1 = checkNil(evalExp(thisStore, exp[0]))
            e2 = checkNil(evalExp(thisStore, exp[2]))
            return e1 == e2

        elif (exp[1] == '!='):
            e1 = checkNil(evalExp(thisStore, exp[0]))
            e2 = checkNil(evalExp(thisStore, exp[2]))
            return e1 != e2
        elif (exp[1] == '&'):
            return evalExp(thisStore, exp[0]) and evalExp(thisStore, exp[2])


def evalStatement(classMap, statement, thisStore, thisType, invert):

    if statement is None:
        return
    if (statement[0] == 'assignment'): # p[0] = ['assignment', p[2], p[1], p[3]]
        if isinstance(statement[2][0], list):
            if (statement[1] == '+='):
                if invert:
                    thisStore[statement[2][0][0]]['value'][int(
                        statement[2][0][1][0])] -= evalExp(thisStore, statement[3])
                else:
                    thisStore[statement[2][0][0]]['value'][int(
                        statement[2][0][1][0])] += evalExp(thisStore, statement[3])

            elif (statement[1] == '-='):
                if invert:
                    thisStore[statement[2][0][0]]['value'][int(
                        statement[2][0][1][0])] += evalExp(thisStore, statement[3])
                else:
                    thisStore[statement[2][0][0]]['value'][int(
                        statement[2][0][1][0])] -= evalExp(thisStore, statement[3])

            elif (statement[1] == '^='):
                thisStore[statement[2][0][0]]['value'][int(
                    statement[2][0][1][0])] ^= evalExp(thisStore, statement[3])

            elif (statement[1] == '<=>'):
                if isinstance(statement[3][0], list):
                    rightSide = thisStore[statement[3][0][0]]['value'][int(statement[3][0][1][0])]
                else:
                    rightSide = thisStore[statement[3][0]]

                tmp = thisStore[statement[2][0][0]]['value'][int(statement[2][0][1][0])]
                thisStore[statement[2][0][0]]['value'][int(
                    statement[2][0][1][0])] = rightSide

                if isinstance(statement[3][0], list):
                    thisStore[statement[3][0][0]]['value'][int(statement[3][0][1][0])] = tmp
                else:
                    thisStore[statement[3][0]] = tmp

        else:

            if (statement[1] == '+='):
                if invert:
                     thisStore[statement[2][0]]-= evalExp(thisStore, statement[3])
                else:
                     thisStore[statement[2][0]]+= evalExp(thisStore, statement[3])

            elif (statement[1] == '-='):
                if invert:
                     thisStore[statement[2][0]]+= evalExp(thisStore, statement[3])
                else:
                     thisStore[statement[2][0]]-= evalExp(thisStore, statement[3])

            elif (statement[1] == '^='):
                 thisStore[statement[2][0]] ^= evalExp(thisStore, statement[3])

            elif (statement[1] == '<=>'):
                if isinstance(statement[3][0], list):
                    rightSide = thisStore[statement[3][0][0]]['value'][int(statement[3][0][1][0])]
                else:
                    rightSide = thisStore[statement[3][0]]

                tmp = thisStore[statement[2][0]]
                thisStore[statement[2][0]] = rightSide

                if isinstance(statement[3][0], list):
                    thisStore[statement[3][0][0]]['value'][int(statement[3][0][1][0])] = tmp
                else:
                    thisStore[statement[3][0]] = tmp


    elif (statement[0] == 'print'):

        print(evalExp(thisStore, statement[1]))

    elif (statement[0] == 'skip'):
        pass
    elif (statement[0] == 'new'):
        if invert:
            thisStore[statement[2][0]] = {}
        else:
            if isinstance(statement[1], list):
                thisStore[statement[2][0]].update(
                    {'value': makeStore(classMap, statement[1])})
            else:
                thisStore[statement[2][0]].update(
                    makeStore(classMap, statement[1]))

    elif (statement[0] == 'delete'):
        if invert:
            thisStore[statement[2][0]].update(
                makeStore(classMap, statement[1]))
        else:
            thisStore[statement[2][0]] = {}
    elif (statement[0] == 'copy'):
        if invert:
            thisStore[statement[3][0]] = {}
        else:
            # TODO: typecheck
            thisStore[statement[3][0]] = thisStore[statement[2][0]]

    elif (statement[0] == 'call' or statement[0] == 'uncall'):
        # ['call', 'tc', 'test', [args]]
        # ['call', 'test', [args]]

        if len(statement) == 4:  # call method of object
            try:  # when caller is field
                callerType = classMap[thisType]['fields'][statement[1]]
            except:  # when caller is arg or local
                callerType = thisStore[statement[1]]['type']

            callMethodInfo = classMap[callerType]['methods'][statement[2]]
            callMethodName = statement[2]
            storeToPass = copy.copy(thisStore[statement[1]])
            argsPassed = statement[3]
            returnStore = thisStore[statement[1]]
        else:  # local call
            callerType = thisType
            callMethodName = statement[1]
            callMethodInfo = classMap[callerType]['methods'][callMethodName]
            storeToPass = copy.copy(thisStore)  # 関数を実行するために必要なstore
            returnStore = thisStore
            argsPassed = statement[2]

        stmts = callMethodInfo["statements"]
        argsInfo = callMethodInfo["args"]

        for i, a in enumerate(argsInfo):
            # ex) args =  [{'name': 'a', 'type': 'int'}, {'name': 'b', 'type': 'int'}]
            try:
                storeToPass.pop(argsPassed[i])
            except:
                pass
            if a['type'] == 'int':
                storeToPass[a['name']] = thisStore[argsPassed[i]]
            else:
                storeToPass[a['name']] = thisStore[argsPassed[i]]
                storeToPass[a['name']]['type'] = a['type']

        if statement[0] == 'call':
            if invert:
                stmts = reversed(stmts)
            for stmt in stmts:
                evalStatement(classMap, stmt, storeToPass, callerType, invert)

        elif statement[0] == 'uncall':
            invert = not invert
            for stmt in reversed(stmts):
                evalStatement(classMap, stmt, storeToPass, callerType, invert)
            invert = not invert

        for i, a in enumerate(argsInfo):
            # ex) args =  [{'name': 'a', 'type': 'int'}, {'name': 'b', 'type': 'int'}]
            # これでargumentにわたした変数を更新
            thisStore[argsPassed[i]] = storeToPass[a['name']]

        # local callの場合、argument以外にmember変数も更新される可能性がある。
        # よってargument以外も更新。
        # returnStoreにあるkeyのみに更新をかける。
        for key in storeToPass.keys():
            try:
                returnStore[key]
            except:
                continue
            returnStore[key] = storeToPass[key]

    elif (statement[0] == 'if'):  # statement[1:4] = [e1, s1, s2, e2]
        if invert:
            e1 = statement[4]
            e2 = statement[1]
        else:
            e1 = statement[1]
            e2 = statement[4]

        e1 = evalExp(thisStore, e1)
        if e1:
            if invert:
                statements = reversed(statement[2])
            else:
                statements = statement[2]
        else:
            if invert:
                statements = reversed(statement[3])
            else:
                statements = statement[3]

        for s in statements:
            evalStatement(classMap, s, thisStore, thisType, invert)

    elif (statement[0] == 'from'):  # statement[1:4] = [e1, s1, s2, e2]
        if invert:
            e1 = statement[4]
            e2 = statement[1]
            s1 = statement[2]
            s2 = statement[3]
        else:
            e1 = statement[1]
            e2 = statement[4]
            s1 = statement[2]
            s2 = statement[3]

        result_e1 = evalExp(thisStore, e1)

        if not result_e1:
            raise Exception("Loop initial Condition is False")

        # initially, e1 is true.
        while result_e1:  # e1  e2

            for s in s1:  # s1  s1
                evalStatement(classMap, s, thisStore, thisType, invert)

            if evalExp(thisStore, e2):  # e2 e1
                break
            else:
                if invert:
                    for s in reversed(s2):
                        evalStatement(classMap, s, thisStore, thisType, invert)
                else:
                    for s in s2:
                        evalStatement(classMap, s, thisStore, thisType, invert)

            # after 1st loop, e1 is false.
            result_e1 = not evalExp(thisStore, e1)

            if not result_e1:
                if invert:
                    raise Exception("Loop initial Condition is False")
                else:
                    raise Exception(
                        "INVERTED : Loop initial Condition is False")

    # LOCAL:0 type:1 id:2 EQ exp:3  statements:4 DELOCAL type:5 id:6 EQ exp:7
    elif (statement[0] == 'local'):

        if invert:
            id1 = statement[6][0]
            id2 = statement[2][0]
            exp1 = statement[7]
            exp2 = statement[3]
            stmts = reversed(statement[4])
        else:
            id1 = statement[2][0]
            id2 = statement[6][0]
            exp1 = statement[3]
            exp2 = statement[7]
            stmts = statement[4]

        thisStore[id1] = evalExp(thisStore, exp1)
        if statement[1] != 'int':
            thisStore[id1]['type'] = statement[1]

        for s in stmts:
            evalStatement(classMap, s, thisStore, thisType, invert)

        try:
            thisStore[id1].pop('type')
        except:
            pass

        if thisStore[id2] == evalExp(thisStore, exp2):
            thisStore.pop(statement[6][0])
        else:
            raise Exception("delocal Error")
