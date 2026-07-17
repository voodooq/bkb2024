<template>
    <div class="pg">
        <div class="pgHeaderFix">
            <i @click="$router.back()" class="btnBack fa fa-chevron-left"></i>
            <div class="title">{{ videoInfo.gameName }} - {{ videoInfo.athName }}</div>
            <el-button size="small" type="primary">
                <i class="fa fa-refresh"></i> 刷新
            </el-button>
        </div>

        <div class="pgBody"> 
            <div class="videoFrame">

            </div>
            <div class="videoData">
                <div class="vidoInfo">
                    <div class="infoItem">
                        <i class="fa fa-server itemIcon"></i>
                        <div class="data">
                            <div class="lab">赛事名称</div>
                            <div class="value">{{ videoInfo.gameName }}</div>
                        </div>
                    </div>
                </div>
                <div class="vidoInfo">
                    <div class="infoItem">
                        <i class="fa fa-server itemIcon"></i>
                        <div class="data">
                            <div class="lab">项目名称</div>
                            <div class="value">{{ videoInfo.eventName }}</div>
                        </div>
                    </div>
                </div>
                <div class="vidoInfo">
                    <div class="infoItem">
                        <i class="fa fa-server itemIcon"></i>
                        <div class="data">
                            <div class="lab">考核等级</div>
                            <div class="value">{{ videoInfo.phaseName }}</div>
                        </div>
                    </div>
                </div>
                <div class="vidoInfo">
                    <div class="infoItem">
                        <i class="fa fa-server itemIcon"></i>
                        <div class="data">
                            <div class="lab">状态</div>
                            <div class="value">{{ videoInfo.resStatusName }}</div>
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
            me.videoCode = me.$route.query.videoCode;
            me.refresh ();
        } catch (error) {
            console.log(error)
        }
    },
    data(){
        return{  
            videoCode:"", 
            videoInfo:{}
        }
    },
    methods:{  
        refresh (){
            var me = this;
            try { 
                me.$eq.getVideoInfo(me.videoCode).then(_res=>{
                    me.videoInfo = _res;
                    console.log(_res)
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
        padding: 0px;
        padding-top: 60px;
        
    } 

    .videoFrame{
        height: 240px;
        background-color: #222;
        margin-bottom: 15px;
    }

    .videoData{
        padding: 15px;
        .vidoInfo{
            background-color: #fff;
            border-radius: 10px;
            background-color: 0 0 10px 0 #f0f0f0;
            .infoItem{
                display: flex;
                align-items: center;
                .itemIcon{
                    height: 40px;
                    line-height: 40px;
                    width: 40px;
                    text-align: center;
                }
                .data{
                    flex: 1;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0 10px;
                    border-bottom:1px solid #eee;
                    min-height: 40px;
                    .lab{
                        font-weight: bold;
                    }
                }
            }
        }
        .vidoInfo:last-child .infoItem .data{
            border:0
        }
    }
</style>