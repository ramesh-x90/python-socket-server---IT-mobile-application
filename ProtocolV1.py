from pubSubServices import Service
import threading
from DataBase.CloudStor import CloudStore
from ServerRespons.ServerResponses import ResSendMsgs
import Worker
from Models.User import User
from DataBase.Db import Db
import json
import socket
import FromJson
import ServerRespons.ServerResponses as S_res
import fileManager.fileManager as filemanager


def hook(req, dataSoures: dict, conn: socket.socket, userDict: dict):

    # resources
    userObj : User = userDict.get('UserObj')
    userFiles: list = userDict['fileBinaryBuffer']
    mndb: Db = dataSoures['mongoDb']
    firBs: CloudStore = dataSoures['fireBase']
    users: list  = dataSoures['users']

    #
    req_obj = FromJson.json2obj(req)

    if req_obj == None:
        print('decoding failed')
        return

    # loging api
    if req_obj.reqType == 'logingreq':

        # crafting serever ServerRespons
        resType = "LoginAuthentication"
        LoginRes = -2

        database_read = Worker.findUser(mndb, req_obj.userName)

        if database_read != None:
            if database_read.get('_password') == req_obj.userPasswd:
                LoginRes = 0
            else:
                LoginRes = -1
        if LoginRes == 0:
            send(conn, S_res.LoginAuthentication(
                resType, LoginRes, database_read.get('_role')).toJson())
        else:
            send(conn, S_res.LoginAuthentication(
                resType, LoginRes,  'null').toJson())


        if LoginRes == 0:
            database_read.pop('_id')
            try:
                users.remove(userObj)
            except Exception as identifier:
                pass
            
            userDict['UserObj'] = userObj = User(**database_read)
            users.append(userObj)
            userObj.setSocket(conn)

            threading.Thread(target=(Service.clientAdded), args=( )).start()

        return

    if req_obj.reqType == 'RegistrationReq':

        database_read = Worker.findUser(mndb, req_obj.userName)
        Errorcode = -3
        resType = "RegistrationRespons"

        # varifi admin accounts for now disabled
        if database_read == None:
            if Worker.findbyEmail(mndb, req_obj.email) == None:

                userdata = User(req_obj.userName, req_obj.email,
                                req_obj.userPasswd, 'null', req_obj.role)

                print('adding a new user....')
                Errorcode = 0

                if(req_obj.profileimage == 1):
                    print('uploading user profile image')

                    picBinary = userDict['fileBinaryBuffer'].pop(0)
                    if picBinary == None:
                        print('picture binary not found')
                    else:
                        filepath = './cache/users/images/' + req_obj.userName + '.jpg'
                        uplocation = 'users/profileImages/' + req_obj.userName + '.jpg'
                        filemanager.creatFile(filepath, picBinary)
                        firBs.uploadFile(uplocation, filepath)
                        url = firBs.getFileUrl(uplocation)
                        userdata.setPicUrl(url)

                map = userdata.userToJson()
                Worker.addUserToDataBase(mndb, map)

            else:
                userFiles.clear()
                Errorcode = -1
        else:
            userFiles.clear()
            Errorcode = -2

        send(conn,  S_res.RegistrationRespons(resType, Errorcode).toJson())

    # register api

    if userObj == None:
        send(conn, {'_responseType':'unAuthorized'})
        return

    if req_obj.reqType == 'ReqMyUserInfo':
        send(conn, S_res.SendClientBasicInforRes(
            "ClientBasicInforRes", userObj).toJson())

    if req_obj.reqType == 'ReqLatestNews':
        send(conn, S_res.ResLatestNews("LatestNews",
             Worker.getlatestEvents(mndb)).toJson())

    if req_obj.reqType == 'SendMsgReq':
        respons = S_res.ResSendMsgs(
            'ChatMsg', userObj, req_obj.destination, req_obj.data, req_obj.time)
        if req_obj.destination == 'PublicChat':
            for i in users:
                if i != userObj:
                    i:User.sendAll(respons.toJson())

    if req_obj.reqType == 'ReqCalendarInfo':
        respons = S_res.ResCalendarInfo(
            "CalendarInfo", Worker.getCalendarEvents(mndb)).toJson()
        send(conn, respons)

    if req_obj.reqType == 'ReqCourseItems':
        respons = S_res.ResCourses(
            "CourseItems", Worker.getCourses(mndb)).toJson()
        send(conn, respons)

    if req_obj.reqType == 'ReqCourseDocs':
        respons = S_res.ResCoursesDocs(
            "CourseDocs", Worker.getCourseDocs(mndb , req_obj.moduleiD)).toJson()
        send(conn, respons)

def send(conn: socket.socket, dataDict):
    strData = (json.dumps(dataDict)+'[<->END<->]').encode()
    conn.sendall(strData)
    print('SERVER: ' + strData.decode())
