"""
>pip install oss2 -i https://mirrors.aliyun.com/pypi/simple
>pip install aliyun-python-sdk-core -i https://mirrors.aliyun.com/pypi/simple
>pip install aliyun-python-sdk-sts -i https://mirrors.aliyun.com/pypi/simple
>pip install alibabacloud_dysmsapi20170525 alibabacloud_tea_openapi alibabacloud_tea_util
"""
import json
import os
import time
import uuid
import queue
import hashlib
import logging
import threading
import requests
from . import pluginDB , pluginOssBucket
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models

logger = logging.getLogger('pluginBkSignup')

# NOTE: 会话过期时间（秒），默认 2 小时
SESSION_TTL = int(os.getenv('SESSION_TTL', '7200'))
# NOTE: 短信发送最小间隔（秒），防止恶意刷短信
SMS_MIN_INTERVAL = int(os.getenv('SMS_MIN_INTERVAL', '60'))


"""
error code 
1000 sessionId error.
1001 发送短信次数超限 .
1002 发送短信失败
1003 未登录
1004 电话号码与会话ID不一致

2000 参赛队名不能为空
2001 参赛队名不能重复
2002 项目代码错误
2003 年龄组错误
2004 赛区错误


3000 TeamKey 错误
3001 function错误
3002 gender错误
3003 idTypeCode错误
3004 运动员重复报名
3005 错误
3006 memkey错误

4000 memKey 错误
4001 memKey 与 tel 不匹配
"""

class TBkSignup2024Data:
    def __init__(self  ):
        self.gameInfo ={}
        self.dictAge ={}
        self.dictArea ={}
        self.dictCheckReason ={}
        self.dictCheckStatus ={}
        self.dictFunction ={}
        self.dictGender ={}
        self.dictID ={}
        self.dictPhase ={}
        self.dictSignupStatus ={}
        self.dictEvent ={}
        self.sessions ={}
        self.users ={}
        self.teams ={}
        self.teamMembers ={}
        self.athIds ={}
        self._user_teams_idx = {}
        self._team_mems_idx = {}

    def _build_indexes(self):
        self._user_teams_idx.clear()
        self._team_mems_idx.clear()
        for t in self.teams.values():
            tel = t.get('createUserCode')
            if tel:
                self._user_teams_idx.setdefault(tel, set()).add(t['teamKey'])
        for m in self.teamMembers.values():
            tCode = m.get('teamCode')
            if tCode:
                self._team_mems_idx.setdefault(tCode, set()).add(m['memKey'])

    def _add_team_index(self, tel, teamKey):
        self._user_teams_idx.setdefault(tel, set()).add(teamKey)

    def _add_member_index(self, teamCode, memKey):
        self._team_mems_idx.setdefault(teamCode, set()).add(memKey)

    def _remove_member_index(self, teamCode, memKey):
        if teamCode in self._team_mems_idx:
            self._team_mems_idx[teamCode].discard(memKey)

    def getExportData(self):
        exportPath = ""
        content = ""
        try:
            exportPath = "/".join([
                "bksignup2024",
                self.gameInfo.get('gameCode', ''),
                "gameInfo.txt"
            ])
            exportData =  {
                "gameInfo": self.gameInfo,
                "dicts":{
                    "age": self.dictAge,
                    "area": self.dictArea ,
                    "function": self.dictFunction ,
                    "event":self.dictEvent ,
                    "signupStatus":self.dictSignupStatus ,
                    "phase":self.dictPhase ,
                    "gender":self.dictGender ,
                    "idType":self.dictID
                }
            }
            content = json.dumps(exportData , ensure_ascii=False)
        except Exception as er :
            logger.error('getExportData error: %s', er)
        return  exportPath , content

    def getUserData(self , tel ):
        exportPath = ""
        exportData = None
        try:
            teamList = []
            memList = []
            if not self._user_teams_idx and self.teams:
                self._build_indexes()

            teamKeys = self._user_teams_idx.get(tel, set())
            for tk in teamKeys:
                t = self.teams.get(tk)
                if t:
                    teamList.append(t)
                    memKeys = self._team_mems_idx.get(tk, set())
                    for mk in memKeys:
                        m = self.teamMembers.get(mk)
                        if m:
                            memList.append(m)

            exportPath = "/".join([
                "bksignup2024",
                self.gameInfo.get('gameCode', ''),
                "users",
                tel+".txt"
            ])
            exportData =  {
                "teams": teamList,
                "members": memList
            }
        except Exception as er :
            logger.error('getUserData error: %s', er)
        return  exportPath , exportData

