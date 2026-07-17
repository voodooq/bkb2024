import time
import uuid
import logging
import os

# NOTE: 使用 logging 替代 print，生产环境可通过环境变量控制日志级别
log_level = os.getenv("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.WARNING),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('pyapisvr')

logger.info('------------------------------  py api server -----------------------------------')


from config import svrConfig
from apilibs.acRouter import acRouter
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import json

#config io
pluginIo = acRouter.plugins['io']
for item in svrConfig["io"]:
    code = item['code']
    pluginIo.ios[code] = item
#config oss
pluginOss = acRouter.plugins['oss']
for item in svrConfig["oss"]:
    code=item['code']
    pluginOss.settings[code] = item


# config db
pluginDB = acRouter.plugins['db']
for item in svrConfig['mssql']:
    pluginDB.setSettings(
        item['code'] ,
        'mssql',
        item['host'],
        item['port'],
        item['db'],
        item['uid'],
        item['pwd'],
        item['sqlPath']
    )
for item in svrConfig['mysql']:
    pluginDB.setSettings(
        item['code'] ,
        'mysql',
        item['host'],
        item['port'],
        item['db'],
        item['uid'],
        item['pwd'],
        item['sqlPath']
    )
# config ossBucket
pluginOssBucket = acRouter.plugins['ossBucket']
for item in svrConfig["ossBucket"]:
    pluginOssBucket.setSettings(
        item['code'],
        item['bucket'],
        item['ak'],
        item['sk'],
        item['endpoint'],
        item['shortEndpoint'],
        item['stsRoleArn']
    )

# NOTE: config ossLive — 从 svrConfig 注入直播配置，不再硬编码
pluginOssLive = acRouter.plugins['ossLive']
if 'ossLive' in svrConfig:
    pluginOssLive.setConfig(svrConfig['ossLive'])

# app BkSignup
appBkSignup = acRouter.apps['bkSignup']
try:
    item = svrConfig['apps']['bksignup']
    appBkSignup.setSettings(item['dbCode'] , item['ossBucketCode']  , item['bucketName'])
    appBkSignup.exportGameData()
except Exception as er:
    logger.error('BkSignup init error: %s', er)

# fastapi app
class TRequestData(BaseModel):
    action:str
    params:dict= dict()
    result: dict = None
    def getJson(self):
        return  json.loads(json.dumps({
            "action": self.action ,
            "params": self.params,
            "result": self.result
        }))
    def saveReques(self):
        try:
            pass
            '''
            content = json.dumps({
                "action": self.action ,
                "params": self.params,
                "result": self.result
            } , ensure_ascii=False)
            fn = "/reqlog/"+str(int(1000*1000*time.time()))+".txt"
            with open(fn , 'w') as f :
                f.write(fn)
            '''
        except Exception as er:
            print('save request error.',er)
app = FastAPI()
@app.get("/")
def root(  ):
    return {
        "action":"yyapi"
    }
@app.post("/yyapi")
def yyapi( reqData : TRequestData):
    reqData.result={
        "status":1,
        "data":{}
    }
    try:
        action = reqData.action
        logger.info('call %s', action)
        flag = action in acRouter.handlers.keys()
        if flag :
            try:
                reqData.saveReques()
                acRouter.runAcHandler(reqData)
            except Exception as erHandler:
                logger.error('handler error: %s', erHandler)
        else:
            reqData.result['status']= -100
            reqData.result['data']=None
            reqData.result['errMsg']="action error."
    except Exception as eer:
        logger.error('request error: %s', eer)
    return  reqData.result

webHost= svrConfig['webSvr'][0]['host']
webPort= svrConfig['webSvr'][0]['port']
def startWebSvr():
        reloadFlag = str(os.getenv("UVICORN_RELOAD", "false")).lower() in ("1", "true", "yes", "on")
        uvicorn.run("pyapisvr:app", host= webHost, port=webPort, reload=reloadFlag)

if __name__ == '__main__':
        startWebSvr()