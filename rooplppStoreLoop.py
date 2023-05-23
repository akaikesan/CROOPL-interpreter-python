import multiprocessing as mp
import time


def assignVarAndGetDictByAddress(dic, p, varName, value, sep="/"):
    lis = p.split(sep)
    def _(dic, lis, sep):
        if len(lis) == 0:
            return 
        if len(lis) == 1:
            if isinstance(varName, list):
                index = int(varName[1][0])
                dic[lis[0]][varName[0]][index] = value
            else:
                dic[lis[0]][varName] = value 
        else:
            _(dic.get(lis[0], {}), lis[1:], sep)
    _(dic, lis, sep=sep)

def storeCycle(q, globalStore):

    print("store Is Available")

    global m
    m = mp.Manager()


    while(True):
        
        try:
            q.qsize()
        except:
            raise Exception("store error")

        if q.qsize() != 0:
            request = q.get()

            if(len(request) == 4):
                if(request[0] == "update"):
                #update
                    objName = request[1]
                    varName = request[2]
                    value = request[3]

                    if isinstance(varName, list):
                        proxy = globalStore[objName]
                        try:
                            index = int(varName[1][0])
                        except:
                            raise Exception('List index must be int')
                        proxy[varName[0]][index] = value
                        globalStore[objName] = proxy
                    else:
                        proxy = globalStore[objName]
                        proxy[varName] = value
                        globalStore[objName] = proxy

                if(request[0] == "updatePath"):
                    #updateByPath
                    storePath = request[1]
                    varName = request[2]
                    value = request[3]

                    l = storePath.split('/')
                    callerObjName = l[0]

                    tmpCaller = globalStore[callerObjName]
                    copyGlobalStore = { callerObjName : tmpCaller}

                    assignVarAndGetDictByAddress(copyGlobalStore, 
                                                 storePath, 
                                                 varName, 
                                                 value)

                    globalStore[callerObjName] = copyGlobalStore[callerObjName]


            elif(len(request) == 3):
                if(request[0] == "deletePath"):
                    storePath = request[1]
                    varName = request[2]

        time.sleep(2)
        print(globalStore)

def makeSeparatedStore( globalStore, m):

    print("making Store")
    q = m.Queue()

    globalStore['#Store'] = {'#q': q}
    p = mp.Process(target =  storeCycle, args = (q, globalStore))

    time.sleep(0.2)
    p.start()
