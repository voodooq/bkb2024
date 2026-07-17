<template>
    <div class="live">
        <div class="block coursel"> 
            <el-carousel height="250px">
                <el-carousel-item v-for="item in swiperImgs" :key="item">
                    <img :src="item" class="courseImg" alt="">
                </el-carousel-item>
            </el-carousel>
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
                        <div class="value">{{gameInfo.gameCode}}</div>
                    </div>
                </div>
                <div class="r">
                    <i class="infoIcon fa fa-institution"></i>
                    <div class="info">
                        <div class="lab">赛事名称</div>
                        <div class="value">{{gameInfo.gameName}}</div>
                    </div>
                </div>
                <div class="r">
                    <i class="infoIcon fa fa-flag-o"></i>
                    <div class="info">
                        <div class="lab">开始时间</div>
                        <div class="value">{{gameInfo.openDate}}</div>
                    </div>
                </div>
                <div class="r">
                    <i class="infoIcon fa fa-flag-checkered"></i>
                    <div class="info">
                        <div class="lab">结束时间</div>
                        <div class="value">{{gameInfo.closeDate}}</div>
                    </div>
                </div>
                <div class="r">
                    <i class="infoIcon fa fa-map-marker"></i>
                    <div class="info">
                        <div class="lab">地点</div>
                        <div class="value">{{gameInfo.address}}</div>
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
                    me.getGameInfo();
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
                swiperImgs:[
                    require('./imgs/swiper/1.jpg') ,
                    require('./imgs/swiper/2.jpg') ,
                    require('./imgs/swiper/3.jpg') ,
                ],
                gameInfo:{
                    gameCode:"20240105001",
                    gameName:"测试赛3",
                    address:"中国.地点1",
                    openDate:"2024-01-05",
                    closeDate:"2024-01-08"
                },
                events:[],
                phases:[],
                liveSrcUrl : ""
            }
        },
        methods:{
            playLiveVideo(){
                var me=this;
                try {  
                    var liveUrl = me.gameInfo.m3u8Url;
                    me.liveSrcUrl = liveUrl;
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
            getGameInfo(){
                var me=this;
                try {  
                    me.$eq.getGameInfo(me.sys.gameCode).then(info=>{
                        console.log(info);
                        me.gameInfo = info.gameInfo;
                        me.events = info.events;
                        me.phases = info.phases;

                        me.playLiveVideo();
                    })
                    /*
                    me.$eqVideo.getStatic(me.sys.gameInfoUrl).then(info=>{
                        if(info){
                            me.gameInfo = info.gameInfo[0];
                            me.events = info.events;
                            me.phases = info.phases;

                            var liveUrl = me.gameInfo.m3u8Url;
                            me.liveSrcUrl = liveUrl;
                            var hls = new Hls();
                            hls.loadSource(liveUrl);
                            hls.attachMedia(this.$refs.videoRef);
                            hls.on(Hls.Events.MANIFEST_PARSED,function() {
                                this.$refs.videoRef.play();
                            });
                        }
                    });
                */
                } catch (error) {
                    console.log(error)
                }
            }
        }
    }
</script>

<style lang="less" scoped>
    .coursel{
        margin-bottom: 20px;
        img.courseImg{
            width: 100%;
            object-fit: cover;
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