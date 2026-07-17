import axios from "axios";
import Vue from 'vue'
import flvjs from 'flv.js';
const uuid = require('uuid');

const gameResult = {
    config: {
        //dataPath: "/static/femo"https://hhucjsoss.oss-cn-beijing.aliyuncs.com/game001/sysData.txt
        dataPath: "https://hhucjsoss.oss-cn-beijing.aliyuncs.com/game002"
    },
    sysInfo: {
        gameInfo: {},
        imgs: {
            top: require("./imgs/per_apply_bg.png"),
            medals: {
                G: require("./imgs/medal/g.png"),
                S: require("./imgs/medal/s.png"),
                B: require("./imgs/medal/b.png"),
            }
            //top: require("./imgs/bg.png")
        },
        events: [],
        dicts: {
            event: [
                { code: "I", lab: "个人赛" },
                { code: "T", lab: "团体赛" },
            ],
            gender: [
                { code: "M", lab: "男子" },
                { code: "F", lab: "女子" }
            ],
            category: [

            ],
            weapon: [
                { code: "花剑", lab: "花剑" },
                { code: "重剑", lab: "重剑" },
                { code: "佩剑", lab: "佩剑" }
            ]
        },
    },
    getStaticData(dataPath) {
        var me = this;
        return new Promise((su, fa) => {
            try {
                var resPath = dataPath.indexOf('.') > 0 ? dataPath : (dataPath + ".txt");
                var url = [me.config.dataPath, resPath].join("/");
                axios.get(url).then(res => {
                    console.log(url, res);
                    if (res && res.data) {
                        res = res.data;
                    }
                    su(res)
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    loadSysDatas() {
        var me = this;
        return new Promise((su, fa) => {
            try {
                console.log('load game result sys data.')
                var dataPath = "sysData";
                me.getStaticData(dataPath).then(_res => {
                    console.log(_res);
                    try {
                        me.sysInfo.gameInfo = _res[0][0];
                        me.sysInfo.dicts.weapon = _res[1];
                        me.sysInfo.dicts.gender = _res[2];
                        me.sysInfo.dicts.event = _res[3];
                        me.sysInfo.events = _res[4];
                        su();
                    } catch (err) {
                        console.log(err);
                        su();
                    }
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    getDualPhases(eventCode) {
        var me = this;
        return new Promise((su, fa) => {
            try {
                var dataPath = ["dualPhase", eventCode].join("/");
                me.getStaticData(dataPath).then(_res => {
                    su(_res)
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    getStartList(eventCode) {
        var me = this;
        return new Promise((su, fa) => {
            try {
                var dataPath = ["startList", eventCode].join("/");
                me.getStaticData(dataPath).then(_res => {
                    su(_res)
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    getStartListTeam(eventCode) {
        var me = this;
        return new Promise((su, fa) => {
            try {
                var dataPath = ["startListTeam", eventCode].join("/");
                me.getStaticData(dataPath).then(_res => {
                    var teams = _res[0];
                    var aths = _res[1];
                    teams.forEach(t => {
                        t.members = aths.filter(a => {
                            return t.teamCode == a.teamCode;
                        }).map(a => {
                            return a.athName;
                        }).join(' ');
                    })
                    su(teams)
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    getPoolResult(eventCode) {
        var me = this;
        return new Promise((su, fa) => {
            try {
                var dataPath = ["poolResult", eventCode].join("/");
                me.getStaticData(dataPath).then(_res => {
                    var pools = {}
                    _res.forEach(r => {
                        var pool = pools[r.poolCode]
                        if (!(pool && pool != null)) {
                            pool = {
                                poolCode: r.poolCode,
                                items: []
                            };
                            pools[pool.poolCode] = pool;
                        }
                        pool.items.push(r)
                    })
                    var _pools = Object.values(pools)
                    su(_pools)
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    getPoolRank(eventCode) {
        var me = this;
        return new Promise((su, fa) => {
            try {
                var dataPath = ["poolRank", eventCode].join("/");
                me.getStaticData(dataPath).then(_res => {
                    su(_res)
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    getDualPhaseMatch(phaseId) {
        var me = this;
        return new Promise((su, fa) => {
            try {
                var dataPath = ["dualPhaseMatch", phaseId + ""].join("/");
                me.getStaticData(dataPath).then(_res => {
                    _res.forEach(r => {
                        if (r.homeRegId < 0) {
                            r.homeAthName = 'bye';
                            r.awayWinSets = 1;
                        }
                        if (r.awayRegId < 0) {
                            r.awayAthName = 'bye'
                            r.homeWinSets = 1;
                        }
                    })
                    su(_res)
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    getEventRank(eventCode) {
        var me = this;
        return new Promise((su, fa) => {
            try {
                var dataPath = ["eventRank", eventCode].join("/");
                me.getStaticData(dataPath).then(_res => {
                    su(_res)
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    loadSysDatas__() {
        var me = this;
        return new Promise((su, fa) => {
            try {
                console.log('load game result sys data.')
                var dataPath = "gameinfo";
                me.getStaticData(dataPath).then(_res => {
                    me.sysInfo.gameInfo = _res.game[0];
                    var gameCode = me.sysInfo.gameInfo.GameCode;
                    if (gameCode && gameCode != null) {
                        dataPath = "json/EventList_" + gameCode;
                        me.getStaticData(dataPath).then(_events => {
                            me.sysInfo.events = _events.Events;
                            me.sysInfo.events.forEach(ev => {
                                var item = me.sysInfo.dicts.category.find(i => {
                                    return i.code == ev.category;
                                });
                                if (item == null) {
                                    me.sysInfo.dicts.category.push({
                                        code: ev.category,
                                        lab: ev.category
                                    })
                                }
                            })
                            su();
                        })
                    } else {
                        su();
                    }
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
    getEventData(eventCode) {
        var me = this;
        return new Promise((su, fa) => {
            try {
                var dataPath = ["json", eventCode].join("/");
                me.getStaticData(dataPath).then(_res => {
                    su(_res)
                })
            } catch (er) {
                console.log(er);
                su()
            }
        })
    },
};

export default gameResult;