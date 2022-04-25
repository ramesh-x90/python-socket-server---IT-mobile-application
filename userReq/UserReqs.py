import time


class UserReq:
    def __init__(self, reqType):
        self.reqType = reqType


class ChangeBufferSize(UserReq):
    def __init__(self, reqType, _buffersize):
        super().__init__(reqType)
        self.buffersize = _buffersize


class LoginReq(UserReq):
    def __init__(self, reqType, _username, _password):
        super().__init__(reqType)
        self.userName = _username
        self.userPasswd = _password


class RegistrationReq (UserReq):

    def __init__(self, reqType, _username, _email, _password, _profileimage, _role):
        super().__init__(reqType)
        self.userName = _username
        self.email = _email
        self.userPasswd = _password
        self.profileimage = _profileimage
        self.role = _role


class SendMsgReq (UserReq):

    def __init__(self, reqType, message: dict):
        super().__init__(reqType)
        self.sender = message['_sender']
        self.data = message['_data']
        self.destination = message['_destination']
        self.time = time.strftime('%Y-%m-%d %H:%M')

class CourseDocsReq (UserReq):

    def __init__(self, reqType, moduleiD: str):
        super().__init__(reqType)
        self.moduleiD=moduleiD
