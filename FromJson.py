import json
import userReq.UserReqs as UserReq


def json2obj(jsonString: str):
    try:
        json_dict = json.loads(jsonString)
    except Exception as identifier:
        return

    if json_dict['reqType'] == 'logingreq':
        return UserReq.LoginReq(**json_dict)

    if json_dict['reqType'] == 'RegistrationReq':
        return UserReq.RegistrationReq(**json_dict)

    if json_dict['reqType'] == 'ReqMyUserInfo':
        return UserReq.UserReq(**json_dict)

    if json_dict['reqType'] == 'ChangeBufferSize':
        return UserReq.ChangeBufferSize(**json_dict)

    if json_dict['reqType'] == 'ReqLatestNews':
        return UserReq.UserReq(**json_dict)

    if json_dict['reqType'] == 'SendMsgReq':
        return UserReq.SendMsgReq(**json_dict)

    if json_dict['reqType'] == 'ReqCalendarInfo':
        return UserReq.UserReq(**json_dict)
    
    if json_dict['reqType'] == 'ReqCourseItems':
        return UserReq.UserReq(**json_dict)

    if json_dict['reqType'] == 'ReqCourseDocs':
        return UserReq.CourseDocsReq(**json_dict)

