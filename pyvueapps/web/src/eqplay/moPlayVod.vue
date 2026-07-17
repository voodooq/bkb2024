<template>
    <div class="playVod">
        <div class="header">
            <i class="fa fa-chevron-left btnIcon" @click="$router.back()"></i>
            <div class="athName">
                {{vodInfo.athName}}
            </div>
            <div class="title">
                视频回放
            </div>
        </div>
        <div class="content">
            <div class="gameInfo">
                <div class="r">
                    <div class="liveVideo">
                        <video id="liveVideoPlayer" ref="videoRef" controls></video>
                    </div>

                </div>
                <div class="r">
                    <i class="infoIcon fa fa-tv"></i>
                    <div class="info">
                        <div class="lab">赛事代码</div>
                        <div class="value">{{vodInfo.gameCode}}</div>
                    </div>
                </div>
                <div class="r">
                    <i class="infoIcon fa fa-institution"></i>
                    <div class="info">
                        <div class="lab">赛事名称</div>
                        <div class="value">{{vodInfo.gameName}}</div>
                    </div>
                </div> 
                <div class="r">
                    <i class="infoIcon fa fa-sitemap"></i>
                    <div class="info">
                        <div class="lab">项目</div>
                        <div class="value">{{vodInfo.eventName}}</div>
                    </div>
                </div> 
                <div class="r">
                    <i class="infoIcon fa fa-sort-numeric-desc"></i>
                    <div class="info">
                        <div class="lab">等级</div>
                        <div class="value">{{vodInfo.phaseName}}</div>
                    </div>
                </div> 
                <div class="r">
                    <i class="infoIcon fa fa-server"></i>
                    <div class="info">
                        <div class="lab">单位</div>
                        <div class="value">{{vodInfo.address}}</div>
                    </div>
                </div> 
                <div class="r">
                    <i class="infoIcon fa fa-graduation-cap"></i>
                    <div class="info">
                        <div class="lab">姓名</div>
                        <div class="value">{{vodInfo.athName}}</div>
                    </div>
                </div> 
                <div class="r">
                    <i class="infoIcon fa fa-heartbeat"></i>
                    <div class="info">
                        <div class="lab">性别</div>
                        <div class="value">{{vodInfo.athGender}}</div>
                    </div>
                </div> 
                <div class="r">
                    <i class="infoIcon fa fa-file-picture-o"></i>
                    <div class="info">
                        <div class="lab">马匹</div>
                        <div class="value">{{vodInfo.horseName}}</div>
                    </div>
                </div>  
            </div>

            <!--
            <div class="empty">
                <img :src="sys.img404" alt="">
                <div class="emptyText">暂无直播信息</div>
            </div>
            -->
        </div>
    </div>
</template>

<script>
    import Hls from 'hls.js'; 
    export default {
        mounted(){
            var me=this;
            try {
                console.log('eqvideo');
                me.$nextTick().then(_=>{
                    me.getVodInfo();
                })
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return {                
                sys:{
                    gameCode:"20240105001",
                    logoImg:require('./imgs/eqlogo.png'),
                    img404:require('./imgs/404.png'),    
                    gameInfoUrl:"http://hhucjsoss.oss-cn-beijing.aliyuncs.com/eqvideo/20240105001/gameInfo.txt"                
                }, 
                vodInfo:{
                    gameCode:"20240105001",
                    gameName:"测试赛3",
                    address:"中国.地点1", 
                } 
            }
        },
        methods:{
            playVodVideo(){
                var me=this;
                try {  
                    var liveUrl = me.vodInfo.vodUrl; 
                    var hls = new Hls();
                    hls.loadSource(liveUrl);
                    hls.attachMedia(this.$refs.videoRef);
                    hls.on(Hls.Events.MANIFEST_PARSED,function() {
                        this.$refs.videoRef.play();
                    });
                } catch (error) {
                    console.log(error)
                }
            },
            getVodInfo(){
                var me=this;
                try {  
                    me.$eq.getVodInfo(me.$route.query.resId).then(info=>{
                        console.log(info);
                        me.vodInfo = info;
                        me.playVodVideo();
                    }) 
                } catch (error) {
                    console.log(error)
                }
            }
        }
    }
</script>

<style lang="less" scoped>
    .header{
        background-color: #0077fe;
        padding: 5px;
        color: #fff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        .btnIcon{
            height: 40px;
            line-height: 40px;
            width: 40px;
            text-align: center;
        }
        .title{
            padding: 0 15px;
        }
    }
    .content{
        padding: 0 20px;
        .empty{
            margin-bottom: 15px;
            img{
                width: 100%;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .emptyText{
                color: #777;
            }
        }
    }
    .gameInfo{
        background-color: #fff;
        border-radius: 7px;
        box-shadow: 0 0 10px 0 #e1e1e1;
        padding: 10px 0;
        margin-bottom: 20px;
        font-size:0.9em;

        .r{
            display: flex;
            align-items: center;
            .infoIcon{
                width: 40px;
                line-height: 40px;
                height: 40px;
                text-align: center;
            }
            .info{
                flex: 1;
                min-height: 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #eee;
                .lab{
                    color: #666;
                }
                .value{
                    padding-right: 10px;
                }
            }
            .liveVideo{
                width: 100%;
                padding: 0 15px;
                video{
                    width: 100%;
                    object-fit: cover;
                    background-color: #222;
                }
            }
        }
        .r:last-child  .info{ 
            border: 0;
        }
    }

</style>