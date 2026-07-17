<template>
    <div class="login">
        <div class="loginPage">

            <div class="logo">
                <img :src="sys.logoImg" alt="">
                <div class="title">{{sys.title}}</div>
            </div>
            <div class="formEdit">
                <div class="r">
                    <div class="lab">赛事代码</div>
                    <div class="edit">
                        <el-input style="width:100%" v-model="login.gameCode" placeholder="请输入赛事代码"></el-input>
                    </div>
                    <i class="fa fa-server ic"></i>
                </div>
                <div class="r">
                    <div class="lab">用户账号</div>
                    <div class="edit">
                        <el-input style="width:100%" v-model="login.userCode" placeholder="请输入用户账号"></el-input>
                    </div>
                    <i class="fa fa-user-o ic"></i>
                </div>
                <div class="r">
                    <div class="lab">登录密码</div>
                    <div class="edit">
                        <el-input style="width:100%" type="password" v-model="login.pwd" placeholder="请输入登录密码"></el-input>
                    </div>
                    <i class="fa fa-lock ic"></i>
                </div>
                <div class="postBtn">
                    <el-button type="text"><i class="fa fa-"></i> 忘记密码</el-button>
                    <el-button @click="acLogin" type="primary"><i class="fa fa-key"></i> 登录系统</el-button>
                </div>
            </div>
            <div class="copyRight">
                {{sys.copyRight}}
            </div>
        </div>

    </div>
</template>

<script>
    export default {
        data(){
            return{
                sys:{
                    title:"视频考级系统",
                    logoImg:require("./imgs/eqlogo.png"),
                    copyRight:"中国马术协会" 
                },
                login:{
                    userCode:"admin",
                    pwd:"123456",
                    gameCode:"20240105001"
                } 
            }
        },
        methods:{
            acLogin(){
                var me = this;
                try {
                    me.$eq.checkLogin(
                        "admin",
                        me.login.userCode ,
                        me.login.pwd
                    ).then(_res=>{
                        if( _res){
                            me.$eq.getGameInfo(me.login.gameCode).then(_game=>{
                                if( _game && _game.success>0){
                                    _game.userInfo = me.$eq.datas.userInfo;
                                    me.$eq.setAdminSessionData( _game )                                  
                                    me.$router.push({
                                        path:"/eqAdminIndex"
                                    })
                                }
                                else{
                                    me.$message.error('赛事代码错误！')
                                }
                            })
                        }
                        else{
                            me.$message.error('用户名或密码错误！')
                        }
                        console.log(_res)
                    })
                } catch (error) {
                    console.log(error);
                }
            }
        }
    }
</script>

<style lang="less" scoped>
    .login{
        width: 400px;
        position: fixed;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);

        .loginPage{
            .logo{
                display: flex;
                align-items: center;
                justify-content: space-evenly;
                margin-bottom: 15px;
                img{
                    height: 50px;
                }
                .title{
                    font-size: 1.2em;
                    font-weight: bold;
                }
            }
            .formEdit{
                padding: 15px;
                background-color: #fff;
                box-shadow: 0 0 10px 0 #f0f0f0;
                margin-bottom: 60px;
                .r{
                    position: relative;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                    .lab{
                        width: 90px;
                        text-align: right;
                        padding-right: 10px;
                    }
                    .edit{
                        flex: 1;

                    }
                    i.ic{
                        position: absolute;
                        right: 15px;
                        height: 40px;
                        line-height: 40px;
                    }
                }
                .postBtn{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
            }
            .copyRight{
                font-size: 0.9em;
                color: #999; 
            }
        }
    }
</style>