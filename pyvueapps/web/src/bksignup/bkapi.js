import axios from "axios";
//const md5 = require('./md5');
const bkapi = {
    config: {
        apiUrl: "/yyapi",
        ossCode: "hhuoss",
        rootUrl: "https://hhucjsoss.oss-cn-beijing.aliyuncs.com/bksignup2024/BK202401BJ",
        sessionKey: "sessionKey.bkSignup2024",
        bucket: "hhucjsoss",
        dbCode: "bksignup"
    },
    session: {},
    sts: {
        updateTime: 0,
        duration: 20 * 60,
        enable: 0
    },
    gameData: {},
    callApi(action, params) {
        var me = this;
        var res = {
            status: 0
        };
        return new Promise((su, faild) => {
            try {
                var postData = {
                    action: action,
                    params: params,
                    result: {}
                }
                axios.post(me.config.apiUrl, postData).then(_res => {
                    su(_res.data)
                })
            } catch (error) {
                console.log(error);
                su(res);
            }
        })
    },
    query(dbKey, params) {
        var me = this;
        return new Promise((su, faild) => {
            try {
                var action = "db/query"
                var ps = {
                    dbCode: me.config.dbCode,
                    dbKey: dbKey,
                    dbPs: params && params != null ? params : {}
                }
                me.callApi(action, ps).then(_res => {
                    console.log(_res)
                    su(_res)
                })

            } catch (error) {
                console.log(error);
                su();
            }
        })
    },
    getSts(roleSessionName) {
        var me = this;
        return new Promise((su, faild) => {
            try {
                me.sts.enable = 0;
                var nowTm = (new Date()).getTime()
                var ststEnable = me.sts &&
                    me.sts.updateTime &&
                    me.sts.updateTime > 0 &&
                    nowTm - me.sts.updateTime < 1000 * me.sts.duration;
                if (ststEnable) {
                    me.sts.enable = 1
                    su(me.sts)
                } else {
                    me.sts = {
                        updateTime: 0,
                        duration: 20 * 60,
                        stsInfo: {}
                    };
                    me.sts = {
                        updateTime: 0,
                        duration: 20 * 60,
                    };
                    var action = 'oss/bucket/stsInfo';
                    var params = {
                        ossCode: me.config.ossCode,
                        roleSessionName: roleSessionName,
                        duration: me.sts.duration
                    };
                    me.callApi(action, params).then(_res => {
                        console.log(_res)
                        if (_res && _res.status && _res.status == 1) {
                            me.sts.stsInfo = _res.stsInfo;
                            me.sts.updateTime = nowTm;
                            me.sts.enable = 1;
                        }
                        su(me.sts);
                    })
                }

            } catch (error) {
                console.log(error);
                su(me.sts);
            }
        })
    },
    uploadFile(roleSessionName, file, targetFn) {
        var me = this;
        var res = {
            status: 0,
            url: ""
        };
        return new Promise((su, faild) => {
            try {
                me.getSts(roleSessionName).then(_ => {
                    var flag = me.sts && me.sts.enable && me.sts.enable == 1;
                    if (flag) {
                        var ak = me.sts.stsInfo.Credentials.AccessKeyId;
                        var sk = me.sts.stsInfo.Credentials.AccessKeySecret;
                        var token = me.sts.stsInfo.Credentials.SecurityToken;
                        var bucket = me.config.bucket;

                        var client = new OSS({
                            // yourRegion填写Bucket所在地域。以华东1（杭州）为例，yourRegion填写为oss-cn-hangzhou。
                            region: "oss-cn-beijing",
                            // 从STS服务获取的临时访问密钥（AccessKey ID和AccessKey Secret）。
                            accessKeyId: ak,
                            accessKeySecret: sk,
                            // 从STS服务获取的安全令牌（SecurityToken）。
                            stsToken: token,
                            // 填写Bucket名称。
                            bucket: bucket,
                        });
                        client.put(targetFn, file).then(r => {
                            console.log(r);
                            if (r && r.url && r.url.length > 0) {
                                res.status = 1;
                                res.url = r.url;
                            }
                            su(res)
                        }).catch(e => {
                            console.log(e)
                            su(res)
                        })
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res);
            }
        })
    },
    getStatic(dataPath) {
        var me = this;
        var res = null;
        return new Promise((su, fa) => {
            try {
                var url = me.config.rootUrl + "/" + dataPath + '.txt?t=' + (new Date()).getTime();
                console.log(url)
                axios.get(url).then(res => {
                    if (res && res.data) {
                        res = res.data;
                    }
                    su(res)
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    init() {
        var me = bkapi;
        return new Promise((su, fa) => {
            try {
                var ac = 'bksignup/init'
                var ps = {}
                me.callApi(ac, ps).then(res => {
                    console.log(res);
                    su();
                })
            } catch (error) {
                console.log(error);
                su()
            }
        })
    },
    exportGameData() {
        var me = bkapi;
        return new Promise((su, fa) => {
            try {
                var ac = 'bksignup/exportGameData'
                var ps = {}
                me.callApi(ac, ps).then(res => {
                    console.log(res);
                    return me.getGameData();
                }).then(_ => {
                    su();
                })
            } catch (error) {
                console.log(error);
                su()
            }
        })
    },
    getGameData() {
        var me = bkapi;
        return new Promise((su, fa) => {
            try {
                var dataPath = 'gameInfo';
                me.getStatic(dataPath).then(_res => {
                    me.gameData = _res;
                    su();
                })
            } catch (error) {
                console.log(error);
                su()
            }
        })
    },
    getSession() {
        var me = bkapi;
        return new Promise((su, fa) => {
            try {
                var hasSession = () => {
                    return me.session && me.session.sessionId
                }
                if (hasSession()) {
                    su()
                } else {
                    var content = window.sessionStorage.getItem(me.config.sessionKey);
                    try {
                        var session = JSON.parse(content)
                        if (session && session.sessionId) {
                            me.session = session;
                        }
                    } catch (er) {
                        console.log(er)
                    }
                }
                if (hasSession()) {
                    su();
                } else {
                    var apiPath = 'bksignup/sessionCreate';
                    me.callApi(apiPath, {}).then(_res => {
                        console.log(_res)
                        if (_res && _res.status == 1) {
                            me.session = _res.res;
                            window.sessionStorage.setItem(me.config.sessionKey, JSON.stringify(me.session))
                        } else {
                            me.session = {};
                        }
                        su()
                    })
                }
            } catch (error) {
                console.log(error);
                su()
            }
        })
    },
    updateUserData(forceUpdate = false) {
        var me = bkapi;
        var res = {
            status: 0
        }
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var flag = me.isLogin();
                    if (flag) {
                        var onUpdate = () => {
                            var dataPath = 'users/' + me.session.tel;
                            me.getStatic(dataPath).then(_res => {
                                console.log(_res)
                                try {
                                    res.status = 1;
                                    _res.teams.forEach(t => {
                                        t.members = _res.members.filter(m => {
                                            return m.teamCode == t.teamKey;
                                        })
                                    })
                                    res.userDatas = _res.teams;

                                } catch (ee) {
                                    console.log(ee)
                                }
                                su(res);
                            })
                        }
                        if (forceUpdate) {
                            var apiPath = "bksignup/sessionExecuteUserData";
                            var ps = {
                                tel: me.session.tel
                            };
                            me.callApi(apiPath, ps).then(_res => {
                                console.log(_res);
                                if (_res && _res.status == 1) {
                                    onUpdate();
                                } else {
                                    su(_res)
                                }
                            })
                        } else {
                            onUpdate();
                        }

                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    uploadLogoImg(file, targetFn) {
        var me = bkapi;
        var res = {
            status: 0
        }
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var flag = me.isLogin();
                    if (flag) {
                        me.uploadFile(me.session.sessionId, file, targetFn).then(_res => {
                            su(_res)
                        })
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    //获取验证码
    requestSessionValid(tel) {
        var me = bkapi;
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var apiPath = "bksignup/sessionValid"
                    var ps = {
                        sessionId: me.session.sessionId,
                        tel: tel
                    };
                    me.callApi(apiPath, ps).then(_res => {
                        console.log(_res);
                        if (_res.status == 1) {
                            me.session = _res.res;
                            me.session.loginStatus = 0;
                            window.sessionStorage.setItem(me.config.sessionKey, JSON.stringify(me.session))
                        }
                        su();
                    })
                })
            } catch (error) {
                console.log(error);
                su()
            }
        })
    },
    checkLogin(validCode) {
        var me = bkapi;
        var res = 0
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var flag = me.session && me.session.sessionId &&
                        me.session.tel && me.session.tel.length > 0;
                    if (flag) {
                        var sec = md5.hex_md5([me.session.sessionId, me.session.tel, validCode].join('.'));
                        if (sec == me.session.sec) {
                            var apiPath = "bksignup/sessionCheckLogin";
                            var ps = {
                                sessionId: me.session.sessionId,
                                tel: me.session.tel,
                                validCode: validCode
                            };
                            me.callApi(apiPath, ps).then(_res => {
                                console.log(_res);
                                if (_res && _res.status == 1) {
                                    me.session.loginStatus = 1;
                                    window.sessionStorage.setItem(me.config.sessionKey, JSON.stringify(me.session))
                                    res = 1;
                                }
                                su(res)
                            })
                        } else {
                            su(res)
                        }
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    isLogin() {
        var me = this;
        var res = false;
        try {
            res = me.session && me.session.loginStatus > 0;
        } catch (error) {
            console.log(error)
        }
        return res;
    },
    teamCreate(teamName, eventCode, areaCode, phaseCode, logoImg) {
        var me = bkapi;
        var res = {
            status: 0,
            team: {}
        }
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var flag = me.isLogin();
                    if (flag) {
                        var apiPath = "bksignup/teamCreate";
                        var ps = {
                            sessionId: me.session.sessionId,
                            tel: me.session.tel,
                            teamName,
                            eventCode,
                            areaCode,
                            phaseCode,
                            logoImg
                        };
                        me.callApi(apiPath, ps).then(_res => {
                            console.log(_res);
                            su(_res)
                        })
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    teamSetSignupStatus(teamKey, teamStatus) {
        var me = bkapi;
        var res = {
            status: 0,
            team: {}
        }
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var flag = me.isLogin();
                    if (flag) {
                        var apiPath = "bksignup/teamSetSignupStatus";
                        var ps = {
                            sessionId: me.session.sessionId,
                            tel: me.session.tel,
                            teamKey,
                            teamStatus
                        };
                        me.callApi(apiPath, ps).then(_res => {
                            console.log(_res);
                            su(_res)
                        })
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    teamSetSignupStatusAdmin(teamKey, teamStatus, teamExInfo) {
        var me = bkapi;
        var res = {
            status: 0,
            team: {}
        }
        return new Promise((su, fa) => {
            try {
                var apiPath = "bksignup/teamSetSignupStatusAdmin";
                var ps = {
                    teamKey,
                    teamStatus,
                    teamExInfo
                };
                me.callApi(apiPath, ps).then(_res => {
                    console.log(_res);
                    su(_res)
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    memberCreate(teamKey, memberName, functionCode, genderCode, idTypeCode, idCode, memTel, photoImg, idImgList) {
        var me = bkapi;
        var res = {
            status: 0,
            membere: {}
        }
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var flag = me.isLogin();
                    if (flag) {
                        var apiPath = "bksignup/memberCreate";
                        var ps = {
                            sessionId: me.session.sessionId,
                            tel: me.session.tel,
                            teamKey,
                            memberName,
                            functionCode,
                            genderCode,
                            idTypeCode,
                            idCode,
                            memTel,
                            photoImg,
                            idImgList
                        };
                        me.callApi(apiPath, ps).then(_res => {
                            console.log(_res);
                            su(_res)
                        })
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    memberEdit(memKey, memberName, functionCode, genderCode, idTypeCode, idCode, memTel, photoImg, idImgList) {
        var me = bkapi;
        var res = {
            status: 0,
            membere: {}
        }
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var flag = me.isLogin();
                    if (flag) {
                        var apiPath = "bksignup/memberEdit";
                        var ps = {
                            sessionId: me.session.sessionId,
                            tel: me.session.tel,
                            memKey,
                            memberName,
                            functionCode,
                            genderCode,
                            idTypeCode,
                            idCode,
                            memTel,
                            photoImg,
                            idImgList
                        };
                        me.callApi(apiPath, ps).then(_res => {
                            console.log(_res);
                            su(_res)
                        })
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    memberUpdateExInfo(memKey, height, weight, width, bib, birthday, masterName, masterRelation, masterTel) {
        var me = bkapi;
        var res = {
            status: 0,
            membere: {}
        }
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var flag = me.isLogin();
                    if (flag) {
                        var apiPath = "bksignup/memberUpdateExInfo";
                        var ps = {
                            sessionId: me.session.sessionId,
                            tel: me.session.tel,
                            memKey,
                            height,
                            weight,
                            width,
                            bib,
                            birthday,
                            masterName,
                            masterRelation,
                            masterTel
                        };
                        me.callApi(apiPath, ps).then(_res => {
                            console.log(_res);
                            su(_res)
                        })
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    memberRemove(memKey) {
        var me = bkapi;
        var res = {
            status: 0,
            membere: {}
        }
        return new Promise((su, fa) => {
            try {
                me.getSession().then(_ => {
                    var flag = me.isLogin();
                    if (flag) {
                        var apiPath = "bksignup/memberRemove";
                        var ps = {
                            sessionId: me.session.sessionId,
                            tel: me.session.tel,
                            memKey
                        };
                        me.callApi(apiPath, ps).then(_res => {
                            console.log(_res);
                            su(_res)
                        })
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    }
};
const wxpay = {
    config: {
        mchCode: "yysport",
        urls: {
            api: "",
            apiPath_getopenId: "https://dev.yy-sport.com.cn/wx/wxpay/getOpenId?wxCode={code}&mchCode={mchCode}",
            apiPath_requestOrder: "https://dev.yy-sport.com.cn/wx/wxpay/requestOrder"
        },
        wxpaySessionKey: "wxpayKey",
    },
    wxInfo: {
        code: "",
        openId: "oFwIT6UV45soFM9vP3JLZdUI3Iic"
    },
    getOpenId() {
        var me = this;
        var res = {
            status: 0,
            openId: ""
        }
        return new Promise((su, fa) => {
            try {
                var content = window.sessionStorage.getItem(me.config.wxpaySessionKey)
                if (content && content != "") {
                    try {
                        var obj = JSON.parse(content);
                        res.openId = obj.openId;
                        res.status = 1;
                    } catch (error) {
                        console.log(error);
                    }
                    su(res)
                } else {
                    var _url = window.location.href;
                    var hasCodeStateFlag = _url.indexOf('?') > 0 && _url.indexOf('code=') > 0 && _url.indexOf('state=') > 0;
                    if (hasCodeStateFlag) {
                        var pos = _url.indexOf("?");
                        var str = _url.substring(pos + 1, _url.length)
                        var searchParams = new URLSearchParams(str);
                        me.wxInfo.code = searchParams.get('code');
                        var url = me.config.urls.apiPath_getopenId.replace('code', mw.wxInfo.code).replace('mchCode', me.config.mchCode)
                        axios.get(url).then(_res => {
                            if (_res.status == 1) {
                                window.sessionStorage.setItem(me.config.wxpaySessionKey, JSON.stringify({ openId: _res.result }))
                                me.wxInfo.openId = _res.result;
                                res = {
                                    status: 1,
                                    openId: me.wxInfo.openId

                                }
                            }
                            su(res)
                        })
                    } else {
                        su(res)
                    }
                }
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    requestOrder(openId, out_trade_no, total_fee, time_start, time_expire, body, attach, orderDesc) {
        var me = this;
        var res = {
            status: 0,
            orderInfo: {},
            invoke: {}
        }
        return new Promise((su, fa) => {
            try {
                var ps = {
                    "mchCode": me.config.mchCode,
                    "openId": openId,
                    "body": body,
                    "attach": attach,
                    "out_trade_no": out_trade_no,
                    "total_fee": total_fee,
                    "spbill_create_ip": "0.0.0.0",
                    "time_start": time_start,
                    "time_expire": time_expire,
                    "orderDesc": orderDesc
                }
                console.log(ps)
                var url = me.config.urls.apiPath_requestOrder;
                axios.post(url, ps).then(_res => {
                    console.log(_res);
                    try {
                        var flag = _res && _res.data && _res.data.status == 1 &&
                            _res.data.result && _res.data.result.resquestStatus == 1;
                        if (flag) {
                            res.orderInfo = ps;
                            res.invoke = _res.data.result.clientParams;
                            res.status = 1;
                        }
                    } catch (ee) {
                        console.log(ee)
                    }
                    su(res);
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    invokePay(invokeParams) {
        var me = this;
        var res = {
            status: 0,
            msg: ""
        }
        return new Promise((su, fa) => {
            try {
                WeixinJSBridge.invoke(
                    'getBrandWCPayRequest', invokeParams,
                    function(_res) {
                        console.log('invoke pay result:', _res.err_msg)
                        var msg = {
                            "get_brand_wcpay_request:ok": "支付成功",
                            "get_brand_wcpay_request:cancel": "支付过程中用户取消",
                            "get_brand_wcpay_request:fail": "支付失败",
                        }
                        if (_res.err_msg == 'get_brand_wcpay_request:ok') {
                            res.status = 1;
                        }
                        res.msg = msg[_res.err_msg];
                        su(res)
                    });
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    showWxPay(out_trade_no, total_fee, time_start, time_expire, body, attach, orderDesc) {
        var me = this;
        var res = {
            status: 0,
            msg: ""
        }
        return new Promise((su, fa) => {
            try {
                me.getOpenId().then(_res => {
                    return me.requestOrder(
                        me.wxInfo.openId,
                        out_trade_no, total_fee, time_start, time_expire, body, attach, orderDesc
                    )
                }).then(_resOrder => {
                    if (_resOrder.status == 1) {
                        var params = _resOrder.invoke;
                        me.invokePay(params).then(_invokeRes => {
                            su(_invokeRes)
                        })
                    } else {
                        su(res)
                    }
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    }
}

export {
    bkapi,
    wxpay
}