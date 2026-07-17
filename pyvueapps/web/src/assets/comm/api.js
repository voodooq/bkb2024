import axios from "axios";
import Vue from 'vue'
import flvjs from 'flv.js';
const md5 = require('./md5');
const uuid = require('uuid');

const api = {
    config: {
        apiUrl: "/yyapi",
        msCode: "eqvideo",
        myCode: "sport"
    },
    caches: {},
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
    query(key, queryPs, srcType = 'ms') {
        var me = this;
        var res = {
            status: 0
        };
        return new Promise((su, faild) => {
            try {
                var action = srcType == 'ms' ? 'msquery' : 'myquery';
                var dbCode = srcType == 'ms' ? me.config.msCode : me.config.myCode;
                var ps = {
                    dbCode: dbCode,
                    dbKey: key,
                    ps: queryPs || {}
                }
                me.callApi(action, ps).then(_res => {
                    su(_res);
                })
            } catch (error) {
                console.log(error);
                su(res);
            }
        })
    },
    msQuery(key, queryPs) {
        var me = this;
        var res = {
            status: 0
        };
        return new Promise((su, faild) => {
            try {
                me.query(key, queryPs, 'ms').then(_ => {
                    su(_)
                })
            } catch (error) {
                console.log(error);
                su(res);
            }
        })
    },
    myQuery(key, queryPs) {
        var me = this;
        var res = {
            status: 0
        };
        return new Promise((su, faild) => {
            try {
                me.query(key, queryPs, 'my').then(_ => {
                    su(_)
                })
            } catch (error) {
                console.log(error);
                su(res);
            }
        })
    },
    getCacheObject(key, updateCache = false, updateLocal = false) {
        var me = this;
        var res = null;
        return new Promise((su, fail) => {
            try {
                if (updateCache && me.caches[key]) {
                    delete me.caches[key]
                }
                if (updateLocal) {
                    try {
                        window.localStorage.removeItem(key);
                    } catch (err) {;
                    }
                }
                if (me.caches[key] && me.caches[key] != null) {
                    res = me.caches[key];
                    su(res);
                } else {
                    var flag = false;
                    try {
                        var content = window.localStorage.getItem(key);
                        if (content && content != null && content != "") {
                            var obj = JSON.parse(content);
                            if (obj && obj != null) {
                                me.caches[key] = obj;
                                res = obj;
                                flag = true;
                            }
                        }
                    } catch (err) {
                        flag = false;
                        console.log(err);
                    }
                    if (flag) {
                        su(res);
                    } else {
                        axios.get(key).then(_res => {
                            try {
                                var obj = JSON.parse(_res.data);
                                if (obj && obj != null) {
                                    me.caches[key] = obj;
                                    res = obj;
                                }
                            } catch (errCache) {
                                console.log(errCache);
                            }
                            su(res)
                        })
                    }
                }
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    },
    generateVod(videoCode, startTm, endTm) {
        var me = this;
        var res = null;
        return new Promise((su, fail) => {
            try {
                var action = 'splitOssLive';
                var ps = {
                    code: videoCode,
                    start: startTm,
                    end: endTm
                }
                me.callApi(action, ps).then(_res => {
                    su(_res);
                })
            } catch (error) {
                console.log(error);
                su(res)
            }
        })
    }
};

const eq2024 = {
    api: api,
    datas: {
        sessionKey: "eq2024UserSessionKey",
        userInfo: {},
        adminSessionData: {}
    },
    isLogin() {
        var me = this;
        var res = false;
        try {
            res = me.datas.userInfo && me.datas.userInfo != null &&
                me.datas.userInfo.userCode && me.datas.userInfo.userCode != null &&
                me.datas.userInfo.userCode.length > 0;
        } catch (er) {
            console.log(er);
        }
        return res;
    },
    loadSessionUserInfo() {
        var me = this;
        try {
            me.datas.userInfo = {};
            var content = window.sessionStorage.getItem(me.datas.sessionKey);
            var userInfo = JSON.parse(content);
            me.datas.userInfo = userInfo;
            userInfo = null;
        } catch (er) {
            console.log(er);
        }
    },
    checkLogin(userRole, userCode, pwd) {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var userSec = md5.hex_md5(userCode.toLowerCase() + "$" + pwd);
                var ps = {
                    userRole,
                    userCode,
                    userSec
                };
                var key = "checkLogin";
                me.api.msQuery(key, ps).then(_res => {
                    var flag = _res && _res.data && _res.data.recordset && _res.data.recordset.length > 0;
                    if (flag) {
                        me.datas.userInfo = _res.data.recordset[0];
                        window.sessionStorage.setItem(me.datas.sessionKey, JSON.stringify(me.datas.userInfo));
                    } else {
                        me.datas.userInfo = {};
                        window.sessionStorage.setItem(me.datas.sessionKey, "{}");
                    }
                    su(me.isLogin())
                })
            } catch (error) {
                console.log(error);
                su(me.isLogin());
            }
        })
    },
    checkLoginAdmin(userCode, pwd, gameCode) {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var userSec = md5.hex_md5(userCode.toLowerCase() + "$" + pwd);
                var ps = {
                    userRole: 'admin',
                    userCode,
                    userSec,
                    gameCode
                };
                var key = "checkLoginAdmin";
                me.api.msQuery(key, ps).then(_res => {
                    var flag = _res && _res.data && _res.data.recordset && _res.data.recordset.length > 0;
                    if (flag) {
                        me.datas.userInfo = _res.data.recordset[0];
                        me.datas.userInfo.events = _res.data.recordsetList[1];
                        me.datas.userInfo.phases = _res.data.recordsetList[2];
                        window.sessionStorage.setItem(me.datas.sessionKey, JSON.stringify(me.datas.userInfo));
                    }
                    su(me.isLogin())
                })
            } catch (error) {
                console.log(error);
                su(me.isLogin());
            }
        })
    },
    setAdminSessionData(sessionData) {
        var me = this;
        try {
            me.datas.adminSessionData = sessionData;
            var key = "eqVideo.adminSession";
            window.localStorage.setItem(key, JSON.stringify(sessionData));
        } catch (error) {
            console.log(error)
        }
    },
    getAdminSessionData() {
        var me = this;
        try {
            me.datas.adminSessionData = {};
            var key = "eqVideo.adminSession";
            var content = window.localStorage.getItem(key);
            me.datas.adminSessionData = JSON.parse(content);
        } catch (error) {
            console.log(error)
        }
        return me.datas.adminSessionData;
    },
    getGameInfo(gameCode) {
        var me = this;
        return new Promise((su, fail) => {
            try {
                console.log('getGameInfo', gameCode)
                var ps = { gameCode };
                var key = "getGameInfo";
                me.api.msQuery(key, ps).then(_res => {
                    var flag = _res && _res.data && _res.data.recordset && _res.data.recordset.length > 0;
                    if (flag) {
                        su({
                            success: 1,
                            gameInfo: _res.data.recordset[0],
                            events: _res.data.recordsetList[1],
                            phases: _res.data.recordsetList[2],
                        })
                    } else {
                        su({ success: 0 })
                    }
                })
            } catch (error) {
                console.log(error);
                su({ success: 0 })
            }
        })
    },
    getHomeGames() {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var ps = {};
                var key = "getHomeGames";
                me.api.msQuery(key, ps).then(_res => {
                    var flag = _res && _res.data && _res.data.recordset && _res.data.recordset.length > 0;
                    su(flag ? _res.data.recordset : [])
                })
            } catch (error) {
                console.log(error);
                su([]);
            }
        })
    },
    getGamesByStatus(status) {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var ps = {
                    status
                };
                var key = "getGamesByStatus";
                me.api.msQuery(key, ps).then(_res => {
                    var flag = _res && _res.data && _res.data.recordset && _res.data.recordset.length > 0;
                    su(flag ? _res.data.recordset : [])
                })
            } catch (error) {
                console.log(error);
                su([]);
            }
        })
    },
    getGameVideos(gameCode) {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var ps = {
                    gameCode
                };
                var key = "getGameVideos";
                me.api.msQuery(key, ps).then(_res => {
                    var flag = _res && _res.data && _res.data.recordsetList &&
                        _res.data.recordsetList.length > 1 && _res.data.recordsetList[0].length > 0;
                    var res = {
                        success: 0,
                        gameInfo: flag ? _res.data.recordsetList[0][0] : {},
                        videos: flag ? _res.data.recordsetList[1] : []
                    }
                    if (res && res.gameInfo && res.gameInfo.gameCode) {
                        res.success = 1;
                    }
                    su(res)
                })
            } catch (error) {
                console.log(error);
                su([]);
            }
        })
    },
    getVideoInfo(videoCode) {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var ps = {
                    videoCode
                };
                var key = "getVideoInfo";
                me.api.msQuery(key, ps).then(_res => {
                    var flag = _res && _res.data && _res.data.recordset &&
                        _res.data.recordset.length > 0;
                    var res = flag ? _res.data.recordset[0] : {};
                    su(res)
                })
            } catch (error) {
                console.log(error);
                su([]);
            }
        })
    },
    setVideoStatus(resId, status) {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var ps = {
                    resId,
                    status
                };
                var key = "setVideoStatus";
                me.api.msQuery(key, ps).then(_res => {
                    su(_res)
                })
            } catch (error) {
                console.log(error);
                su([]);
            }
        })
    },
    setVodFlag(resId, vodFlag) {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var ps = {
                    resId,
                    vodFlag
                };
                var key = "setVodFlag";
                me.api.msQuery(key, ps).then(_res => {
                    su(_res)
                })
            } catch (error) {
                console.log(error);
                su([]);
            }
        })
    },
    getVodInfo(resId) {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var ps = {
                    resId
                };
                var key = "getVodInfo";
                me.api.msQuery(key, ps).then(_res => {
                    var flag = _res && _res.data && _res.data.recordset &&
                        _res.data.recordset.length > 0;
                    var res = flag ? _res.data.recordset[0] : {};
                    su(res)
                })
            } catch (error) {
                console.log(error);
                su([]);
            }
        })
    },
    getLiveVideoInfo() {
        var me = this;
        return new Promise((su, fail) => {
            try {
                var ps = {
                    gameCode: '20240105001'
                };
                var key = "getLiveVideoInfo";
                me.api.msQuery(key, ps).then(_res => {
                    var flag = _res && _res.data && _res.data.recordset &&
                        _res.data.recordset.length > 0;
                    var res = flag ? _res.data.recordset[0] : {};
                    su(res)
                })
            } catch (error) {
                console.log(error);
                su([]);
            }
        })
    },

    //---- mo videos --- 
};

const eqVideo = {
    getStatic(url) {
        var me = this;
        var res = null;
        return new Promise((su, fa) => {
            try {
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
    }
};
/*
var ps = {
    c: "m",
    n: "新类型"
}
api.query("signup2024/newRole", ps, 'ms').then(_r => {
    console.log(_r)
    return api.query("sport/newRole", ps, 'my');
}).then(_ => {
    console.log(_)
})
*/
Vue.prototype.$api = api;
Vue.prototype.$eq = eq2024;
Vue.prototype.$eqVideo = eqVideo;