<template> 
    <div class="home">

        <div class="sec"> 
            <div class="sec-body">
                <div class="block coursel"> 
                    <el-carousel height="250px">
                        <el-carousel-item v-for="item in carouselImgs" :key="item">
                            <img :src="item" class="courseImg" alt="">
                        </el-carousel-item>
                    </el-carousel>
                </div>
            </div>
        </div>
        <div class="sec">
            <div class="sec-header">
                <div class="sec-title">
                    近期赛事
                </div>
            </div>
            <div class="sec-body">
                <div class="games">
                    <div
                        class="gameItem"
                        v-for = "(item , index) in homeGames" :key="index"
                        @click="gotoGameVideos(item.gameCode)"
                    >
                        <div class="thumb">
                            <div :class="'status status'+item.gameStatus">{{ item.gameStatusText }}</div>
                        </div>
                        <div class="data">
                            <div class="title">{{ item.gameName }}</div>
                            <div class="info">
                                <div class="item"><i class="fa fa-calendar"></i> {{ item.openDate }}</div>
                                <div class="item"><i class="fa fa-map-marker"></i> {{ item.address }}</div>
                                <div class="item"><i class="fa fa-flag"></i> {{ item.gameStatusText }}</div>
                            </div>
                        </div>
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
                me.refreshHomeGames();
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{
                carouselImgs:[
                    'https://img.zcool.cn/community/0169d55ac42e93a8012062e30f5e71.jpg?x-oss-process=image/auto-orient,1/resize,m_lfit,w_1280,limit_1/sharpen,100',
                    'https://pic.52112.com/180713/JPG-180713_521/YEDIEAd51A_small.jpg',
                    'https://ww1.sinaimg.cn/mw690/0089mqAkly1hqlirs694kj35oq3sknpm.jpg',
                    'https://img2.baidu.com/it/u=3713634215,1684735084&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=333'
                ],
                homeGames:[]
            }
        },
        methods:{
            refreshHomeGames(){
                var me = this;
                try {
                    me.$eq.getHomeGames().then(_res=>{
                        me.homeGames = _res;
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            gotoGameVideos(gameCode){
                var me = this;
                try {
                    var url = "/gameVideos"
                    var ps ={
                        gameCode:gameCode
                    };
                    me.$router.push({
                        path:url ,
                        query: ps
                    })
                } catch (error) {
                    console.log(error)
                }
            },
        }
        
    }
</script>

<style lang="less" scoped>
    @import url('../assets/comm/comm.less');
    .coursel{
        img.courseImg{
            width: 100%;
            object-fit: cover;
        }
    }

    .games{
        padding: 15px;
        .gameItem{
            background-color: #fff;
            border-radius: 7px;
            box-shadow: 0 0 10px 0 #f0f0f0;
            margin-bottom:15px;
            .thumb{
                height: 180px;
                position: relative;
                background-image: url('https://ww1.sinaimg.cn/mw690/0089mqAkly1hqlirs694kj35oq3sknpm.jpg');
                border-radius: 7px 7px 0 0 ;
                .status {
                    position: absolute;
                    right:10px;
                    top:10px;
                    padding: 5px 10px;
                    border-radius: 5px;
                    color: #fff;
                }
                .status.status0{
                    background-color: #0077fe;
                }
                .status.status1{
                    background-color: #089213;
                }
                .status.status2{
                    background-color: #fe008c;
                }
            }
            .data{
                .title{
                    font-weight: bold;
                    text-align: left;
                    padding: 10px;
                    font-size: 1.1em;
                }
                .info{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 10px;
                    padding-top: 0;
                    color: #777;
                }
            }
        }
    }
</style>