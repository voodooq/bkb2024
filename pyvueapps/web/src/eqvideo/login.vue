<template>
    <div class="moapp full">
        <div class="login full">
            <div class="welcome">
                <img class="imgLogo" :src="sysInfo.logoImg" alt="">
                <div class="title">欢迎您</div>
            </div>
            <div class="sysTitle">
                {{sysInfo.title}}
            </div>
            <div class="loginForm shadowBox">
                <div class="cateFilter" >
                    <div :class="loginData.cate=='official'?'cateItem active':'cateItem'" @click="loginData.cate='official';">官员登录</div>
                    <div :class="loginData.cate=='admin'?'cateItem active':'cateItem'" @click="loginData.cate='admin';">工程师登录</div>
                </div>
                <div class="userData">
                    <div class="r" v-if="loginData.cate=='admin'">
                        <el-input v-model="loginData.gameCode" placeholder="请输入赛事代码" ></el-input>
                        <i class="fa fa-newspaper-o"></i>
                    </div>
                    <div class="r">
                        <el-input v-model="loginData.userCode" placeholder="请输入用户名" ></el-input>
                        <i class="fa fa-user-o"></i>
                    </div>
                    <div class="r">
                        <el-input v-model="loginData.pwd" type="password" placeholder="请输入密码" ></el-input>
                        <i class="fa fa-key"></i>
                    </div>
                    <div class="btnPost">
                        <el-button type="text">注册账号</el-button>
                        <el-button @click="login" type="primary"><i class="fa fa-lock"></i> 登录系统</el-button>
                    </div>
                </div>
            </div>
            <div class="copyright bg3">
                {{sysInfo.copyright}}
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data(){
            return{
                sysInfo:{
                    title:"马术考级视频系统 2024",
                    copyright:"中国马术协会",
                    logoImg: require("./imgs/eqlogo.png")
                }
                ,loginData:{
                    cate:'official',       
                    userCode:"",
                    pwd:"",
                    gameCode:""             
                }
            }
        },
        methods:{
            login(){
                var me = this;
                try {
                    console.log('l')
                    debugger
                    if( me.loginData.cate == 'official'){
                        me.$eq.checkLogin( me.loginData.cate , me.loginData.userCode , me.loginData.pwd).then(_res=>{
                            if( _res){
                                me.$router.push({
                                    path:"/index/home"
                                })
                            }
                            else{
                                me.$message.error('用户名或密码错误！')
                            }
                        })
                    }
                    else if( me.loginData.cate == 'admin'){
                        
                        me.$eq.checkLoginAdmin( me.loginData.userCode , me.loginData.pwd, me.loginData.gameCode).then(_res=>{
                            if( _res){
                                me.$router.push({
                                    path:"/index/home"
                                })
                            }
                            else{
                                me.$message.error('用户名或密码错误！')
                            }
                        })

                    }
                } catch (error) {
                    console.log(error)
                }
            }
        }
        
    }
</script>

<style lang="less" scoped>
    @import url('../assets/comm/comm.less');

    .login{
        padding: 20px;
        position: relative;
        .welcome{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;

            .imgLogo{
                height: 60px;
            }
            .title{
                font-size: 1.2em;
                font-weight: bold;
            }
        }
        .sysTitle{
            font-weight: bold;
            font-size: 1.2em;
            padding-left: 20px;
            border-left: 3px solid #32a666;
            text-align: left;
            margin-bottom: 30px;
        }
        .loginForm{
            background-color: #fff;
            border-radius: 7px; 
            padding-top: 20px;
            .cateFilter{
                display: flex;
                justify-content: space-between;
                align-items: center;
                .cateItem{
                    flex: 1;
                    text-align: center;
                    margin-bottom: 20px;
                    height: 50px;
                    line-height: 50px;
                    text-align: center;
                    border-bottom: 1px solid #eee;
                }
                .cateItem.active{
                    border-bottom:1px solid #0077fe;
                    font-weight: bold;
                    color: #0077fe;
                }
            }
            .userData{
                padding: 0 20px;
                .r{
                    position: relative;
                    margin-bottom: 15px;
                    i{
                        position: absolute;
                        right: 15px;
                        height: 40px;
                        line-height: 40px;
                    }
                }
                .btnPost{
                    padding: 15px 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
            }
        }
        .copyright{
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translate(-50%);
        }
    }
</style>