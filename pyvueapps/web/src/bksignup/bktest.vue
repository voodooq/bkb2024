<template>
    <div class="bk">
        <div class="header">
            <div class="toolbar">
                <div class="title">BkSignup api Test</div>
            </div>
        </div>
        <div class="body">
            <ul class="lstAcs">
                <li @click="bk.exportGameData">
                    <div class="ac">
                        <div class="title">exportGameData</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li>
                <li @click="acGetGameData">
                    <div class="ac">
                        <div class="title">getGameData</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li> 
                <li @click="acGetUserData">
                    <div class="ac">
                        <div class="title">getUserData</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li> 
                <li @click="acGetSessionValid">
                    <div class="ac">
                        <div class="title">session_valid</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li>
                <li @click="acCheckLogin">
                    <div class="ac">
                        <div class="title">session_checkLogin</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li>
                <li @click="acTeamCreate">
                    <div class="ac">
                        <div class="title">team_create</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li>
                <li @click="acTeamSetSignupStatus">
                    <div class="ac">
                        <div class="title">team_setSignupStatus</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li>
                <li @click="acMemberCreate">
                    <div class="ac">
                        <div class="title">memmber_create</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li>
                <li @click="acMemberEdit">
                    <div class="ac">
                        <div class="title">memmber_edit</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li>
                <li @click="acMemberUpdateExInfo">
                    <div class="ac">
                        <div class="title">memmber_updateExInfo</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li>
                <li @click="acMemberRemove">
                    <div class="ac">
                        <div class="title">memmber_remove</div>
                        <i class="fa fa-chevron-right acIcon"></i>
                    </div>
                </li> 
                <li>
                    <div class="upload">
                        <div class="inputFile">
                            <input type="file" ref="inputUploadFile" id="inputUpload">
                        </div>
                        <div class="img">
                            <img :src="imgUrl" alt="">
                        </div>
                        <el-button @click="acUploadImg">upload image</el-button>
                    </div>
                </li>
            </ul> 
        </div>
    </div>
</template>

