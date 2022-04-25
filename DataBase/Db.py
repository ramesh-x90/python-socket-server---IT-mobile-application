
import threading
import pymongo as mongoConnector
import certifi
import os


import dotenv 

dotenv.load_dotenv()



ca = certifi.where()

CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")


class Db:
    threadlock = threading.Lock()
    def __init__(self,) -> None:

        self.dbclient = mongoConnector.MongoClient(
            CONNECTION_STRING, tlsCAFile=ca)
        self.db = self.dbclient["ITappDB"]
        self.usersdbcollection = self.db["Users"]
        self.eventsCollections = self.db['Events']
        self.CalendarEventsCollections = self.db['CalendarEvents']
        self.Courses = self.db['Courses']
        self.CourseDocuments = self.db['CourseDocuments']
        

    def addAuser(self, map: dict):
        self.threadlock.acquire()
        self.usersdbcollection.insert_one(map)
        self.threadlock.release()

    def findUser(self, username: str):
        return self.usersdbcollection.find_one({'_username': username})

    def findbyEmail(self, email: str):
        return self.usersdbcollection.find_one({'_email': email})

    def getLatestEvents(self):

        List: list = []
        Dbres = self.eventsCollections.find({}, {'_id': 0})

        for item in Dbres:
            List.append(item)
        return List

    def getCalendarEvents(self):
        List = []
        Dbres = self.CalendarEventsCollections.find({}, {'_id': 0})

        for events in Dbres:
            List.append(events)
        return List

    def getCourses(self):
        List = []
        Dbres = self.Courses.find({} , {'_id':0})


        for course in Dbres:
            List.append(course)
        return List

    def getCourseDocs(self , courseId :str):
        List = []

        Dbres = self.CourseDocuments.find({'moduleiD':courseId} , {'_id':0})

        for courseDoc in Dbres:
            List.append(courseDoc)
        return List

