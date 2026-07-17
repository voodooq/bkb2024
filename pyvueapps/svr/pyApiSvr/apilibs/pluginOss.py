import oss2
import os


'''
channel配置参数
    code:"",
    ak:"",
    sk:"",
    bucket:"",
    endpoint:"" 
'''

class TPyOss:
    def __init__(self , acRouter):
        self.acRouter = acRouter
        self.settings={}
        self.channels ={}
    def getChannel(self, channelCode):
        ch = None
        try:
            if channelCode in self.channels.keys():
                ch = self.channels[channelCode]
            else:
                if channelCode in self.settings.keys():
                    access_key_id = self.settings[channelCode]['ak']
                    access_key_secret = self.settings[channelCode]['sk']
                    endpoint = self.settings[channelCode]['endpoint']
                    bucket_name = self.settings[channelCode]['bucket']
                    ch = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
                    self.channels[channelCode] = ch
        except Exception as er:
            print(er)
        return  ch
    def read(self , channelCode , dataPath):
        res = {
            "status": 0 ,
            "content":""
        }
        try:
            ch = self.getChannel(channelCode)
            if ch == None:
                res['status'] = -1000
            else:
                fn = dataPath
                _, extName = os.path.splitext(fn)
                if extName=="":
                    fn = fn +".txt"
                result = ch.get_object(fn)
                try:
                    res['content'] = result.read()
                    res['status'] = 1
                except Exception as ee:
                    res['status'] = -3000
                    print(ee)
        except Exception as er:
            print(er)
        return  res
    def write(self , channelCode , dataPath , content):
        res = {
            "status": 0
        }
        try:
            ch = self.getChannel(channelCode)
            if ch!=None:
                fn = dataPath
                _, extName = os.path.splitext(fn)
                if extName=="":
                    fn = fn +".txt"
                result = ch.put_object(fn, content)
                res['status'] = result.status
                endpoint = self.settings[channelCode]['endpoint']
                bucket_name = self.settings[channelCode]['bucket']
                res['url'] = 'http://'+bucket_name+'.'+ endpoint+"/"+fn
            else:
                res['status'] = -1000
        except Exception as er:
            print(er)
        return  res
    def acRouterWrite(self, data):
        try:
            chCode = data.params['channelCode']
            dataPath = data.params['dataPath']
            content = data.params['content']
            data.result = self.write(chCode , dataPath , content)
        except Exception as er:
            print(er)
    def acRouterRead(self, data):
        try:
            chCode = data.params['channelCode']
            dataPath = data.params['dataPath']
            data.result = self.read(chCode , dataPath)
        except Exception as er:
            print(er)