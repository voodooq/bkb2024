<template>
    <div class="vod">
        <div class="filterPan">
            <div class="event item">
                <div class="lab">项目</div>
                <div class="content">
                    <ul class="lstPick">
                        <li
                            v-for="(item,index) in dicts.events" :key="index"
                            :class="index==dictIndex.event?'active':''"
                            @click="onPickEvent(index)"
                        >
                            {{item.eventName}}
                        </li>
                    </ul>
                </div>
            </div>
            <el-divider></el-divider>
            <div class="phase item">
                <div class="lab">等级</div>
                <div class="content">
                    <ul class="lstPick">
                        <li
                            v-for="(item,index) in dicts.phases" :key="index"
                            :class="index==dictIndex.phase?'active':''"
                            @click="onPickPhase(index)"
                        >
                            {{item.phaseName}}
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="videoList">
            <div
                v-for="(item,index) in videos" :key="index"
                class="videoItem"
                @click="playVod(item.resId)"
            >
                <div class="thumb">
                    <img :src="thumb" alt="">
                </div>
                <div class="info">
                    <div class="title">
                        <div class="ath">{{item.athName}}</div>
                        <div class="horse">
                            <img :src="sys.imgHorse" alt=""> <div class="lab">{{item.horseName}}</div>
                        </div>
                    </div>
                    <div class="org">{{item.orgName}}</div>
                </div> 
            </div>
        </div>
    </div>
</template>

<script>
    import Hls from 'hls.js'; 
    export default {
        mounted(){
            var me=this;
            try {
                console.log('eqvideoVod');
                me.$nextTick().then(_=>{
                    me.loadStatus();
                    me.getGameInfo();
                })
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{               
                sys:{
                    gameCode:"20240105001",
                    logoImg:require('./imgs/eqlogo.png'),
                    imgHorse: require('./imgs/iconhorse.png'),
                    img404:require('./imgs/404.png'),    
                    gameInfoUrl:"http://hhucjsoss.oss-cn-beijing.aliyuncs.com/eqvideo/20240105001/gameInfo.txt"  ,
                    localKey:"eqmoVod"              
                },
                gameInfo:{},
                dicts:{
                    events:[{"eventId":1,"eventCode":"E2","eventName":"盛装舞步","eventDesc":""},{"eventId":2,"eventCode":"E1","eventName":"场地障碍","eventDesc":""}],
                    phases:[{"phaseId":1,"phaseCode":"J1","phaseName":"初一级","phaseDesc":""},{"phaseId":2,"phaseCode":"J2","phaseName":"初二级","phaseDesc":""},{"phaseId":3,"phaseCode":"J3","phaseName":"初三级","phaseDesc":""},{"phaseId":4,"phaseCode":"S1","phaseName":"中一级","phaseDesc":""},{"phaseId":5,"phaseCode":"S2","phaseName":"中二级","phaseDesc":""},{"phaseId":6,"phaseCode":"S3","phaseName":"中三级","phaseDesc":""}]
                },
                dictIndex:{
                    event:0 ,
                    phase:0
                },
                thumb:require('./imgs/swiper/2.jpg'),
                videos:[]
            }
        },
        methods:{
            saveStatus(){
                var me=this;
                try {  
                    window.sessionStorage.setItem(me.localKey,JSON.stringify(me.dictIndex));
                } catch (error) {
                    console.log(error)
                }
            },
            loadStatus(){
                var me=this;
                try {  
                    var indexJson = window.sessionStorage.getItem(me.localKey);
                    var info = JSON.parse(indexJson);
                    if( info && info!=null){
                        me.dictIndex = info
                    }
                } catch (error) {
                    console.log(error)
                }
            },
            onPickEvent(ind){
                var me=this;
                try {  
                    me.dictIndex.event = ind ;
                    me.saveStatus();
                    me.refresh();
                } catch (error) {
                    console.log(error)
                }
            },
            onPickPhase(ind){
                var me=this;
                try {  
                    me.dictIndex.phase = ind ;
                    me.saveStatus();
                    me.refresh();
                } catch (error) {
                    console.log(error)
                }
            },
            refresh(){
                var me=this;
                try {  
                    var ps = {
                        gameCode: me.gameInfo.gameCode ,
                        eventCode : me.dicts.events[me.dictIndex.event].eventCode ,
                        phaseCode : me.dicts.phases[me.dictIndex.phase].phaseCode
                    };
                    var key = "getVodRes";
                    me.$eq.api.msQuery(key, ps).then(_res => {
                        var flag = _res && _res.data && _res.data.recordset  ;
                        if (flag) {
                            me.videos = _res.data.recordset;
                        } 
                    })

                } catch (error) {
                    console.log(error)
                }
            },
            getGameInfo(){
                var me=this;
                try {  
                    me.$eq.getGameInfo(me.sys.gameCode).then(info=>{
                        console.log(info);
                        me.gameInfo = info.gameInfo;
                        me.dicts.events = info.events;
                        me.dicts.phases = info.phases;

                        me.refresh();
                    }) 
                } catch (error) {
                    console.log(error)
                }
            },
            playVod(resId){
                var me=this;
                try {  
                    me.$router.push({
                        path:"/eqmoVod",
                        query:{
                            resId:resId
                        }
                    })
                } catch (error) {
                    console.log(error)
                }
            }
        }
    }
</script>

<style lang="less" scoped>
    .filterPan{
        position: fixed;
        width: 100%;
        background-color: #fff;
        z-index: 999;
        padding: 15px;
        padding-bottom: 0;
        font-size: 0.9em;
        box-shadow: 0 0 10px 0 #ddd;
        .item{
            display: flex;            
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 10px;
            .lab{ 
                height: 32px;
                line-height: 32px;
                width: 80px;
                background-color: #f2f3f9;
            }
            .content{
                .lstPick{
                    display: grid;
                    grid-column-gap: 10px;
                    grid-template-columns: auto auto auto;
                    li{
                        height: 32px;
                        line-height: 32px;
                        width: 70px;
                        text-align: center;
                    }
                    li.active{
                        background-color: #0077fe;
                        color: #fff;
                    }
                }

            }
        } 
    }

    .videoList{
        padding: 15px;
        padding-top: 215px;
        .videoItem{
            display: flex;
            margin-bottom: 10px;
            background-color: #fff;
            padding: 5px;
            box-shadow: 0 0 10px 0 #ddd;
            .thumb{
                width: 120px;
                height: 70px;
                img{
                    height: 100%;
                    width: 100%;
                    object-fit: cover;
                }
            }
            .info{
                flex: 1;
                padding: 10px;
                .title{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    font-weight: bold;
                    margin-bottom: 10px;
                    .horse{
                        display: flex;
                        align-items: center;
                        img{
                            height: 16px;
                        }
                        .lab{
                            padding-left: 5px;
                            font-size: 12px;
                            color: #042852;
                        }
                    }
                }
                .org{
                    text-align: left;
                    font-size: 0.9em;
                    color: #777;

                }
            }
        }
    }

</style>