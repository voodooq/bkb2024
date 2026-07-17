from .pluginOssBucket import TPyOssBucket
from .plugOssLive import TOssLive
from .pluginIo import TPyIo
from .pluginDataPump import TPyDataPump
from .pluginOss import TPyOss
from .pluginDB import TPyDB

# app plugin

from .pluginBkSignup import TBkSignup
class TAcRouter:
    def __init__(self):
        self.handlers={};
        pluginOssBucket = TPyOssBucket(self)
        pluginDB = TPyDB(self)
        plugOssLive = TOssLive(self)
        plugIo = TPyIo(self)
        plugDataPump = TPyDataPump(self)
        pluginOss = TPyOss(self)

        appBkSignup =TBkSignup(self)

        self.plugins ={
            "ossBucket": pluginOssBucket,
            "db": pluginDB,
            "ossLive":plugOssLive,
            "io":plugIo,
            "dataPump": plugDataPump,
            "oss": pluginOss
        }
        self.apps ={
            "bkSignup": appBkSignup
        }
        self.regist("msquery", pluginDB.acRouterLegacyQuery)
        self.regist("myquery", pluginDB.acRouterLegacyQuery)
        self.regist("oss/bucket/read" , pluginOssBucket.acRouterRead)
        self.regist("oss/bucket/write" , pluginOssBucket.acRouterWrite)
        self.regist("oss/bucket/stsInfo" , pluginOssBucket.acRouterStsInfo)
        self.regist("db/query", pluginDB.acRouterQueryByKey)
        self.regist("db/create", pluginDB.acRouterCreateRow)
        self.regist("db/update", pluginDB.acRouterUpdteRow)
        self.regist("db/del", pluginDB.acRouterDeleteRow)
        self.regist("db/view", pluginDB.acRouterViewRows)
        self.regist("splitOssLive", plugOssLive.acRouterSplit)
        self.regist("ossChannel", plugOssLive.acRouterGetChannel)
        self.regist("ioRead", plugIo.acRouterRead)
        self.regist("ioWrite", plugIo.acRouterWrite)
        self.regist("ossWrite", pluginOss.acRouterWrite)
        self.regist("ossRead", pluginOss.acRouterRead)
        self.regist("dataPumpExport2File", plugDataPump.acRouterExport2file)
        self.regist("dataPumpExport2Oss", plugDataPump.acRouterExport2oss)

        appBkSignup.regist2Router()


    def regist(self , acKey , handler):
        try:
            self.handlers[acKey] = handler
        except Exception as er:
            print(er)
    def runAcHandler(self , acData):
        try:
            acData.result = {}
            action = acData.action
            if( action in self.handlers.keys()):
                handler = self.handlers[action]
                handler(acData)
            else:
                acData['result'] = {
                    "errCode": -100,
                    "errMsg":"action error."
                }
        except Exception as er:
            print(er)

acRouter = TAcRouter()