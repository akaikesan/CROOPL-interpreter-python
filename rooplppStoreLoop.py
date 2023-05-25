import multiprocessing as mp
import time


def popVarOfDict(dic, p, varName, sep="/"):
    lis = p.split(sep)
    def _(dic, lis, sep):
        if len(lis) == 0:
            return 
        if len(lis) == 1:
            if isinstance(varName, list):
                dic[lis[0]].pop(varName[0])
            else:
                dic[lis[0]].pop(varName)
        else:
            _(dic.get(lis[0], {}), lis[1:], sep)
    _(dic, lis, sep=sep)

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



def reflectArgsAndGetDictByAddress(dic, p, result, sep="/"):
    lis = p.split(sep)
    def _(dic, lis, result, sep, default):
        if len(lis) == 0:
            return 
        if len(lis) == 1:
            for k in result.keys():
                dic[lis[0]][k] = result[k]
        else:
            _(dic.get(lis[0], {}), lis[1:], result ,sep, default)
    _(dic, lis, result, sep=sep, default=None)
    return dic



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

            if(len(request) == 7):
                if (request[0] == "reflectArgsPassedSeparated"):
                    print("reflectArgsPassedSeparated")

                    # object that called
                    callerObjName = request[1]
                    # object that is called
                    calledObjName = request[2]  
                    argsInfo = request[3] 
                    passedArgs = request[4] 
                    dictAddress = request[5] 
                    
                    tmpCaller = globalStore[callerObjName]
                    tmpCaller = { callerObjName : tmpCaller}

                    tmpThis = globalStore[calledObjName]
                    result = {} 
                    for i, a in enumerate(argsInfo):
                        result[passedArgs[i]] = globalStore[calledObjName][a['name']]
                        tmpThis.pop(a['name'])



                    # must be synchronized

                    globalStore[calledObjName] = tmpThis
                    globalStore[callerObjName] = reflectArgsAndGetDictByAddress(tmpCaller, dictAddress, result)[callerObjName]
                print('send')
                request[6].send('signal')

            if(len(request) == 6):
                if (request[0] == "reflectArgsPassed"):
                    print("reflectArgsPassed")

                    # object that called
                    callerObjName = request[1]
                    # object that is called
                    calledObjName = request[2]  
                    argsInfo = request[3] 
                    passedArgs = request[4] 

                    tmp = globalStore[callerObjName]
                    for i, k in enumerate(passedArgs):


                        if k in globalStore[callerObjName].keys():
                             tmp[k] = globalStore[callerObjName][calledObjName][argsInfo[i]['name']]
                             tmp[calledObjName].pop(argsInfo[i]['name'])

                        globalStore[callerObjName] = tmp  
                    
                print('send')
                request[5].send('signal')
                

            if(len(request) == 5):

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
                    print("updateByPath")
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

                print('send')
                request[4].send('signal')

            elif(len(request) == 4):
                # deleteByPath
                if(request[0] == "deletePath"):
                    storePath = request[1]
                    varName = request[2]

                    l = storePath.split('/')
                    callerObjName = l[0]

                    tmpCaller = globalStore[callerObjName]
                    copyGlobalStore = { callerObjName : tmpCaller}

                    popVarOfDict(copyGlobalStore, storePath, varName)

                    globalStore[callerObjName] = copyGlobalStore[callerObjName]
                    print('deleteByPath')
                

                elif(request[0] == "delete"):

                    envObjName = request[1]
                    id1 = request[2]

                    tmp = globalStore[envObjName]
                    tmp.pop(id1)
                    globalStore[envObjName] = tmp

                print('send')
                request[3].send('signal')
                


        time.sleep(0.1)

def makeSeparatedStore( globalStore, m):

    print("making Store")
    q = m.Queue()

    globalStore['#Store'] = q
    p = mp.Process(target =  storeCycle, args = (q, globalStore))

    time.sleep(0.2)
    p.start()
