

from Models.User import User


class ServerRespons:
    def __init__(self, Restype: str) -> None:
        self._responseType = Restype


class LoginAuthentication(ServerRespons):

    def __init__(self, type: str, varification: int, role: str) -> None:
        super().__init__(type)
        self._varification = varification
        self._role = role

    def toJson(self):
        return({
            "_responseType": self._responseType,
            "_varification": self._varification,
            '_role': self._role

        })


class RegistrationRespons(ServerRespons):

    def __init__(self, type: str, _regresult: int) -> None:
        super().__init__(type)
        self._regresult = _regresult

    def toJson(self):
        return({
            "_responseType": self._responseType,
            "_regresult": self._regresult,

        })


class SendClientBasicInforRes(ServerRespons):

    def __init__(self, type: str, user: User):
        super().__init__(type)
        self._user = user

    def toJson(self):
        return({
            "_responseType": self._responseType,
            "info": self._user.userToJsonforOtherUsers()

        })


class ResLatestNews(ServerRespons):
    def __init__(self, type: str, latestNews: list):
        super().__init__(type)
        self._latestNews = latestNews

    def toJson(self):
        return ({
            "_responseType": self._responseType,
            "_latestNews": self._latestNews,
        })


class ResSendMsgs(ServerRespons):
    def __init__(self, type: str, _sender: User, _destination: str, _data: str, _time: str):
        super().__init__(type)
        self.sender: User = _sender
        self.destination = _destination
        self.data = _data
        self.time = _time

    def toJson(self):
        return ({
            "_responseType": self._responseType,
            "_sender": self.sender.userToJsonforOtherUsers(),
            "_destination": self.destination,
            "_data": self.data,
            "_time": self.time,
        })


class ResCalendarInfo(ServerRespons):
    def __init__(self, type: str, calendarEvents: list):
        super().__init__(type)
        self._calendarEvents = calendarEvents

    def toJson(self):
        return ({
            "_responseType": self._responseType,
            "_calendarEvents": self._calendarEvents,
        })


class ResCourses(ServerRespons):
    def __init__(self, type: str, courses: list):
        super().__init__(type)
        self._courses = courses

    def toJson(self):
        return ({
            "_responseType": self._responseType,
            "courses": self._courses,
        })

class ResCoursesDocs(ServerRespons):
    def __init__(self, type: str, coursesDocs: list):
        super().__init__(type)
        self._coursesDocs = coursesDocs

    def toJson(self):
        return ({
            "_responseType": self._responseType,
            "coursesDocs": self._coursesDocs,
        })