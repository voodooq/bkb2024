<template> 
    <div class="game">
        <div class="filterBar">
            <div class="filter">
                <ul class="lstFilter">
                    <li
                        v-for="(item,index) in filter.items" :key="index"
                        :class="index==filter.index?'active':''"
                        @click="onPickStatus(index)"
                    >
                        {{ item.lab }}
                    </li>
                </ul>
            </div> 
        </div> 
        <div class="sec" style="padding-top:70px"> 
            <div class="sec-body">
                <div class="productList">
                    <div
                        class="product"
                        v-for = "(item , index) in games" :key="index"
                        @click="gotoGameVideos(item.gameCode)"
                    >
                        <div class="iconImg">
                            <img src='https://ww1.sinaimg.cn/mw690/0089mqAkly1hqlirs694kj35oq3sknpm.jpg' alt="">
                            <div :class="'flatLabel status'+item.gameStatus">{{ item.gameStatusText }}</div>
                        </div>
                        <div class="productInfo">
                            <div class="data">
                                <div class="productTitle">
                                    {{ item.gameName }}
                                </div>
                                <div class="desc">
                                    {{ item.gameDesc }}
                                </div>
                            </div>
                            <div class="info">
                                <div class="item">
                                    <i class="fa fa-calendar"></i> {{ item.openDate }}
                                </div>
                                <div class="item">
                                    <i class="fa fa-map-marker"></i> {{ item.address }}
                                </div>
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
                console.log('game', this)
                me.refreshGames();
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{ 
                filter:{
                    items:[
                    {status:"9" , lab:"所有赛事"},
                    {status:"0" , lab:"未开始"},
                    {status:"1" , lab:"进行中"},
                    {status:"2" , lab:"已结束"},
                    ],
                    index:0
                },
                games:[]
            }
        },
        methods:{
            onPickStatus(index){
                var me = this;
                try {
                    me.filter.index = index;
                    me.refreshGames();
                } catch (error) {
                    console.log(error)
                }
            },
            refreshGames(){
                var me = this;
                try {
                    var status = me.filter.items[me.filter.index].status;
                    me.$eq.getGamesByStatus(status).then(_res=>{
                        me.games = _res;
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

    .filterBar{
        background-color: #f2f3f9;
        position: fixed;
        top: 0;
        width: 100%;
        padding: 10px 30px; 
        z-index: 999;
    }

    .flatLabel.status0{
        background-color: #0077fe;
        color: #fff;
    }
    .flatLabel.status1{
        background-color: #089213;
        color: #fff;
    }
    .flatLabel.status2{
        background-color: #fe008c;
        color: #fff;
    }
</style>