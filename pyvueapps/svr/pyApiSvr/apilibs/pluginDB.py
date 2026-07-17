"""
# pip install pymysql
# pip install DBUtils==1.3  --- 特别要注意
"""
import json
import re
import time
import logging
import pymysql
import pymssql
from pymysql.constants import CLIENT
from DBUtils.PooledDB import PooledDB
import os

logger = logging.getLogger('pluginDB')

# NOTE: SQL 标识符白名单正则，仅允许字母、数字、下划线、点号
_SAFE_IDENTIFIER_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_.]*$')

'''
Error Code:
1001 : db code is error.
1002 : db type is error.
1003 : pool params error.
1004 : query faild.
'''
class TPyDB():
    def __init__(self , acRouter):
        self.acRouter = acRouter;
        self.settings = {}
        self.pools ={}

    def setSettings (self, code , dbType , host , port , db , uid , pwd , sqlPath):
        try:
            item = {}
            if code in  self.settings.keys():
                item = self.settings[code]
            else:
                self.settings[code] = item

            item['code'] = code
            item['dbType'] = dbType
            item['host'] = host
            item['port'] = port
            item['db'] = db
            item['uid'] = uid
            item['pwd'] = pwd
            item['sqlPath'] = sqlPath
        except Exception as er:
            logger.error('pluginDB error: %s', er)
    def getPool (self, code):
        pool = None
        status = 0
        try:
            if code in self.pools.keys():
                pool = self.pools[code]
                status = 1
            elif code in self.settings.keys():
                settingItem = self.settings[code]
                if settingItem['dbType'] =='mysql':
                    pool , status = self.getMysqlPool(settingItem)
                elif settingItem['dbType'] =='mssql':
                    pool , status  = self.getMssqlPool(settingItem)
                else:
                    status = 1002
            else:
                status = 1001
                logger.warning('pool Code is error: %s', code)
        except Exception as er:
            logger.error('pluginDB error: %s', er)
        return  pool , status

    @staticmethod
    def _sanitize_identifier(name: str) -> str:
        """
        校验 SQL 标识符（表名、字段名、视图名）是否安全。
        仅允许字母、数字、下划线、点号，防止 SQL 注入。
        """
        if not _SAFE_IDENTIFIER_RE.match(name):
            raise ValueError(f'Unsafe SQL identifier rejected: {name!r}')
        return name

    def getMysqlPool(self, settingItem):
        pool = None
        status = 0
        try:
            maxconnections = int(os.getenv("DB_POOL_MAX_CONNECTIONS", "20"))
            mincached = int(os.getenv("DB_POOL_MIN_CACHED", "0"))
            maxcached = int(os.getenv("DB_POOL_MAX_CACHED", "5"))
            pool = PooledDB(
                creator=pymysql,
                maxconnections=maxconnections,
                mincached=mincached,
                maxcached=maxcached,
                maxshared=0,
                maxusage=1000,
                blocking=True,
                ping=4,
                host=settingItem["host"],
                port=settingItem["port"],
                database=settingItem["db"],
                user=settingItem["uid"],
                password=settingItem["pwd"],
                autocommit=True,
                client_flag=CLIENT.MULTI_STATEMENTS,
                # NOTE: 连接超时和读取超时，防止网络异常时长时间阻塞
                connect_timeout=10,
                read_timeout=30,
            )
            self.pools[settingItem['code']] = pool
            status = 1
        except Exception as er:
            status = 1003
            logger.error('MySQL pool create failed: %s', er)
        return  pool , status
    def getMssqlPool(self, settingItem):
        pool = None
        status = 0
        try:
            maxconnections = int(os.getenv("DB_POOL_MAX_CONNECTIONS", "20"))
            mincached = int(os.getenv("DB_POOL_MIN_CACHED", "0"))
            maxcached = int(os.getenv("DB_POOL_MAX_CACHED", "5"))
            pool = PooledDB(
                creator=pymssql,
                maxconnections=maxconnections,
                mincached=mincached,
                maxcached=maxcached,
                maxshared=0,
                maxusage=1000,
                ping=4,
                blocking=True,
                host=settingItem["host"],
                port=settingItem["port"],
                database=settingItem["db"],
                user=settingItem["uid"],
                password=settingItem["pwd"],
                autocommit=True,
                # NOTE: 登录超时，防止不可达的数据库地址阻塞进程
                login_timeout=10,
            )
            code = settingItem['code']
            self.pools[code] = pool
            status = 1
        except Exception as er:
            status = 1003
            logger.error('MSSQL pool create failed: %s', er)
        return  pool , status
    def getConnection (self, code):
        conn = None
        status = 0
        try:
            pool , poolStatus= self.getPool(code)
            if poolStatus==1 :
                conn = pool.connection()
                status = 1
            else:
                status = poolStatus
        except Exception as er:
            logger.error('getConnection error [%s]: %s', code, er)
        return  conn , status
    def query (self, code  , sql , params):
        queryRes = {
            "queryStatus" :0 ,
            "errMsg":"",
            "executeResult" :{},
            "datasetList":[],
            "recordset":[]
        }
        conn = None
        cursor = None
        try:
            conn , connstatus = self.getConnection(code)
            if connstatus == 1 :
                settingItem = self.settings[code]
                dbType = settingItem['dbType']
                if dbType == 'mysql':
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                else:
                    cursor = conn.cursor(as_dict=True)
                try:
                    logger.debug('start execute')
                    if params is not None:
                        cursor.execute(sql, params)
                    else:
                        cursor.execute(sql)
                    logger.debug('execute done')

                    if cursor.description is not None:
                        rsList = []
                        rs = cursor.fetchall()
                        rsList.append(list(rs))
                        while cursor.nextset():
                            rs = cursor.fetchall()
                            rsList.append(list(rs))
                        queryRes['datasetList'] = rsList
                        if len(queryRes['datasetList']) > 0:
                            queryRes['recordset'] = queryRes['datasetList'][0]
                    else:
                        queryRes['executeResult'] = {
                            "rowNum": cursor.rownumber,
                            "rowCount": cursor.rowcount,
                            "newId": cursor.lastrowid
                        }
                    queryRes['queryStatus'] = 1
                except Exception as eer:
                    logger.error('query failed: %s', eer)
                    logger.debug('query error sql: %s params: %s', sql, params)
                    queryRes['queryStatus'] = 1004
                    queryRes['errMsg'] = str(eer)
            else:
                queryRes['queryStatus'] = connstatus
        except Exception as er:
            logger.error('query outer error: %s', er)
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception as cursorErr:
                    logger.warning('cursor close error: %s', cursorErr)
            if conn is not None:
                try:
                    conn.close()
                except Exception as connErr:
                    logger.warning('conn close error: %s', connErr)
        return  queryRes
    def queryByKey (self, code  , key , params):
        queryRes = {
            "queryStatus" :0 ,
            "errMsg":"",
            "executeResult" :{},
            "datasetList":[],
            "recordset":[]
        }
        try:
            if code in self.settings.keys():
                fn = os.path.join(self.settings[code]["sqlPath"], key)
                _, ext = os.path.splitext(fn)
                if ext =='' :
                    fn = fn +'.txt'
                if os.path.exists(fn):
                    sql = ""
                    with open(fn, "r", encoding='utf-8') as f:
                        sql = f.read()
                    queryRes = self.query(code , sql ,  params)
                else:
                    logger.warning('file not exists: %s', fn)
                    queryRes['queryStatus'] = 1005
                    queryRes['errMsg'] = "key("+key+") is not exists."
            else:
                queryRes['queryStatus'] = 1001
        except Exception as er:
            logger.error('queryByKey error: %s', er)
        return  queryRes
    def createRow (self, code  , table , fieldValues):
        queryRes = {
            "queryStatus" :0 ,
            "errMsg":"",
            "executeResult" :{},
            "datasetList":[],
            "recordset":[]
        }
        try:
            if code in self.settings.keys():
                # NOTE: 校验表名和字段名，防止 SQL 注入
                self._sanitize_identifier(table)
                for x in fieldValues.keys():
                    self._sanitize_identifier(x)
                fields = ','.join([x for x  in fieldValues.keys()])
                values = ",".join(["%("+x+")s" for x in fieldValues.keys()])
                sql = "insert into " + table + "(" + fields +") values (" + values+")"
                queryRes = self.query(code , sql , fieldValues)
            else:
                queryRes['queryStatus'] = 1001
        except ValueError as ve:
            logger.error('SQL injection blocked in createRow: %s', ve)
            queryRes['queryStatus'] = 1006
            queryRes['errMsg'] = 'Invalid identifier'
        except Exception as er:
            logger.error('createRow error: %s', er)
        return  queryRes
    def updateRow (self, code  , table , fieldValues , keyValues):
        queryRes = {
            "queryStatus" :0 ,
            "errMsg":"",
            "executeResult" :{},
            "datasetList":[],
            "recordset":[]
        }
        try:
            if code in self.settings.keys():
                # NOTE: 校验表名和字段名，防止 SQL 注入
                self._sanitize_identifier(table)
                for x in fieldValues.keys():
                    self._sanitize_identifier(x)
                for x in keyValues.keys():
                    self._sanitize_identifier(x)
                fields = ','.join([x+'=%('+x+')s' for x in fieldValues.keys()])
                keys = " and ".join([x+'=%('+x+')s' for x in keyValues.keys()])
                sql = "update "+ table + ' set '+ fields +' where '+ keys
                ps ={}
                for k in fieldValues.keys():
                    ps[k] = fieldValues[k]
                for k in keyValues.keys():
                    ps[k] = keyValues[k]
                queryRes = self.query(code , sql , ps)
            else:
                queryRes['queryStatus'] = 1001
        except ValueError as ve:
            logger.error('SQL injection blocked in updateRow: %s', ve)
            queryRes['queryStatus'] = 1006
            queryRes['errMsg'] = 'Invalid identifier'
        except Exception as er:
            logger.error('updateRow error: %s', er)
        return  queryRes
    def deleteRow (self, code  , table  , keyValues):
        queryRes = {
            "queryStatus" :0 ,
            "errMsg":"",
            "executeResult" :{},
            "datasetList":[],
            "recordset":[]
        }
        try:
            if code in self.settings.keys():
                # NOTE: 校验表名和字段名，防止 SQL 注入
                self._sanitize_identifier(table)
                for x in keyValues.keys():
                    self._sanitize_identifier(x)
                keys = " and ".join([x+'=%('+x+')s' for x in keyValues.keys()])
                sql = "delete from  "+ table + ' where '+ keys
                queryRes = self.query(code , sql , keyValues)
            else:
                queryRes['queryStatus'] = 1001
        except ValueError as ve:
            logger.error('SQL injection blocked in deleteRow: %s', ve)
            queryRes['queryStatus'] = 1006
            queryRes['errMsg'] = 'Invalid identifier'
        except Exception as er:
            logger.error('deleteRow error: %s', er)
        return  queryRes
    def viewRows (self, code  , view  , keyValues):
        queryRes = {
            "queryStatus" :0 ,
            "errMsg":"",
            "executeResult" :{},
            "datasetList":[],
            "recordset":[]
        }
        try:
            if code in self.settings.keys():
                # NOTE: 校验视图名和字段名，防止 SQL 注入
                self._sanitize_identifier(view)
                for x in keyValues.keys():
                    self._sanitize_identifier(x)
                keys = " and ".join([x+'=%('+x+')s' for x in keyValues.keys()])
                sql = "select * from  "+ view + ' where '+ keys
                queryRes = self.query(code , sql , keyValues)
            else:
                queryRes['queryStatus'] = 1001
        except ValueError as ve:
            logger.error('SQL injection blocked in viewRows: %s', ve)
            queryRes['queryStatus'] = 1006
            queryRes['errMsg'] = 'Invalid identifier'
        except Exception as er:
            logger.error('viewRows error: %s', er)
        return  queryRes
    def acRouterQueryByKey(self, data):
        try:
            code = data.params['dbCode']
            key = data.params['dbKey']
            params = data.params['dbPs']
            data.result = self.queryByKey(code , key , params)
        except Exception as er:
            logger.error('acRouterQueryByKey error: %s', er)
    def acRouterCreateRow(self, data  ):
        try:
            code = data.params['dbCode']
            table = data.params['table']
            fieldValues = data.params['data']
            data.result = self.createRow(code , table , fieldValues)
        except Exception as er:
            logger.error('acRouterCreateRow error: %s', er)
    def acRouterUpdteRow(self, data  ):
        try:
            code = data.params['dbCode']
            table = data.params['table']
            fieldValues = data.params['data']
            keyValues = data.params['keys']
            data.result = self.updateRow(code , table , fieldValues , keyValues)
        except Exception as er:
            logger.error('acRouterUpdateRow error: %s', er)
    def acRouterDeleteRow(self, data  ):
        try:
            code = data.params['dbCode']
            table = data.params['table']
            keyValues = data.params['keys']
            data.result = self.deleteRow(code , table  , keyValues)
        except Exception as er:
            logger.error('acRouterDeleteRow error: %s', er)
    def acRouterViewRows(self, data  ):
        try:
            code = data.params['dbCode']
            view = data.params['view']
            keyValues = data.params['keys']
            data.result = self.viewRows(code , view  , keyValues)
        except Exception as er:
            logger.error('acRouterViewRows error: %s', er)

    # NOTE: 兼容由于移除 pluginMssql.py 和 pluginMysql.py 带来的历史路由结构差异
    def acRouterLegacyQuery(self, data):
        try:
            code = data.params['dbCode']
            key = data.params['dbKey']
            params = data.params['ps']
            raw_res = self.queryByKey(code, key, params)
            # 适配原 pluginMssql / pluginMysql 返回格式
            data.result = {
                "data": {
                    "recordset": raw_res.get("recordset", []),
                    "recordsetList": raw_res.get("datasetList", []),
                    "execResult": raw_res.get("executeResult", {})
                },
                "status": raw_res.get("queryStatus", 0),
                "errMsg": raw_res.get("errMsg", "")
            }
        except Exception as er:
            logger.error('acRouterLegacyQuery error: %s', er)