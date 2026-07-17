<template>
    <div class="pg">
        <div class="pgHeaderFix">
            <i @click="$router.back()" class="btnBack fa fa-chevron-left"></i>
            <div class="title">{{ gameInfo.gameName }}</div>
            <div class="btns">
                <el-button @click="refresh" size="small" type="primary">
                    <i class="fa fa-refresh"></i> 刷新
                </el-button>
                <el-button @click="control" size="small" type="primary">
                    <i class="fa fa-flash"></i> 控制
                </el-button>
            </div>
        </div>

        <div class="pgBody">
            <div 
                class="liveVideos"
                v-if="liveVideos.length>0"
            >
                <div 
                    class="liveVideoItem"
                    v-for="(item,index)  in liveVideos" :key ="index"
                    @click="playVideo(item.resCode)"
                    >
                    <div class="videoThumb">
                        <div class="lab">直播</div>
                    </div>
                    <div class="videoInfo"> 
                        <div class="info">
                            <div class="item"><i class="fa fa-cogs"></i> {{ item.athName }}</div>
                            <div class="item"><i class="fa fa-tv"></i> {{ item.phaseName }}</div>
                            <div class="item"><i class="fa fa-cogs"></i> {{ item.eventName }}</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="videos">
                <div 
                    class="videoItem"
                    v-for="(item,index)  in videos" :key ="index"
                    @click="playVideo(item.resCode)"
                    >
                        <div class="thumb">
                            <div class="lab">回放</div>
                        </div>
                        <div class="title">{{ item.athName }}</div>
                        <div class="info">
                            <div class="item"><i class="fa fa-tv"></i> {{ item.phaseName }}</div>
                            <div class="item"><i class="fa fa-cogs"></i> {{ item.eventName }}</div>
                        </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        mounted(){
            var me = this;
            try { 
                me.gameCode = me.$route.query.gameCode;
                me.refresh ();
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{ 
                gameCode:"",
                gameInfo:{},
                events:{
                    items:[],
                    index:0
                },
                videos:[],
                liveVideos:[]
            }
        },
        methods:{  
            refresh (){
                var me = this;
                try { 
                    me.$eq.getGameVideos(me.gameCode).then(_res=>{
                        if( _res.success>0){
                            me.gameInfo = _res.gameInfo;
                            me.videos = _res.videos;
                            me.liveVideos = _res.videos.filter( v=>{
                                //return v.resStatus==1;
                                return v.resId%54==0;
                            })

                        }
                        console.log(_res, me.liveVideos)
                    })
                } catch (error) {
                    console.log(error)
                }
            } ,
            playVideo (videoCode){
                var me = this;
                try { 
                    var ps={
                        gameCode : me.gameCode ,
                        videoCode
                    }
                    var url = "/video" 
                    me.$router.push({
                        path:url ,
                        query: ps
                    }) ;
                } catch (error) {
                    console.log(error)
                }
            } ,
            control ( ){
                var me = this;
                try { 
                    me.$router.push({
                        path:"/control"
                    })
                } catch (error) {
                    console.log(error)
                }
            } 
        }
    }
</script>

<style lang="less" scoped>
    @import url("../assets/comm/comm.less");

    .pgHeaderFix{
        position: fixed;
        z-index: 99;
        width: 100%;
        top: 0;
        padding: 10px;
        background-color: #0077fe;
        color: #fff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        .btnBack{
            height: 40px;
            line-height: 40px;
            width:40px;
            text-align: center;
        }
    }
    .pgBody{
        padding: 15px;
        padding-top: 75px;
    }

    .liveVideos{ 
        .liveVideoItem{
            background-color: #fff;
            box-shadow: 0 0 10px 0 #f0f0f0;
            margin-bottom: 15px;
            border-radius: 10px;
            .videoThumb{
                height: 180px;
                background-image: url('https://ww1.sinaimg.cn/mw690/0089mqAkly1hqlirs694kj35oq3sknpm.jpg');
                background-size: cover;
                border-radius: 10px 10px 0 0 ;
                position: relative;
                .lab{
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background-color: #b6174c;
                    color: #fff;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
            }
            .info{
                padding: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
        }
    }

    .videos{
        display: grid;
        grid-template-columns: auto auto;
        gap: 15px; 
        .videoItem{
            background-color: #fff;
            margin-bottom: 15px;
            border-radius: 7px;
            .thumb{
                height: 120px;
                background-image: url('https://ww1.sinaimg.cn/mw690/0089mqAkly1hqlirs694kj35oq3sknpm.jpg');
                background-size: cover;
                border-radius: 10px 10px 0 0 ;
                position: relative;
                .lab{
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background-color: #0077fe;
                    color: #fff;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
            }
            .title{
                text-align: left;
                font-weight: bold;
                font-size:1.1em;
                padding: 5px;
            }
            .info{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 5px;
                color: #999;
            }
        }
    }
</style>