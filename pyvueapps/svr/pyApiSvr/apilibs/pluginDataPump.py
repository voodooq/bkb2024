import json


class TPyDataPump:
    def __init__(self , acRouter):
        self.acRouter = acRouter
    def export2file(self, srcType , srcCode , srcKey , srcParams , ioCode , dataPath):
        res={
            "status":0
        }
        try:
            if ioCode in self.acRouter.plugins['io'].ios.keys():
                pluginIo = self.acRouter.plugins['io']
                src = None
                if srcType == 'mssql' or srcType == 'mysql':
                    src = self.acRouter.plugins[srcType]
                if src == None:
                    res['status'] = -2000
                else:
                    queryResult = src.queryByKey(srcCode , srcKey , srcParams )
                    if queryResult['status']>0:
                        num = len(queryResult["data"]["recordsetList"])
                        resList = []
                        if num==1:
                            resList = queryResult["data"]["recordsetList"][0]
                        else:
                            resList = queryResult["data"]["recordsetList"]
                        content = json.dumps(resList, ensure_ascii=False)
                        resList = None
                        writeRes= pluginIo.write(ioCode , dataPath , content)
                        res['status'] = writeRes['status']
                    else:
                        res['status'] = queryResult['status']
            else:
                res['status'] = -1000
        except Exception as er:
            print(er)
        return  res
    def export2oss(self, srcType , srcCode , srcKey , srcParams , channelCode , dataPath):
        res={
            "status":0
        }
        try:
            if channelCode in self.acRouter.plugins['oss'].settings.keys():
                pluginOss = self.acRouter.plugins['oss']
                src = None
                if srcType == 'mssql' or srcType == 'mysql':
                    src = self.acRouter.plugins[srcType]
                if src == None:
                    res['status'] = -2000
                else:
                    queryResult = src.queryByKey(srcCode , srcKey , srcParams )
                    if queryResult['status']>0:
                        num = len(queryResult["data"]["recordsetList"])
                        resList = []
                        if num==1:
                            resList = queryResult["data"]["recordsetList"][0]
                        else:
                            resList = queryResult["data"]["recordsetList"]
                        content = json.dumps(resList, ensure_ascii=False)
                        resList = None
                        writeRes= pluginOss.write(channelCode , dataPath , content)
                        res['status'] = writeRes['status']
                    else:
                        res['status'] = queryResult['status']
            else:
                res['status'] = -1000
        except Exception as er:
            print(er)
        return  res


    def acRouterExport2file(self, data):
        try:
            srcType = data.params['srcType']
            srcCode = data.params['srcCode']
            srcKey = data.params['srcKey']
            srcParams = data.params['srcParams']
            ioCode = data.params['ioCode']
            dataPath = data.params['dataPath']
            data.result = self.export2file(srcType , srcCode , srcKey , srcParams , ioCode , dataPath)
        except Exception as er:
            print(er)
    def acRouterExport2oss(self, data):
        try:
            srcType = data.params['srcType']
            srcCode = data.params['srcCode']
            srcKey = data.params['srcKey']
            srcParams = data.params['srcParams']
            chCode = ""
            if 'channelCode' in data.params.keys():
                chCode = data.params['channelCode']
            elif 'ioCode' in data.params.keys():
                chCode = data.params['ioCode']
            dataPath = data.params['dataPath']
            data.result = self.export2oss(srcType , srcCode , srcKey , srcParams , chCode , dataPath)
        except Exception as er:
            print(er)