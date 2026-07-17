<template>
    <div class="screen"> 
        <div class="video" id="J_prismPlayer" > 
        </div>
        <div class="logo">
            <img :src="imgs.logo" alt="">
        </div>
        <div class="match">
            <div class="game">{{info.gameName}}</div>
            <div class="info">
                <div class="event">{{info.eventName}}</div>
                <div class="phase">{{info.phaseName}}</div>
            </div>
        </div>
        <div class="ath" v-if="info.isLiving>0">
            <div class="title">
                <div class="athName">{{info.athName}}</div>
                <div class="horse">
                    <img :src="imgs.horse" alt="">
                    <div class="horseName">{{info.horseName}}</div>
                </div>
            </div>
            <div class="orgName">{{info.orgName}}</div>
        </div>

    </div>
</template>

<script>
    
    import flvjs from 'flv.js' 
    export default {
        mounted(){
            var me = this;
            try {
                me.$nextTick().then(_=>{
                    me.refresh();
                });
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{
                info:{},
                imgs:{
                    logo: require('./imgs/eqlogo.png'),
                    horse:require('./imgs/iconhorse.png')
                },
                player : null
            }
        },
        methods:{
            refresh(){
                var me = this;
                try {
                    var updateData = ()=>{
                        me.$eq.getLiveVideoInfo().then(res=>{
                            console.log(res)
                            me.info = res;
                            if ( me.player==null){
                                me.playVideo();
                            }
                            window.setTimeout(()=>{
                                updateData();
                            }, 5*1000)
                        })
                    }
                    updateData();
                } catch (error) {
                    console.log(error)
                }
            },
            playVideo_flv(){
                var me = this;
                try {
                    if (flvjs.isSupported()) {
                        // 准备监控设备流地址
                        // 创建一个flvjs实例
                        // 下面的ws://localhost:8888换成你搭建的websocket服务地址，后面加上设备流地址
                        me.player = flvjs.createPlayer({
                            type: 'flv',
                            isLive: true,
                            url: url
                        })
                        
                        me.player.on('error', (e) => {
                            console.log(e)
                        })
                        
                        // 将实例挂载到video元素上面
                        me.player.attachMediaElement(this.$refs.player)
                        
                        try {
                            // 开始运行加载 只要流地址正常 就可以在h5页面中播放出画面了
                            this.player.load()
                            this.player.play()
                        } catch (error) {
                            console.log(error)
                        }  
                    } 
                } catch (error) {
                    console.log(error)
                }
            },
            playVideo(){
                var me = this;
                try {
                    console.log(me.info)
                    var url = me.info.flvUrl;
                    var player = new Aliplayer({
                        id: 'J_prismPlayer',
                        source: url, // 播放地址，可以是第三方直播地址，或阿里云直播服务中的拉流地址。
                        isLive: true, // 是否为直播播放。
                        width: "100%",
                        height: "100%",
                    },function(player){
                        console.log('The player is created.')
                        me.player = player
                    });
                } catch (error) {
                    console.log(error)
                }
            }
        }
        
    }
</script>

<style lang="less" scoped>
    .screen{
        position: relative;
        width: 100%;
        height: 100%;
        background-color: #111;
        color: #fff;

        .video{
            position: relative;
            width: 100%;
            height: 100%;  
            video{
                position: absolute;
                width: 100%;
                height: 100%;
                object-fit: cover;
                left: 0;
                top: 0;
            }          
        }

        .logo{
            position: fixed;
            z-index: 99;
            left: 30px;
            top: 30px;
            background-color: #fff;
            padding-right: 20px;
            border-radius: 30px;
            img{
                height: 60px;
            }
        }

        .match{
            position: fixed;
            z-index: 99;
            right: 30px;
            top: 30px;
            background-color: rgba(10, 10, 10, 0.5);
            font-size: 1.2em;
            padding: 15px;
            .game{
                font-weight: bold;
            }
            .info{
                display: flex;
                justify-content: space-between;
            }
        }

        .ath{
            position: fixed;
            z-index: 99;
            left: 30px;
            bottom: 30px;
            background-color: rgba(10, 10, 10, 0.5);
            font-size: 1.2em;
            padding: 15px;
            .orgName{
                text-align: left;
                
            }
            .title{
                font-weight: bold;
                display: flex;
                justify-content: space-between;
                .athName{
                    padding-right: 30px;
                }
                .horse{
                    display: flex;
                    align-items: center;
                    img{
                        height: 32px;
                    }
                    .horseName{
                        font-size: 12pt;
                        padding-left: 5px;
                    }
                }
            }
        }
    }
</style>