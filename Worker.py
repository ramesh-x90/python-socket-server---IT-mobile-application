import threading
from DataBase.Db import Db


def addUserToDataBase(DataBase: Db, map: dict):
    t = threading.Thread(target=(DataBase.addAuser), args=(map, ))
    t.start()


def findUser(DataBase: Db, uname: str):
    # t = threading.Thread(target=(DataBase.finduser) , args=(map, ))
    # t.start()

    return DataBase.findUser(uname)


def findbyEmail(DataBase: Db, email: str):
    # t = threading.Thread(target=(DataBase.finduser) , args=(map, ))
    # t.start()

    return DataBase.findbyEmail(email)


def getlatestEvents(DataBase: Db):
    return DataBase.getLatestEvents()


def getCalendarEvents(DataBase: Db):
    return DataBase.getCalendarEvents()


def getCourses(DataBase: Db):
    return DataBase.getCourses()


def getCourseDocs(DataBase: Db , moduleiD : str):
    return DataBase.getCourseDocs(moduleiD)