class TBkSignup:
    def __init__(self , acRouter):
        self.acRouter = acRouter
        self.dbCode = ""
        self.ossBucketCode=""
        self.bucketName = ""

        self.datas = TBkSignup2024Data()
        self.db = pluginDB.TPyDB(None)
        self.ossBucket = pluginOssBucket.TPyOssBucket(None)

        self.dbBuffer = queue.Queue()
        self.loopStatus = False
        self.dbThreadLock = threading.Lock()
        self.dataLock = threading.RLock()
        # NOTE: 短信发送限频记录 {tel: last_send_timestamp}
        self._sms_rate_limit = {}
    def setSettings(self, dbCode , ossBucketCode , bucketName):
        try:
            self.dbCode = dbCode
            self.ossBucketCode = ossBucketCode
            self.bucketName = bucketName
        except Exception as er:
            print(er)
    def getDB(self):
        res = self.db
        try:
            if res.acRouter==None :
                res = self.acRouter.plugins['db']
        except Exception as er:
            print(er)
        return  res
    def getOssBucket(self):
        res = self.ossBucket
        try:
            if res.acRouter==None :
                res = self.acRouter.plugins['ossBucket']
        except Exception as er:
            print(er)
        return  res
    def sendSmsvalid(self , tel , data):
        res = ''
        status = 0
        try:
            from config import svrConfig
            sms_key = svrConfig.get('sms', {}).get('juhe_key', '')
            if not sms_key:
                logger.error('SMS juhe_key not configured')
                status = 1002
                return res, status
            status = 1
            url = "http://v.juhe.cn/sms/send"
            url = url + "?mobile=" + tel
            url = url + "&tpl_id=265035"
            url = url + "&tpl_value=%23code%23%3D"+str(data)
            url = url + "&key=" + sms_key
            url = url + "&ext="
            url = url + "&dtype=json"

            res = requests.get(
                url=url,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=10
            )
            logger.info('SMS sent to %s, status: %s', tel, res.status_code)
        except Exception as er:
            logger.error('sendSmsvalid error: %s', er)
        return  res , status
    def sendAliSmsvalid(self, tel, data):
        res = ''
        status = 0
        try:
            # NOTE: 从配置中读取阿里云 AK/SK，不再硬编码
            from config import svrConfig
            sms_cfg = svrConfig.get('sms', {})
            ali_ak = sms_cfg.get('ali_ak', '')
            ali_sk = sms_cfg.get('ali_sk', '')
            ali_sign = sms_cfg.get('ali_sign_name', '')
            ali_tpl = sms_cfg.get('ali_template_code', '')
            if not ali_ak or not ali_sk:
                logger.error('Ali SMS AK/SK not configured')
                status = 1002
                return res, status
            config = open_api_models.Config(
                access_key_id=ali_ak,
                access_key_secret=ali_sk,
                endpoint='dysmsapi.aliyuncs.com'
            )
            client = Dysmsapi20170525Client(config)
            send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
                phone_numbers=tel,
                sign_name=ali_sign,
                template_code=ali_tpl,
                template_param=f'{{"code":"{data}"}}'
            )
            runtime = util_models.RuntimeOptions()
            response = client.send_sms_with_options(send_sms_request, runtime)
            res = response.body
            if res.code == 'OK':
                status = 1
            else:
                status = 1002
            logger.info('Ali SMS sent to %s, result: %s', tel, res.code)
        except Exception as er:
            logger.error('sendAliSmsvalid error: %s', er)
            status = 1002
        return res, status
    def putDbBuffer(self , key , params):
        try:
            self.dbBuffer.put({
                'k':key,
                'ps':params
            })
            self.startDBAsync()
        except Exception as er:
            logger.error('putDbBuffer error: %s', er)
    def _check_sms_rate_limit(self, tel):
        """
        短信发送限频检查，防止同一号码被恶意刷短信。
        """
        now = time.time()
        last_send = self._sms_rate_limit.get(tel, 0)
        if now - last_send < SMS_MIN_INTERVAL:
            return False
        self._sms_rate_limit[tel] = now
        return True
    def checkEnable_sendSms(self, tel):
        status = 0
        try:
            status = 1
        except Exception as er:
            logger.warning('checkEnable_sendSms error: %s', er)
        return status
    def check_sessionTel(self, sessionId , tel ):
        status = 1000
        try:
            if sessionId in self.datas.sessions.keys() :
                session = self.datas.sessions[sessionId]
                # NOTE: 会话过期检查，超过 SESSION_TTL 秒则视为过期
                login_time = session.get('loginTime', 0)
                if login_time > 0 and (time.time() - login_time) > SESSION_TTL:
                    # 清理过期会话
                    del self.datas.sessions[sessionId]
                    status = 1005  # 会话已过期
                elif 'tel' in session.keys() :
                    if session['tel'] == tel:
                        status = 1
                    else:
                        status = 1004
                else:
                    status = 1003
        except Exception as er:
            logger.error('check_sessionTel error: %s', er)
        return status
    def check_createTeam(self, sessionId , tel , teamName , eventCode ,  areaCode , phaseCode ):
        status = 0
        try:
            status = self.check_sessionTel(sessionId , tel)
            if  status== 1 :
                if teamName in self.datas.teamsByName.keys():
                    status = 2002
                elif eventCode not in self.datas.dictEvent.keys():
                    status = 2003
                elif areaCode not in self.datas.dictArea.keys():
                    status = 2004
                else:
                    status = 1
        except Exception as er:
            print(er)
        return status
    def checkEnable_createMember(self, sessionId , tel , teamKey , memberName , functionCode , genderCode , idTypeCode , idCode):
        status = 0
        try:
            status = self.check_sessionTel(sessionId , tel)
            if  status== 1 :
                if teamKey not in self.datas.teams.keys():
                    status = 3000
                elif functionCode not in self.datas.dictFunction.keys():
                    status = 3001
                elif genderCode not in self.datas.dictGender.keys():
                    status = 3002
                elif idTypeCode not in self.datas.dictID.keys():
                    status = 3003
                elif functionCode=='01' and idCode in self.datas.athIds.keys():
                    status = 3004
                else:
                    status = 1
        except Exception as er:
            print(er)
        return  status
    def checkEnable_editMember(self, sessionId , tel , memeKey , memberName , functionCode , genderCode , idTypeCode, idCode ):
        status = 0
        try:
            status = self.check_sessionTel(sessionId , tel)
            if  status== 1 :
                if memeKey not in self.datas.teamMembers.keys():
                    status = 3006
                elif functionCode not in self.datas.dictFunction.keys():
                    status = 3001
                elif genderCode not in self.datas.dictGender.keys():
                    status = 3002
                elif idTypeCode not in self.datas.dictID.keys():
                    status = 3003
                elif functionCode=='01' and idCode in self.datas.athIds.keys():
                    member = self.datas.teamMembers[memeKey]
                    if member['idCode'] != idCode:
                        status = 3004
        except Exception as er:
            print(er)
        return  status

    def initSysData(self):
        try:
            self.datas = TBkSignup2024Data()
            db = self.getDB()
            dbKey = "sysData/baseData"
            ps={}
            dataRes = db.queryByKey(self.dbCode , dbKey , ps)
            datasetList = dataRes['datasetList']
            offset = 0
            self.datas.gameInfo = datasetList[offset][0]
            offset = offset + 1
            def list2dict(listObj , keyField):
                resDict = {}
                for item in listObj:
                    try:
                        resDict[item[keyField]] = item
                    except Exception as erItem:
                        print(erItem)
                return resDict
            self.datas.dictAge = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.dictArea = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.dictCheckReason = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.dictCheckStatus = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.dictFunction = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.dictGender = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.dictID = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.dictPhase = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.dictSignupStatus = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.dictEvent = list2dict(datasetList[offset] , 'dictCode')
            offset = offset + 1
            self.datas.users = list2dict(datasetList[offset], 'tel')
            offset = offset + 1
            self.datas.teams = list2dict(datasetList[offset], 'teamKey')
            self.datas.teamsByName = list2dict(datasetList[offset], 'teamName')
            offset = offset + 1
            self.datas.teamMembers = list2dict(datasetList[offset], 'memKey')
            aths =[x for x in   datasetList[offset] if x['functionCode']=='01']
            self.datas.athIds = list2dict(aths, 'idCode')
            offset = offset + 1
            self.datas.sessions = list2dict(datasetList[offset], 'sessionId')
            offset = offset + 1
            self.datas._build_indexes()
            logger.info('load sys datas and built indexes.')
        except Exception as er:
            logger.error('initSysData error: %s', er)
    def exportGameData(self):
        try:
            self.initSysData()
            dataPath , content = self.datas.getExportData()
            self.getOssBucket().bucketWrite(
                self.ossBucketCode ,
                self.bucketName ,
                dataPath,
                content
            )
            logger.info('exportGameData to OSS complete')
        except Exception as er:
            logger.error('exportGameData error: %s', er)
    # session user
    def session_create(self ):
        res ={}
        status = 0
        try:
            with self.dataLock:
                sid = str(uuid.uuid4()).replace('-','')
                res['sessionId'] = sid
                self.datas.sessions[sid] = {
                    'sessionId': sid
                }
                status = 1
            if status == 1:
                self.putDbBuffer('sysData/createSession', res)
        except Exception as er:
            print(er)
        return res , status
    def session_valid(self , sessionId ,  tel):
        res ={}
        status = 0
        try:
            if sessionId in self.datas.sessions.keys() :
                # NOTE: 短信限频检查
                if not self._check_sms_rate_limit(tel):
                    status = 1001
                    return res, status
                code = '000000'+str( int(time.time()) % 1000000 )
                code = code[-6:]
                # NOTE: 移除硬编码测试后门，生产环境不允许跳过短信验证
                sendRes , status = self.sendAliSmsvalid(tel , code)
                if status==1 :
                    s = sessionId +'.'+ tel+'.'+ code
                    sec = hashlib.md5(s.encode(encoding='utf-8')).hexdigest()
                    res ={
                        "sessionId": sessionId ,
                        "tel":tel,
                        "sec": sec
                    }
                    session = self.datas.sessions[sessionId]
                    session["validCode"]= code
                    session["tel"] = tel
                    session["sec"] = sec
                    # NOTE: 记录会话创建时间，用于过期检查
                    session["loginTime"] = time.time()
                    postData ={
                        "sessionId": sessionId ,
                        'tel': tel,
                        "sec": sec,
                        "code": code
                    }
                    # NOTE: 不再打印验证码明文到日志，避免敏感信息泄露
                    logger.info('SMS valid sent to %s', tel)
                    self.putDbBuffer('sysData/updateSession', postData)
            else:
                status = 1000
        except Exception as er:
            logger.error('session_valid error: %s', er)
        return res , status
    def session_checkLogin(self , sessionId , tel , validCode):
        status = 0
        try:
            if (
                    sessionId in self.datas.sessions.keys() and
                    'tel' in self.datas.sessions[sessionId].keys() and
                    self.datas.sessions[sessionId]['tel'] ==  tel
            ):
                session = self.datas.sessions[sessionId]
                if session['validCode'] == str(validCode):
                    status = 1
            else:
                status = 1000
        except Exception as er:
            print(er)
        return  status
    def session_updateUserData(self , tel ):
        res ={
            "ac":"executeUserData"
        }
        status = 0
        try:
            with self.dataLock:
                # 锁内仅做内存数据获取，耗时极短
                dataPath , exportData = self.datas.getUserData(tel)

            if exportData is not None:
                # 锁外执行耗时的 JSON 序列化和网络 OSS 写入
                content = json.dumps(exportData, ensure_ascii=False)
                self.getOssBucket().bucketWrite(
                    self.ossBucketCode ,
                    self.bucketName ,
                    dataPath,
                    content
                )
                status = 1
                logger.debug('update user data end: %s', dataPath)
        except Exception as er:
            logger.error('session_updateUserData error: %s', er)
        return res , status

    #team
    def team_create(self, sessionId , tel , teamName , eventCode , areaCode , phaseCode , logoImg):
        res ={}
        status = 0
        try:
            with self.dataLock:
                status = self.check_createTeam(sessionId, tel, teamName, eventCode,  areaCode , phaseCode )
                if status==1 :
                    session = self.datas.sessions[sessionId]
                    teamKey = str(uuid.uuid4()).replace('-','')
                    res = {
                        "createUserCode": session['tel'],
                        "eventCode": eventCode,
                        "phaseCode": phaseCode,
                        "areaCode": areaCode,
                        "teamName": teamName,
                        "teamKey": teamKey ,
                        "logoImg": logoImg,
                        "signupStatusCode": '0',
                        "checkStatusCode" : "0"
                    }
                    self.datas.teams[teamKey] = res
                    self.datas.teamsByName[teamName] = res
                    self.datas._add_team_index(session['tel'], teamKey)
            if status == 1:
                self.putDbBuffer('sysData/createTeam', res)
                self.session_updateUserData(tel)
        except Exception as er:
            logger.error('team_create error: %s', er)
        return res , status
    #member
    def team_setSignupStatus(self, sessionId, tel, teamKey, teamStatus):
        res = {}
        status = 0
        try:
            status = self.check_sessionTel(sessionId, tel)
            if status == 1:
                if teamKey in self.datas.teams.keys():
                    team = self.datas.teams[teamKey]
                    team['signupStatusCode'] = teamStatus
                    self.putDbBuffer('sysData/updateTeamSignupStaus', {
                        "teamKey": teamKey,
                        "signupStatus": team['signupStatusCode']
                    })
                    createUserCode = team['createUserCode']
                    self.session_updateUserData(createUserCode)
                    res = {
                        "teamKey": teamKey,
                        "signupStatus": teamStatus
                    }
                    status = 1
                else:
                    status = 3000
            else:
                status = 1000
        except Exception as er:
            print(er)
        return res, status

    def team_setSignupStatus_admin(self,   teamKey, teamStatus , teamExInfo):
        res = {}
        status = 0
        try:
            if teamKey in self.datas.teams.keys():
                team = self.datas.teams[teamKey]
                team['signupStatusCode'] = teamStatus
                createUserCode = team['createUserCode']
                self.session_updateUserData(createUserCode)
                self.putDbBuffer('sysData/updateTeamSignupStausAdmin', {
                    "teamKey": teamKey,
                    "signupStatus": team['signupStatusCode'],
                    'teamExInfo':teamExInfo
                })
                res = {
                    "teamKey": teamKey,
                    "signupStatus": teamStatus
                }
                status = 1
            else:
                status = 3000
        except Exception as er:
            print(er)
        return res, status

    def team_setWxPayStatus(self,   teamKey, payStatus , transaction_id, openid):
        res = {}
        status = 0
        try:
            if teamKey in self.datas.teams.keys():
                team = self.datas.teams[teamKey]
                createUserCode = team['createUserCode']
                team['payStatus'] = payStatus
                team['transaction_id'] = transaction_id
                team['openid'] = openid
                team['signupStatusCode'] = 1
                self.session_updateUserData(createUserCode)
                self.putDbBuffer('sysData/updateTeamWxPayStatus', {
                    "teamKey": teamKey,
                    "payStatus": team['payStatus'],
                    "transaction_id": team['transaction_id'],
                    "openid": team['openid'],
                })
                res = {
                    "teamKey": teamKey,
                    "payStatus": payStatus,
                    "transaction_id": transaction_id,
                    "openid": openid
                }
                status = 1
            else:
                status = 3000
        except Exception as er:
            print(er)
        return res, status
    
    def mem_setWxPayStatus(self,   memKey, payStatus , transaction_id, openid,payTime,totalFee):
        res = {}
        status = 0
        try:
            self.putDbBuffer('sysData/updateTeamMemWxPayStatus', {
                "memKey": memKey,
                "payStatus": payStatus,
                "transaction_id": transaction_id,
                "openid": openid,
                "payTime":payTime,
                "totalFee":totalFee
            })
            res = {
                "memKey": memKey,
                "payStatus": payStatus,
                "transaction_id": transaction_id,
                "openid": openid,
                "payTime":payTime,
                "totalFee":totalFee
            }
            status = 1
        except Exception as er:
            logger.error('mem_setWxPayStatus error: %s', er)
        return res, status


    #member
    def memmber_create(self, sessionId , tel , teamKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList):
        res ={}
        status = 0
        try:
            with self.dataLock:
                status = self.checkEnable_createMember(sessionId , tel , teamKey , memberName , functionCode , genderCode , idTypeCode , idCode)
                if status==1 :
                    memKey = str(uuid.uuid4()).replace('-','')
                    res ={
                        "memKey" : memKey,
                        "teamCode": teamKey,
                        "functionCode": functionCode,
                        "memName": memberName,
                        "genderCode": genderCode,
                        "idTypeCode": idTypeCode,
                        "idCode": idCode,
                        "tel": memTel,
                        "photoImg": photoImg,
                        "idImgList": idImgList
                    }
                    self.datas.teamMembers[memKey] = res
                    self.datas._add_member_index(teamKey, memKey)
                    if functionCode=='01' :
                        self.datas.athIds[idCode] = idCode
            if status == 1:
                self.putDbBuffer('sysData/createMem', res)
                self.session_updateUserData(tel)
        except Exception as er:
            logger.error('memmber_create error: %s', er)
        return res , status
    def memmber_edit(self, sessionId , tel , memKey , memberName , functionCode , genderCode , idTypeCode, idCode , memTel , photoImg , idImgList):
        res ={}
        status = 0
        try:
            editInfo = None
            with self.dataLock:
                status = self.checkEnable_editMember(sessionId , tel , memKey , memberName , functionCode , genderCode , idTypeCode, idCode )
                if status == 1 :
                    res = self.datas.teamMembers[memKey]
                    oldIdCode = res['idCode']
                    res['memName'] = memberName
                    res['functionCode'] = functionCode
                    res['genderCode'] = genderCode
                    res['idTypeCode'] = idTypeCode
                    res['idCode'] = idCode
                    res['memTel'] = memTel
                    res['photoImg'] = photoImg
                    res['idImgList'] = idImgList
                    if oldIdCode != idCode:
                        del self.datas.athIds[oldIdCode]
                        self.datas.athIds[idCode] = idCode
                    editInfo ={
                        "memKey": memKey ,
                        "memName": memberName ,
                        "functionCode": functionCode ,
                        "genderCode": genderCode ,
                        "idTypeCode": idTypeCode ,
                        "idCode": idCode ,
                        "memTel": memTel ,
                        "photoImg": photoImg ,
                        "idImgList": idImgList ,
                    }
            if status == 1 and editInfo is not None:
                self.putDbBuffer('sysData/editMem', editInfo)
                self.session_updateUserData(tel)
        except Exception as er:
            print(er)
        return res , status
    def memmber_updateExInfo(self, sessionId , tel , memberKey , height , weight , width , bib, birthday, masterName , masterRelation, masterTel):
        res ={}
        status = 0
        try:
            editInfo = None
            with self.dataLock:
                status = self.check_sessionTel(sessionId, tel)
                if status == 1:
                    if memberKey in  self.datas.teamMembers.keys():
                        res = self.datas.teamMembers[memberKey]
                        res['weight'] =  weight
                        res['height'] =  height
                        res['width'] =  width
                        res['bib'] =  bib
                        res['birthday'] =  birthday
                        res['masterName'] =  masterName
                        res['masterRelation'] =  masterRelation
                        res['masterTel'] =  masterTel

                        editInfo = {
                            "memKey": memberKey,
                            "weight":weight ,
                            "height":height ,
                            "width":width ,
                            "bib":bib ,
                            "birthday":birthday ,
                            "masterName":masterName ,
                            "masterRelation":masterRelation ,
                            "masterTel":masterTel
                        }
                    else:
                        status = 40000
                else:
                    status = 1000
            if status == 1 and editInfo is not None:
                self.putDbBuffer('sysData/editMemExInfo', editInfo)
                self.session_updateUserData(tel)
        except Exception as er:
            print(er)
        return res , status
    #member
    def memmber_remove(self, sessionId , tel , memKey ):
        status = 0
        res = {}
        try:
            with self.dataLock:
                status = self.check_sessionTel(sessionId, tel)
                if status == 1 :
                    if memKey in self.datas.teamMembers.keys():
                        member = self.datas.teamMembers[memKey]
                        if member['functionCode'] == '01':
                            idCode = member['idCode']
                            del self.datas.athIds[idCode]
                        del self.datas.teamMembers[memKey]
                        self.datas._remove_member_index(member.get('teamCode'), memKey)
                        res = {
                            "ac": "removeMember",
                            "memKey": memKey
                        }
                    else:
                        status = 4000
            if status == 1:
                self.putDbBuffer('sysData/removeMem', {'memKey': memKey})
                self.session_updateUserData(tel)
        except Exception as er:
            logger.error('memmber_remove error: %s', er)
        return res , status



    def acRouterInit(self, data  ):
        try:
            self.initSysData()
            data.result = {
                "ac":'initSysDatas'
            }
        except Exception as er:
            logger.error('acRouterInit error: %s', er)
    def acRouterExportGameData(self, data  ):
        try:
            self.exportGameData()
            data.result = {
                "ac":'exportGameData'
            }
        except Exception as er:
            logger.error('acRouterExportGameData error: %s', er)
    def acRouterSessionCreate(self, data  ):
        try:
            res , status = self.session_create()
            data.result = {
                "status":status ,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterSessionCreate error: %s', er)
    def acRouterSessionValid(self, data  ):
        try:
            sessionId = data.params['sessionId']
            tel = data.params['tel']
            res , status = self.session_valid(sessionId, tel)
            data.result = {
                "status":status ,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterSessionValid error: %s', er)
    def acRouterSessionCheckLogin(self, data  ):
        try:
            sessionId = data.params['sessionId']
            tel = data.params['tel']
            validCode = data.params['validCode']
            status = self.session_checkLogin(sessionId, tel , validCode)
            data.result = {
                "status":status
            }
        except Exception as er:
            logger.error('acRouterSessionCheckLogin error: %s', er)
    def acRouterTeamCreate(self, data  ):
        try:
            sessionId = data.params['sessionId']
            tel = data.params['tel']
            teamName = data.params['teamName']
            eventCode = data.params['eventCode']
            areaCode = data.params['areaCode']
            phaseCode = data.params['phaseCode']
            logoImg = data.params['logoImg']
            res , status = self.team_create(sessionId , tel , teamName , eventCode , areaCode , phaseCode , logoImg)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterTeamCreate error: %s', er)
    def acRouterTeamSetSignupStatus(self, data  ):
        try:
            sessionId = data.params['sessionId']
            tel = data.params['tel']
            teamKey = data.params['teamKey']
            teamStatus = data.params['teamStatus']
            res , status = self.team_setSignupStatus(sessionId , tel , teamKey , teamStatus)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterTeamSetSignupStatus error: %s', er)
    def acRouterTeamSetSignupStatusAdmin(self, data  ):
        try:
            teamExInfo = data.params['teamExInfo']
            teamKey = data.params['teamKey']
            teamStatus = data.params['teamStatus']
            res , status = self.team_setSignupStatus_admin( teamKey , teamStatus , teamExInfo)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterTeamSetSignupStatusAdmin error: %s', er)
    def acRouterTeamSetWxPayStatus(self, data  ):
        try:
            logger.info('wxPay team: %s', data )
            teamKey = data.params['out_trade_no']
            payStatus = data.params['payStatus']
            transaction_id = data.params['transaction_id']
            openid = data.params['openid']
            res , status = self.team_setWxPayStatus( teamKey ,payStatus , transaction_id , openid)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterTeamSetWxPayStatus error: %s', er)
    def acRouterMemSetWxPayStatus(self, data  ):
        try:
            logger.info('wxPay mem: %s', data )
            memKey = data.params['out_trade_no']
            payStatus = data.params['payStatus']
            transaction_id = data.params['transaction_id']
            openid = data.params['openid']
            payTime = data.params['payTime']
            totalFee = data.params['totalFee']
            res , status = self.mem_setWxPayStatus( memKey,payStatus,transaction_id,openid,payTime,totalFee)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterMemSetWxPayStatus error: %s', er)

    def acRouterMemberCreate(self, data  ):
        try:
            sessionId = data.params['sessionId']
            tel = data.params['tel']
            teamKey = data.params['teamKey']
            #sessionId , tel , teamKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList
            memberName = data.params['memberName']
            functionCode = data.params['functionCode']
            genderCode = data.params['genderCode']
            idTypeCode = data.params['idTypeCode']
            idCode = data.params['idCode']
            memTel = data.params['memTel']
            photoImg = data.params['photoImg']
            idImgList = data.params['idImgList']
            res , status = self.memmber_create(sessionId , tel , teamKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterMemberCreate error: %s', er)
    def acRouterMemberEdit(self, data  ):
        try:
            sessionId = data.params['sessionId']
            tel = data.params['tel']
            memKey = data.params['memKey']
            #sessionId , tel , memberKey , memberName , functionCode , genderCode , idTypeCode, idCode , memTel , photoImg , idImgList
            memberName = data.params['memberName']
            functionCode = data.params['functionCode']
            genderCode = data.params['genderCode']
            idTypeCode = data.params['idTypeCode']
            idCode = data.params['idCode']
            memTel = data.params['memTel']
            photoImg = data.params['photoImg']
            idImgList = data.params['idImgList']
            res , status = self.memmber_edit(sessionId , tel , memKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterMemberEdit error: %s', er)
    def acRouterMemberUpdateExInfo(self, data  ):
        try:
            sessionId = data.params['sessionId']
            tel = data.params['tel']
            memKey = data.params['memKey']
            #sessionId , tel , memKey , height , weight , width , bib, birthday, masterName , masterRelation, masterTel
            height = data.params['height']
            weight = data.params['weight']
            width = data.params['width']
            bib = data.params['bib']
            birthday = data.params['birthday']
            masterName = data.params['masterName']
            masterRelation = data.params['masterRelation']
            masterTel = data.params['masterTel']
            res , status = self.memmber_updateExInfo(sessionId , tel , memKey , height , weight , width , bib, birthday, masterName , masterRelation, masterTel)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterMemberUpdateExInfo error: %s', er)
    def acRouterMemberRemove(self, data  ):
        try:
            sessionId = data.params['sessionId']
            tel = data.params['tel']
            memKey = data.params['memKey']
            res , status = self.memmber_remove(sessionId , tel , memKey)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterMemberRemove error: %s', er)
    def acRouterExecuteUserData(self, data  ):
        try:
            tel = data.params['tel']
            res , status = self.session_updateUserData(tel)
            data.result = {
                "status":status,
                "res": res
            }
        except Exception as er:
            logger.error('acRouterExecuteUserData error: %s', er)


    def startDB(self):
        # NOTE: 使用阻塞式 get 替代超时轮询，避免空闲时 CPU 空转
        import logging
        db_logger = logging.getLogger('pluginBkSignup.dbLoop')
        try:
            db_logger.info('start db loop ...')
            while self.loopStatus:
                try:
                    # 阻塞等待任务，不再用 timeout 空轮询
                    firstTask = self.dbBuffer.get(timeout=5)
                except queue.Empty:
                    continue

                dbTasks = [firstTask]
                # 批量取出队列中已有的任务
                while True:
                    try:
                        dbTasks.append(self.dbBuffer.get_nowait())
                    except queue.Empty:
                        break

                for task in dbTasks:
                    try:
                        db_logger.debug('db task: %s', task.get('k', ''))
                        key = task['k']
                        ps = task['ps']
                        self.getDB().queryByKey(self.dbCode , key , ps)
                    except Exception as eer:
                        db_logger.error('db task error: %s', eer)
                        # NOTE: 异常退避，防止数据库不可用时疯狂重试消耗 CPU
                        time.sleep(1)
        except Exception as er :
            import logging
            logging.getLogger('pluginBkSignup').error('db loop fatal: %s', er)
        finally:
            self.loopStatus = False
    def startDBAsync(self):
        try:
            with self.dbThreadLock:
                if not self.loopStatus:
                    self.loopStatus = True
                    thread = threading.Thread(target=self.startDB, daemon=True)
                    thread.start()
        except Exception as er:
            logger.error('startDBAsync error: %s', er)
    def regist2Router(self):
        try:
            self.acRouter.regist("bksignup/init", self.acRouterInit)
            self.acRouter.regist("bksignup/exportGameData", self.acRouterExportGameData)
            self.acRouter.regist("bksignup/sessionCreate", self.acRouterSessionCreate)
            self.acRouter.regist("bksignup/sessionValid", self.acRouterSessionValid)
            self.acRouter.regist("bksignup/sessionCheckLogin", self.acRouterSessionCheckLogin)
            self.acRouter.regist("bksignup/teamCreate", self.acRouterTeamCreate)
            self.acRouter.regist("bksignup/teamSetSignupStatus", self.acRouterTeamSetSignupStatus)
            self.acRouter.regist("bksignup/teamSetSignupStatusAdmin", self.acRouterTeamSetSignupStatusAdmin)
            self.acRouter.regist("bksignup/teamSetWxPayStatus", self.acRouterTeamSetWxPayStatus)
            self.acRouter.regist("bksignup/memberCreate", self.acRouterMemberCreate)
            self.acRouter.regist("bksignup/memberEdit", self.acRouterMemberEdit)
            self.acRouter.regist("bksignup/memberUpdateExInfo", self.acRouterMemberUpdateExInfo)
            self.acRouter.regist("bksignup/memberRemove", self.acRouterMemberRemove)
            self.acRouter.regist("bksignup/sessionExecuteUserData", self.acRouterExecuteUserData)
            self.acRouter.regist("bksignup/memSetWxPayStatus", self.acRouterMemSetWxPayStatus)
        except Exception as er:
            logger.error('regist2Router error: %s', er)
