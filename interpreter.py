from rooplppEval import makeStore, evalStatement

# separateを呼ばないver
def interpreter(objName, classMap, className, q, store):
    invert = False
    store = makeStore(classMap, className)
    print(store)
    print("interpreter start")
    while(True):
        if q.qsize() == 0:
            continue
        else:
            request = q.get()
            methodName = request[0]
            args = request[1]
            startStatement = ['call', methodName, args]
            inv = True
            evalStatement(classMap, startStatement, store, className, invert)
            break

