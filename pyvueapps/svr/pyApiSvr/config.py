"""
服务配置文件
所有敏感凭证通过环境变量注入，避免硬编码在代码中泄露。
Docker 部署时通过 docker-compose environment 或 .env 文件传入。
"""
import os


def _env(key: str, default: str = "") -> str:
    """
    从环境变量读取配置，未设置时使用默认值。
    生产环境中敏感信息必须通过环境变量注入。
    """
    return os.getenv(key, default)


svrConfig = {
    "webSvr":[
        {
            "code":"httpSvr",
            "host":"0.0.0.0",
            "port":8010,
            "sslKey":"",
            "sslPem":""
        }
    ],
    "mysql":[
        {
            "code": "sport",
            "host": _env("MYSQL_SPORT_HOST", "meeting.xmgkfw.com"),
            "port": int(_env("MYSQL_SPORT_PORT", "42041")),
            "uid": _env("MYSQL_SPORT_UID", "root"),
            "pwd": _env("MYSQL_SPORT_PWD", ""),
            "db": _env("MYSQL_SPORT_DB", "hh_reg"),
            "sqlPath": "./sysdatas/mysql/sqls"
        },
        {
            "code": "arbvideo",
            "host": _env("MYSQL_ARBVIDEO_HOST", "meeting.xmgkfw.com"),
            "port": int(_env("MYSQL_ARBVIDEO_PORT", "42041")),
            "uid": _env("MYSQL_ARBVIDEO_UID", "root"),
            "pwd": _env("MYSQL_ARBVIDEO_PWD", ""),
            "db": _env("MYSQL_ARBVIDEO_DB", "gameArbVideo2024"),
            "sqlPath": "./sysdatas/mysql/sqls/arbvideo"
        },
    ],
    "mssql":[
        {
            "code": "sv2",
            "host": _env("MSSQL_SV2_HOST", "meeting.xmgkfw.com"),
            "port": int(_env("MSSQL_SV2_PORT", "42049")),
            "uid": _env("MSSQL_SV2_UID", "sa"),
            "pwd": _env("MSSQL_SV2_PWD", ""),
            "db": _env("MSSQL_SV2_DB", "signup2024"),
            "sqlPath": "./sysdatas/mssql/sqls"
        },
        {
            "code": "eqvideo",
            "host": _env("MSSQL_EQVIDEO_HOST", "meeting.xmgkfw.com"),
            "port": int(_env("MSSQL_EQVIDEO_PORT", "42049")),
            "uid": _env("MSSQL_EQVIDEO_UID", "sa"),
            "pwd": _env("MSSQL_EQVIDEO_PWD", ""),
            "db": _env("MSSQL_EQVIDEO_DB", "eqvideo2024"),
            "sqlPath": "./sysdatas/mssql/sqls/eqvideo"
        },
        {
            "code": "femo",
            "host": _env("MSSQL_FEMO_HOST", "47.92.172.14"),
            "port": int(_env("MSSQL_FEMO_PORT", "10084")),
            "uid": _env("MSSQL_FEMO_UID", "sa"),
            "pwd": _env("MSSQL_FEMO_PWD", ""),
            "db": _env("MSSQL_FEMO_DB", "C_Fencing"),
            "sqlPath": "./sysdatas/mssql/sqls/femo"
        },
        {
            "code": "py2024",
            "host": _env("MSSQL_PY2024_HOST", "47.92.172.14"),
            "port": int(_env("MSSQL_PY2024_PORT", "10084")),
            "uid": _env("MSSQL_PY2024_UID", "sa"),
            "pwd": _env("MSSQL_PY2024_PWD", ""),
            "db": _env("MSSQL_PY2024_DB", "cb2024"),
            "sqlPath": "./sysdatas/mssql/sqls/py2024"
        },
        # NOTE: femolocal 指向 127.0.0.1:1433，Docker 容器内不可达，
        # 会导致连接池创建时反复超时重试，空转消耗 CPU。已禁用。
        # {
        #     "code": "femolocal",
        #     "host": "127.0.0.1",
        #     "port": 1433,
        #     "uid": "sa",
        #     "pwd": "123",
        #     "db": "C_Fencing",
        #     "sqlPath": "./sysdatas/mssql/sqls/femo"
        # },
        {
            "code": "bksignup",
            "host": _env("MSSQL_BKSIGNUP_HOST", "47.92.172.14"),
            "port": int(_env("MSSQL_BKSIGNUP_PORT", "10084")),
            "uid": _env("MSSQL_BKSIGNUP_UID", "sa"),
            "pwd": _env("MSSQL_BKSIGNUP_PWD", ""),
            "db": _env("MSSQL_BKSIGNUP_DB", "bkSignup2024"),
            "sqlPath": "./sysdatas/mssql/sqls/bksignup2024"
        },
        {
            "code": "juvenilbk2024",
            "host": _env("MSSQL_JUVENIL_HOST", "47.92.172.14"),
            "port": int(_env("MSSQL_JUVENIL_PORT", "10084")),
            "uid": _env("MSSQL_JUVENIL_UID", "sa"),
            "pwd": _env("MSSQL_JUVENIL_PWD", ""),
            "db": _env("MSSQL_JUVENIL_DB", "juvenilbk2024"),
            "sqlPath": "./sysdatas/mssql/sqls/juvenilbk2024"
        },
        {
            "code": "cbs_bj",
            "host": _env("MSSQL_CBSBJ_HOST", "47.92.172.14"),
            "port": int(_env("MSSQL_CBSBJ_PORT", "10084")),
            "uid": _env("MSSQL_CBSBJ_UID", "sa"),
            "pwd": _env("MSSQL_CBSBJ_PWD", ""),
            "db": _env("MSSQL_CBSBJ_DB", "cbs_bj"),
            "sqlPath": "./sysdatas/mssql/sqls/cbs_bj"
        }
    ],
    "io":[
        {
            "code": "femo",
            "root": _env("IO_FEMO_ROOT", "/pyvueapps/svr/pyApiSvr/ioData/femo")
        }
    ],
    "oss":[
        {
            "code":"femo-oss",
            "ak": _env("OSS_FEMO_AK", ""),
            "sk": _env("OSS_FEMO_SK", ""),
            "endpoint":"oss-cn-beijing.aliyuncs.com",
            "bucket":"hhucjsoss"
        }
    ],
    "ossBucket":[
        {
            "code":"hhuoss",
            "bucket":"hhucjsoss",
            "ak": _env("OSS_BUCKET_AK", ""),
            "sk": _env("OSS_BUCKET_SK", ""),
            "endpoint":"oss-cn-beijing.aliyuncs.com",
            "shortEndpoint":"cn-beijing",
            "stsRoleArn": _env("OSS_STS_ROLE_ARN", "")
        }
    ],
    "apps":{
        "bksignup":{
            "dbCode":"bksignup",
            "ossBucketCode":"hhuoss",
            "bucketName" :"hhucjsoss"
        }
    },
    # NOTE: SMS 和阿里云短信的敏感配置，从环境变量读取
    "sms":{
        "juhe_key": _env("SMS_JUHE_KEY", ""),
        "ali_ak": _env("SMS_ALI_AK", ""),
        "ali_sk": _env("SMS_ALI_SK", ""),
        "ali_sign_name": _env("SMS_ALI_SIGN_NAME", "上海极下之光互联网科技"),
        "ali_template_code": _env("SMS_ALI_TEMPLATE_CODE", "SMS_498270499"),
    },
    # NOTE: OSS Live 直播配置
    "ossLive":{
        "ak": _env("OSS_LIVE_AK", ""),
        "sk": _env("OSS_LIVE_SK", ""),
        "playDomain":"playvideo.hhdata.cn",
        "pushDomain":"pushvideo.hhdata.cn",
        "liveStation":"yylive",
        "endpoint":"oss-cn-beijing.aliyuncs.com",
        "bucket":"hhucjsoss",
        "channel":"20240105001",
        "description":"测试使用的直播频道",
    }
}