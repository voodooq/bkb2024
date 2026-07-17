import oss2
import json
import os
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdksts.request.v20150401 import AssumeRoleRequest




'''
channel配置参数
    code:"",
    ak:"",
    sk:"",
    bucket:"",
    endpoint:"" 
'''

'''
errCode:
1000: ossCode error
1001: connection params error
1002: bucketName error
1003: dataKey error

'''

class TPyOssBucket:
    def __init__(self , acRouter):
        self.acRouter = acRouter
        self.settings={}
        self.buckets ={}
        self.clients ={}
    def setSettings(self , ossCode , bucket, ak , sk , endpoint , shortEndpoint, sts_role_arn):
        status = 0
        try:
            settingItem = {}
            if ossCode in self.settings.keys():
                settingItem = self.settings[ossCode]
            else:
                self.settings[ossCode] = settingItem
            settingItem['bucket'] = bucket
            settingItem['ak'] = ak
            settingItem['sk'] = sk
            settingItem['endpoint'] = endpoint
            settingItem['shortEndpoint'] = shortEndpoint
            settingItem['stsRoleArn'] = sts_role_arn
        except Exception as er:
            print(er)
        return  status
    def bucketRead(self , ossCode , bucketName , dataPath):
        res = ""
        status = 0
        try:
            bucket , status = self.getBucket(ossCode , bucketName)
            if status == 1 :
                fn = dataPath
                _, extName = os.path.splitext(fn)
                if extName=="":
                    fn = fn +".txt"
                try:
                    res = bucket.get_object(fn)
                    status = 1
                except Exception as ee:
                    status = 1001
                    print(ee)
        except Exception as er:
            print(er)
        return  res , status
    def bucketWrite(self , ossCode , bucketName , dataPath , content):
        res=""
        status = 0
        try:
            bucket , status = self.getBucket(ossCode , bucketName)
            if status == 1 :
                fn = dataPath
                _, extName = os.path.splitext(fn)
                if extName=="":
                    fn = fn +".txt"
                try:
                    result = bucket.put_object(fn, content)
                    status = result.status
                    endpoint = self.settings[ossCode]['endpoint']
                    res = 'http://'+bucketName+'.'+ endpoint+"/"+fn
                    status = 1
                except Exception as ee:
                    status = 1001
                    print(ee)
        except Exception as er:
            print(er)
        return  res , status
    def getBucket(self , ossCode , bucketName):
        bucket = None
        status = 0
        try:
            if ossCode in self.settings.keys():
                bucketKey = ossCode +'_'+ bucketName
                if bucketKey in  self.buckets.keys():
                    bucket = self.buckets[bucketKey]
                    status = 1
                else:
                    setting = self.settings[ossCode]
                    access_key_id = setting['ak']
                    access_key_secret = setting['sk']
                    endpoint = setting['endpoint']
                    try:
                        bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucketName)
                        status = 1
                    except Exception as ee:
                        status = 1001
                        print(ee)
            else:
                status = 1000
        except Exception as er:
            print(er)
        return bucket, status
    def getStsClient(self , ossCode  ):
        clt = None
        status = 0
        try:
            if ossCode in self.settings.keys():
                setting = self.settings[ossCode]
                access_key_id = setting['ak']
                access_key_secret = setting['sk']
                endpoint = setting['shortEndpoint']
                try:
                    clt = client.AcsClient(access_key_id, access_key_secret, endpoint)
                    status = 1
                except Exception as ee:
                    status = 1001
                    print(ee)
            else:
                status = 1000
        except Exception as er:
            print(er)
        return  clt , status
    def getStsInfo(self , ossCode ,  roleSessionName,  duration=3000):
        res = {}
        status = 0
        try:
            clt , status = self.getStsClient(ossCode)
            if status == 1:
                setting = self.settings[ossCode]
                request = AssumeRoleRequest.AssumeRoleRequest()
                sts_role_arn = setting['stsRoleArn']
                request.set_RoleArn(sts_role_arn)
                # 设置会话名称，审计服务使用此名称区分调用者
                request.set_RoleSessionName(roleSessionName)
                request.set_DurationSeconds(duration)
                # 发起请求，并得到response
                response = clt.do_action_with_exception(request)
                res = json.loads(oss2.to_unicode(response))
                status = 1
        except Exception as er:
            print(er)
            status = 1001
        return  res , status


    def acRouterWrite(self, data):
        try:
            ossCode = data.params['ossCode']
            bucketName = data.params['bucketName']
            dataPath = data.params['dataPath']
            content = data.params['content']
            res , status  = self.bucketWrite(ossCode , bucketName , dataPath , content)
            data.result ={
                "status": status,
                "dataUrl": res
            }
        except Exception as er:
            print(er)
    def acRouterRead(self, data):
        try:
            ossCode = data.params['ossCode']
            bucketName = data.params['bucketName']
            dataPath = data.params['dataPath']
            res , status  = self.bucketRead(ossCode , bucketName , dataPath  )
            data.result ={
                "status": status,
                "content": res
            }
        except Exception as er:
            print(er)
    def acRouterStsInfo(self, data):
        try:
            ossCode = data.params['ossCode']
            roleSessionName = data.params['roleSessionName']
            duration = data.params['duration']
            res , status  = self.getStsInfo(ossCode, roleSessionName , duration  )
            data.result ={
                "status": status,
                "stsInfo": res
            }
        except Exception as er:
            print(er)