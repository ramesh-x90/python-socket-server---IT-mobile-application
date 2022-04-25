
import threading


def creatFilethread(path : str  , byts : bytearray):
    f = open(path , "wb")
    f.write(byts)
    f.close()


def creatFile(path : str  , byts : bytearray):
    threading.Thread(target= (creatFilethread)  , args=(path , byts ,)).start()



