<template>
<div class="admin">
    <div class="header">
        <div class="toolbar">
            <div class="logo">
                <img :src="sys.logoImg" class="logoImg" alt="">
            </div>

            <div class="games">
                <div class="gameName"> 
                    <el-select size="small" v-model="games.gameCode" placeholder="请选择赛事 ">
                        <el-option
                            v-for="item in games.items"
                            :key="item.gameCode"
                            :label="item.gameName"
                            :value="item.gameCode">
                        </el-option>
                    </el-select>
                </div>
                <div class="addBtn">
                    <el-button type="primary" size="small"><i class="fa fa-plug"></i> 新建赛事</el-button>
                </div>
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
        <div class="content">
            <div class="infos">
                <el-tabs >
                    <el-tab-pane>
                        <span slot="label"><i class="fa fa-trophy"></i> 赛事信息</span>
                        <GameInfo v-bind:gameInfo="gameInfo"></GameInfo>
                    </el-tab-pane>
                    <el-tab-pane>
                        <span slot="label"><i class="fa fa-cubes"></i> 考选手</span>
                        <Results v-bind:resInfo="resInfo"></Results>
                    </el-tab-pane> 
                </el-tabs>
            </div>
        </div>
    </div>
</div>
</template>

<script>
    import GameInfo from './gameInfo.vue'
    import Results from './result.vue'
    export default {
        components:{
            GameInfo,
            Results
        },
        data(){
            return{
                sys:{
                    title:"马术考-视频控制" ,
                    logoImg: require("./imgs/eqlogo.png"),
                    sysLocalKey:"eqAdmin.localKey",
                    videoWidth:100,
                },
                userInfo:{
                    userCode:"admin",
                    userName:"张三丰"
                },
                gameInfo:{},
                resInfo:{
                    filters:{
                        events:{
                            items:[
                                {eventCode:"E1", eventName:"盛装舞步"} ,
                                {eventCode:"E2", eventName:"场地障碍"} ,
                            ],
                            index:0
                        },
                        phases:{
                            items:[
                                {phaseCode:"J1", phaseName:"初一"} ,
                                {phaseCode:"J2", phaseName:"初二"} ,
                                {phaseCode:"J3", phaseName:"初三"} ,
                                {phaseCode:"S1", phaseName:"中一"} ,
                                {phaseCode:"S2", phaseName:"中二"} ,
                                {phaseCode:"S3", phaseName:"中三"} ,
                            ],
                            index:0
                        },
                    },
                    search:{
                        searchText:""
                    }
                },
                games:{
                    items:[
                        {gameCode:"20240105001",gameName:"测试赛1"},
                        {gameCode:"20240105002",gameName:"测试赛2"},
                        {gameCode:"20240105003",gameName:"测试赛3"},
                        {gameCode:"20240105004",gameName:"测试赛4"},
                        {gameCode:"20240105005",gameName:"测试赛5"},
                    ],
                    gameCode:""
                }
            }
        }
    }
</script>

<style lang="less" scoped> 
.header{
    position: fixed;
    width: 100%;
    box-shadow: 0 0 10px 0 #999;
    padding: 5px 50px;
    .toolbar{
        display: flex;
        align-items: center;
        .logo{
            img{
                height: 40px;
            }
        }
        .user{
            display: flex;
                align-items: center;
            .item{
                display: flex;
                align-items: center;
                margin-left: 10px;
                i{
                    padding-right: 5px;
                }
            }
        }
        .games{
            flex: 1;
            display: flex;
            padding: 0 15px;
            text-align: end;
            .addBtn{
                padding-left: 10px;
            }
        }
    }
} 
.body{
    padding: 20px 50px;
    padding-top: 70px;
    .content{ 
        padding-right: 15px;
        .infos{
            background-color: #fff;
            padding: 15px;
        }
    }
}
</style>