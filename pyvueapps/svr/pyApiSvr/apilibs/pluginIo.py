
import os
class TPyIo:
    def __init__(self , acRouter):
        self.acRouter = acRouter
        self.ios ={}
    def read(self , ioCode , dataPath):
        res = {
            "status": 0 ,
            "content":""
        }
        try:
            if ioCode in  self.ios.keys():
                ioInfo = self.ios[ioCode]
                rootPath = ioInfo['root']
                fn = os.path.join(rootPath , dataPath)
                _ , extName = os.path.splitext(fn)
                if extName == '' :
                    fn = fn +".txt"
                if os.path.exists(fn):
                    with open(fn , "r+", encoding="utf-8") as file:
                        res['content'] = file.read()
                    res['status'] = 1
                else:
                    res['status']=-1001
            else:
                res['status'] = -1000
        except Exception as er:
            print(er)
        return  res
    def write(self , ioCode , dataPath , content):
        res = {
            "status": 0 ,
            "content":""
        }
        try:
            if ioCode in  self.ios.keys():
                ioInfo = self.ios[ioCode]
                rootPath = ioInfo['root']
                fn = os.path.join(rootPath , dataPath)
                _ , extName = os.path.splitext(fn)
                if extName == '' :
                    fn = fn +".txt"
                    _dir, _ = os.path.split(fn)
                    if not os.path.exists(_dir):
                        os.makedirs(_dir, 0x777 ,True)
                    if os.path.exists(_dir):
                        with open(fn, 'w', encoding='utf-8') as file:
                            file.write(content)
                        res['status'] = 1
                    else:
                        res['status'] = - 1002
                else:
                    res['status']=-1001
            else:
                res['status'] = -1000
        except Exception as er:
            print(er)
        return  res
    def acRouterWrite(self, data):
        try:
            ioCode = data.params['ioCode']
            dataPath = data.params['dataPath']
            content = data.params['content']
            data.result = self.write(ioCode , dataPath , content)
        except Exception as er:
            print(er)
    def acRouterRead(self, data):
        try:
            ioCode = data.params['ioCode']
            dataPath = data.params['dataPath']
            data.result = self.read(ioCode , dataPath)
        except Exception as er:
            print(er)