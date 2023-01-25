from rooplppEval import makeStore, evalStatement

# separateを呼ばないver
def interpreter(objName, classMap, className, q, store):
    invert = False
    store = makeStore(classMap, className)
    print(store)
    print("interpreter start")
    while(True):
        if q.qsize() == 0:
            print("qsize is 0")
            continue
        else:
            request = q.get()
            methodName = request[0]
            args = request[1]
            startStatement = ['call', methodName, args]
            inv = True
            evalStatement(classMap, startStatement, store, className, invert)

    # TODO: separateを含むプログラムのclassMapを作成する
    # VScodeのデバッガが使いやすい。
    # 中間発表までに、[1,2]の順番で取得して、逆方向で[2,1]の順番で取得するようにする。
    # 目標：多くのconsumer, producerを動かしたい.