<script>
    
    var bkapi = require('./bkapi')
    console.log(bkapi.bkapi)
    import axios from "axios"; 
    const md5 = require('./md5');
    console.log('md5', md5)
    const bkAapi = {
        config:{
            apiUrl: "/yyapi",
            ossCode: "hhuoss",
            rootUrl:"https://hhucjsoss.oss-cn-beijing.aliyuncs.com/bksignup2024/BK202401BJ",
            sessionKey:"sessionKey.bkSignup2024",
            bucket:"hhucjsoss"
        },
        session:{
        },
        sts:{
            updateTime :0,
            duration : 20 * 60, 
            enable: 0 
        },
        gameData:{ 
        },
        callApi(action, params) {
            var me = this;
            var res = {
                status: 0
            };
            return new Promise((su, faild) => {
                try {
                    var postData = {
                        action: action,
                        params: params,
                        result: {}
                    }
                    axios.post(me.config.apiUrl, postData).then(_res => {
                        su(_res.data)
                    })
                } catch (error) {
                    console.log(error);
                    su(res);
                }
            })
        },
        getSts(roleSessionName) {
            var me = this;
            return new Promise((su, faild) => {
                try {
                    me.sts.enable = 0;
                    var nowTm = ( new Date()).getTime()
                    var ststEnable = me.sts &&                         
                        me.sts.updateTime && 
                        me.sts.updateTime > 0  && 
                        nowTm - me.sts.updateTime < 1000 * me.sts.duration;
                    if (ststEnable){
                        me.sts.enable = 1 
                        su(me.sts)
                    }
                    else{
                        me.sts = {
                            updateTime :0,
                            duration : 20 * 60, 
                            stsInfo : {}
                        };
                        me.sts = {
                            updateTime :0,
                            duration : 20 * 60, 
                        };
                        var action = 'oss/bucket/stsInfo';
                        var params = {
                            ossCode: me.config.ossCode,
                            roleSessionName: roleSessionName,
                            duration: me.sts.duration
                        };
                        me.callApi(action, params).then(_res => {
                            console.log(_res)
                            if( _res &&  _res.status && _res.status==1){
                                me.sts.stsInfo = _res.stsInfo;
                                me.sts.updateTime = nowTm;
                                me.sts.enable = 1;
                            }
                            su(me.sts);
                        })
                    }

                } catch (error) {
                    console.log(error);
                    su(me.sts);
                }
            })
        },
        uploadFile( roleSessionName , file ,  targetFn) {
            var me = this;
            var res = {
                status  : 0 ,
                url:""
            };
            return new Promise((su, faild) => {
                try {
                    me.getSts(roleSessionName).then(_=>{
                        var flag  = me.sts && me.sts.enable && me.sts.enable==1;
                        if ( flag ){
                            var ak = me.sts.stsInfo.Credentials.AccessKeyId;
                            var sk = me.sts.stsInfo.Credentials.AccessKeySecret;
                            var token = me.sts.stsInfo.Credentials.SecurityToken;
                            var bucket = me.config.bucket;

                            var client = new OSS({
                                // yourRegion填写Bucket所在地域。以华东1（杭州）为例，yourRegion填写为oss-cn-hangzhou。
                                region: "oss-cn-beijing",
                                // 从STS服务获取的临时访问密钥（AccessKey ID和AccessKey Secret）。
                                accessKeyId: ak,
                                accessKeySecret: sk,
                                // 从STS服务获取的安全令牌（SecurityToken）。
                                stsToken: token,
                                // 填写Bucket名称。
                                bucket: bucket,
                            }); 
                            client.put(targetFn, file).then(r => {
                                console.log(r);
                                if( r && r.url && r.url.length>0){
                                    res.status = 1 ;
                                    res.url = r.url;
                                }
                                su(res)
                            }).catch(e => {
                                console.log(e)
                                su(res)
                            }) 
                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res);
                }
            })
        },

        getStatic(dataPath) {
            var me = this;
            var res = null;
            return new Promise((su, fa) => {
                try {
                    var url = me.config.rootUrl+"/"+dataPath+'.txt?t='+(new Date()).getTime();
                    console.log(url)
                    axios.get(url).then(res => {
                        if (res && res.data) {
                            res = res.data;
                        }
                        su(res)
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        },
        exportGameData(){
            var me = bkAapi;
            return new Promise((su,fa)=>{
                try {
                    var ac = 'bksignup/exportGameData'
                    var ps = {}
                    me.callApi(ac , ps).then(res=>{
                        console.log(  res);
                        return me.getGameData();
                    }).then(_=>{
                        su();
                    })
                } catch (error) {
                    console.log(error);
                    su()
                }
            })
        },
        getGameData(){
            var me = bkAapi;
            return new Promise((su,fa)=>{
                try {
                    var dataPath = 'gameInfo';
                    me.getStatic(dataPath).then(_res=>{
                        me.gameData = _res;
                        su();
                    })
                } catch (error) {
                    console.log(error);
                    su()
                }
            })
        },
        getSession(){
            var me = bkAapi;
            return new Promise((su,fa)=>{
                try {
                    var hasSession =()=>{
                        return me.session && me.session.sessionId
                    } 
                    if( hasSession() ){
                        su()
                    }
                    else{
                        var content = window.sessionStorage.getItem(me.config.sessionKey);
                        try{
                            var session = JSON.parse( content)
                            if( session && session.sessionId){
                                me.session = session;
                            }
                        }
                        catch(er){
                            console.log(er)
                        }
                    }
                    if (hasSession()){
                        su();
                    }
                    else{
                        var apiPath = 'bksignup/sessionCreate';
                        me.callApi(apiPath , {}).then(_res=>{
                            console.log(_res)
                            if(_res && _res.status==1){
                                me.session = _res.res;
                                window.sessionStorage.setItem(me.config.sessionKey , JSON.stringify(me.session))
                            }
                            else{
                                me.session={};
                            }
                            su()
                        })
                    }
                } catch (error) {
                    console.log(error);
                    su()
                }
            })
        },
        updateUserData( forceUpdate = false ){
            var me = bkAapi;
            var res = {
                status:0 
            }
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var flag = me.isLogin();
                        if( flag){ 
                            var onUpdate =()=>{
                                var dataPath = 'users/'+ me.session.tel;
                                me.getStatic(dataPath).then(_res=>{
                                    console.log(_res)
                                    try{
                                        res.status = 1 ;
                                        _res.teams.forEach( t=>{
                                            t.members = _res.members.filter(m=>{
                                                return m.teamCode == t.teamKey;
                                            })
                                        })
                                        res.userDatas = _res.teams;

                                    }
                                    catch(ee){
                                        console.log(ee)
                                    }
                                    su(res);
                                })
                            }
                            if (forceUpdate){
                                var apiPath = "bksignup/sessionExecuteUserData";
                                var ps={ 
                                    tel: me.session.tel 
                                };
                                me.callApi( apiPath , ps).then (_res=>{
                                    console.log(_res);
                                    if(_res && _res.status==1){
                                        onUpdate();
                                    }
                                    else{
                                        su(_res)
                                    }
                                })
                            }
                            else{
                                onUpdate();
                            }

                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        },
        uploadLogoImg( file , targetFn ){
            var me = bkAapi;
            var res = {
                status:0 
            }
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var flag = me.isLogin();
                        if( flag){ 
                            me.uploadFile( me.session.sessionId , file , targetFn).then(_res=>{
                                su(_res)
                            })
                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        },
        //获取验证码
        requestSessionValid(tel){
            var me = bkAapi;
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var apiPath = "bksignup/sessionValid"
                        var ps ={
                            sessionId: me.session.sessionId ,
                            tel: tel
                        };
                        me.callApi(apiPath , ps).then (_res=>{
                            console.log(_res);
                            if( _res.status == 1){
                                me.session = _res.res;
                                me.session.loginStatus = 0 ;
                                window.sessionStorage.setItem(me.config.sessionKey , JSON.stringify(me.session))
                            }
                            su();
                        })
                    })
                } catch (error) {
                    console.log(error);
                    su()
                }
            })
        },
        checkLogin(validCode){
            var me = bkAapi;
            var res = 0
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var flag = me.session && me.session.sessionId && 
                            me.session.tel && me.session.tel.length>0;
                        if( flag){
                            var sec = md5.hex_md5([me.session.sessionId , me.session.tel , validCode].join('.'));
                            if (sec == me.session.sec){
                                var apiPath = "bksignup/sessionCheckLogin";
                                var ps={
                                    sessionId: me.session.sessionId ,
                                    tel: me.session.tel ,
                                    validCode : validCode
                                };
                                me.callApi( apiPath , ps).then (_res=>{
                                    console.log(_res);
                                    if( _res && _res.status==1){
                                        me.session.loginStatus = 1;
                                        window.sessionStorage.setItem(me.config.sessionKey , JSON.stringify(me.session))
                                        res = 1 ;
                                    }
                                    su(res)
                                })
                            }
                            else{
                                su(res)
                            }
                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        },
        isLogin(){
            var me = this;
            var res = false;
            try {
                res = me.session && me.session.loginStatus>0;
            } catch (error) {
                console.log(error)
            }
            return res;
        },
        teamCreate(teamName , eventCode , areaCode , phaseCode , logoImg){
            var me = bkAapi;
            var res = {
                status:0 ,
                team:{}
            }
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var flag = me.isLogin();
                        if( flag){ 
                                var apiPath = "bksignup/teamCreate";
                                var ps={
                                    sessionId: me.session.sessionId ,
                                    tel: me.session.tel ,
                                    teamName ,
                                    eventCode ,
                                    areaCode ,
                                    phaseCode ,
                                    logoImg
                                };
                                me.callApi( apiPath , ps).then (_res=>{
                                    console.log(_res);
                                    su(_res)
                                })
                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        },
        teamSetSignupStatus(teamKey , teamStatus){
            var me = bkAapi;
            var res = {
                status:0 ,
                team:{}
            }
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var flag = me.isLogin();
                        if( flag){ 
                                var apiPath = "bksignup/teamSetSignupStatus";
                                var ps={
                                    sessionId: me.session.sessionId ,
                                    tel: me.session.tel ,
                                    teamKey ,
                                    teamStatus 
                                };
                                me.callApi( apiPath , ps).then (_res=>{
                                    console.log(_res);
                                    su(_res)
                                })
                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        },
        memberCreate( teamKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList){
            var me = bkAapi;
            var res = {
                status:0 ,
                membere:{}
            }
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var flag = me.isLogin();
                        if( flag){ 
                                var apiPath = "bksignup/memberCreate";
                                var ps={
                                    sessionId: me.session.sessionId ,
                                    tel: me.session.tel , 
                                    teamKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList
                                };
                                me.callApi( apiPath , ps).then (_res=>{
                                    console.log(_res);
                                    su(_res)
                                })
                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        }, 
        memberEdit( memKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList){
            var me = bkAapi;
            var res = {
                status:0 ,
                membere:{}
            }
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var flag = me.isLogin();
                        if( flag){ 
                                var apiPath = "bksignup/memberEdit";
                                var ps={
                                    sessionId: me.session.sessionId ,
                                    tel: me.session.tel , 
                                    memKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList
                                };
                                me.callApi( apiPath , ps).then (_res=>{
                                    console.log(_res);
                                    su(_res)
                                })
                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        },
        memberUpdateExInfo( memKey , height , weight , width , bib, birthday, masterName , masterRelation, masterTel){
            var me = bkAapi;
            var res = {
                status:0 ,
                membere:{}
            }
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var flag = me.isLogin();
                        if( flag){ 
                                var apiPath = "bksignup/memberUpdateExInfo";
                                var ps={
                                    sessionId: me.session.sessionId ,
                                    tel: me.session.tel , 
                                    memKey , height , weight , width , bib, birthday, masterName , masterRelation, masterTel
                                };
                                me.callApi( apiPath , ps).then (_res=>{
                                    console.log(_res);
                                    su(_res)
                                })
                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        },
        memberRemove( memKey ){
            var me = bkAapi;
            var res = {
                status:0 ,
                membere:{}
            }
            return new Promise((su,fa)=>{
                try {
                    me.getSession().then(_=>{
                        var flag = me.isLogin();
                        if( flag){ 
                                var apiPath = "bksignup/memberRemove";
                                var ps={
                                    sessionId: me.session.sessionId ,
                                    tel: me.session.tel , 
                                    memKey 
                                };
                                me.callApi( apiPath , ps).then (_res=>{
                                    console.log(_res);
                                    su(_res)
                                })
                        }
                        else{
                            su(res)
                        }
                    })
                } catch (error) {
                    console.log(error);
                    su(res)
                }
            })
        }
    };
    var testTeamKey = 'a4006aa783ae4979993bfb9773f3f496';
    var testMemKey = 'cada1c12f2c24afb82c8902cd1887c8d';
    var testTel = '18601386396';
    export default {
        mounted(){
            var me = this;
            try {
                me.bk.getGameData().then(_=>{
                    console.log(me.bk)
                    return me.bk.getSession()
                }).then(_=>{
                    console.log(me.bk.session)
                })
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{
                bk: bkAapi,
                imgUrl:""
            }
        },
        methods:{
            acGetGameData(){
                var me = this;
                try {
                    me.bk.getGameData().then(_=>{
                        console.log(me.bk.gameData)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acGetUserData(){
                var me = this;
                try {
                    me.bk.updateUserData(true).then(  userData =>{
                        console.log(userData)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acGetSessionValid(){
                var me = this;
                try {
                    me.bk.requestSessionValid(testTel).then(_=>{
                        console.log(me.bk.session)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acCheckLogin(){
                var me = this;
                try {
                    me.bk.checkLogin('123456').then(_=>{
                        console.log(me.bk.session)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acTeamCreate(){
                var me = this;
                try {
                    var eventCode = 'MU8';
                    var areaCode = 'A02';
                    var teamName = '测试队';
                    var logoImg = 'http://sss';
                    var phaseCode = '';
                    me.bk.teamCreate( teamName , eventCode , areaCode , phaseCode , logoImg).then(_res=>{
                        console.log(_res)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acTeamSetSignupStatus(){
                var me = this;
                try {
                    var teamKey = testTeamKey;
                    var teamStatus = '02';
                    me.bk.teamSetSignupStatus(teamKey , teamStatus).then(_res=>{
                        console.log(_res)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acMemberCreate(){
                var me = this;
                try {
                    //teamKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList
                    var teamKey = testTeamKey;
                    var memberName = '张三丰';
                    var functionCode ='01';
                    var genderCode = 'M';
                    var idTypeCode = '01';
                    var idCode = '320402197510220000';
                    var memTel ='13312345678';
                    var photoImg='http://ssss';
                    var idImgs=['http://123','http://345']
                    var idImgList=JSON.stringify(idImgs)
                    me.bk.memberCreate(teamKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList).then(_res=>{
                        console.log(_res)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acMemberEdit(){
                var me = this;
                try {
                    //memKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList
                    var memKey = testMemKey;
                    var memberName = '李江海';
                    var functionCode ='01';
                    var genderCode = 'M';
                    var idTypeCode = '01';
                    var idCode = '32040219751022000x';
                    var memTel ='13312345678';
                    var photoImg='http://ssss';
                    var idImgs=['http://123','http://345']
                    var idImgList=JSON.stringify(idImgs)
                    me.bk.memberEdit(memKey , memberName , functionCode , genderCode , idTypeCode, idCode, memTel, photoImg , idImgList).then(_res=>{
                        console.log(_res)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acMemberUpdateExInfo(){
                var me = this;
                try {
                    //memKey , height , weight , width , bib, birthday, masterName , masterRelation, masterTel
                    var memKey = testMemKey;
                    var height = 170
                    var weight = 65
                    var width = 173
                    var bib = "10"
                    var birthday = '2015-09-01'
                    var masterName = "李国强"
                    var masterRelation = "父子"
                    var masterTel = "13901234567"
                    me.bk.memberUpdateExInfo(memKey , height , weight , width , bib, birthday, masterName , masterRelation, masterTel).then(_res=>{
                        console.log(_res)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acMemberRemove(){
                var me = this;
                try {
                    //memKey
                    var memKey = testMemKey;
                    me.bk.memberRemove(memKey ).then(_res=>{
                        console.log(_res)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acUploadImg(){
                var me = this;
                try {
                    var file = me.$refs.inputUploadFile.files[0];
                    var targetFn = 'test/data.jpg';
                    
                    me.bk.uploadLogoImg( file , targetFn ).then(res=>{
                        console.log(res)
                        if( res.status==1){
                            me.imgUrl = res.url;
                        } 
                    })
                } catch (error) {
                    console.log(error)
                }
            }, 
        }
    }
</script>

<style lang="scss" scoped>
    .header{
        position: fixed;
        width: 100%;
        background-color: #345678;
        color: #fff;
        padding: 15px;
        .toolbar{
            display: flex;
            align-items: center;
        }
    }
    .body{
        padding: 15px;
        padding-top: 75px;

        ul.lstAcs{
            background-color: #fff;
            box-shadow: 0 0 10px 0 #a0a0a0;
            border-radius: 7px;
            li{
                border-bottom: 1px solid #ddd;
                .ac{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 15px;
                    .title{
                        height: 45px;
                        line-height: 45px;
                    }
                }

                .upload{
                    padding: 10px;
                    .inputFile{
                        background-color: #eee;
                        padding: 10px;
                        text-align: left;
                    }
                    .img{
                        img{
                            width: 100%;
                        }
                    }

                }
            }
            li:active{
                background-color: #a0a0a0;
            }
        }
    }
</style>