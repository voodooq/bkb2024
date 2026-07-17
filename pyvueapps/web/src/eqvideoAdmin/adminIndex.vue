<template>
    <div class="admin">
        <div class="header">
            <div class="toolbar">
                <div class="logo">
                    <img :src="sys.logoImg" alt="">
                    <div class="title">
                        {{sys.title}}
                    </div>
                </div>
                <div class="game">
                    {{gameInfo.gameName}}
                </div>
                <div class="user">
                    <div class="item">
                        <i class="fa fa-user-o"></i> {{userInfo.userName}}
                    </div>
                    <div class="item">
                        <i class="fa fa-power-off"></i> 退出系统
                    </div>
                </div>
            </div>
        </div>
        <div class="body">
            <router-view  class="mainPage"></router-view>
        </div>
        <div class="aside">
            <div class="menus">
                <div :class="$route.path=='/eqAdminIndex/game'?'navItem active':'navItem' " @click="onPickNav('game')" >
                    <i class="fa fa-server"></i> 赛事
                </div>
                <div :class="$route.path=='/eqAdminIndex/result'?'navItem active':'navItem' " @click="onPickNav('result')" >
                    <i class="fa fa-flag-checkered"></i> 选手
                </div>
                <!--
                <div :class="$route.path=='/eqAdminIndex/video'?'navItem active':'navItem' " @click="onPickNav('video')" >
                    <i class="fa fa-photo"></i> 视频
                </div>
                -->
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        mounted(){
            var me = this;
            try {
                var sessionData = me.$eq.getAdminSessionData();
                if( sessionData.success>0){
                    me.gameInfo = sessionData.gameInfo;
                    me.userInfo = sessionData.userInfo;
                }
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return {
                
                sys:{
                    title:"视频考级系统",
                    logoImg:require("./imgs/eqlogo.png"),
                    copyRight:"中国马术协会"
                },
                gameInfo:{
                    gameId :0 ,
                    gameCode:"",
                    gameName:"",
                    gameDesc:"",
                    address:"",
                    openDate:"",
                    endDate:""
                },
                userInfo:{
                    userCode:"admin",
                    userName:"系统管理员",
                    pwd:"123456",
                    gameCode:"20240105001"
                }
            }
        },
        methods:{
            onPickNav(key){
            var me = this;
                try {
                    var url = "/eqAdminIndex/"+key;
                    me.$router.push({
                        path: url
                    })
                } catch (error) {
                    console.log(error)
                }
            }
        }
        
    }
</script>

<style lang="less" scoped>
    .admin{
        .header{
            position: fixed;
            width: 100%;
            padding: 10px 50px;
            top: 0;
            z-index: 999;
            box-shadow: 0 0 10px 0 #999 ;
            background-color: #f2f3f9;
            .toolbar{
                display: flex;
                justify-content: space-between;
                align-items: center;
                .logo{
                    display: flex;
                    align-items: center;
                    img{
                        height: 50px;
                    }
                    .title{
                        padding: 0 15px;
                        font-size: 1.2em;
                        font-weight: bold;
                    }
                }
                .game{
                    padding: 10px 15px;
                    background-color: #0077fe;
                    border-radius: 25px;
                    color: #fff;
                }
                .user{
                    display: flex;
                    align-items: center;
                    .item{
                        margin-left: 10px;
                        display: flex;
                        align-items: center;
                        i{
                            padding-right: 5px;
                        }
                    }
                }
            }
        }
        .aside{
            position: fixed;
            left: 0;
            top: 0;
            height: 100%;
            width: 160px;
            padding: 20px;
            padding-top: 90px;
            padding-left: 50px;
            .menus{
                .navItem{
                    text-align: left; 
                    color: #777;
                    padding: 10px;
                    margin-bottom: 10px;
                }
                .navItem:hover{
                    cursor: pointer;
                    color: #222;
                }
                .navItem.active{
                    color: #0077fe; 
                }
            }
        }
        .body{
            padding-left: 160px;
            padding-top: 85px;
            padding-right: 50px;
            padding-bottom: 15px;
        }
    }


</style>