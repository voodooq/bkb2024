<template>
    <div class="pg">
        <div class="pgHeaderFix">
            <i @click="$router.back()" class="btnBack fa fa-chevron-left"></i>
            <div class="title">{{ userInfo.gameName }}</div>
            <div class="btns">
                <el-button @click="refresh" size="small" type="primary">
                    <i class="fa fa-refresh"></i> 刷新
                </el-button> 
            </div>
        </div>

        <div class="pgBody"> 
            <div class="filter">
                <div class="filterRow">
                    <div class="lab">项目</div>
                    <div class="data">
                        <div
                            v-for="(item,index) in events.items" :key="index"
                        >
                            {{ item.eventName }}
                        </div>
                    </div>
                </div>
                <div class="filterRow">
                    <div class="lab">等级</div>
                    <div class="data">
                        <div
                            v-for="(item,index) in phases.items" :key="index"
                        >
                            {{ item.eventName }}
                        </div>
                    </div>
                </div>
            </div>

            <div class="aths">
                <div 
                    v-for ="(item,index) in aths" :key="index"
                    class="athItem"
                >
                    <div class="athInfo">
                        <div class="athName">
                            {{ item.resOrder }} - {{ item.athName }}
                        </div>
                        <div class="horseName">{{ item.horseName }}</div>
                    </div>
                    <div class="action">
                        <ul class="lstAcs">
                            <li>
                                <el-button @click="acStart(index)" v-if="item.resStatus==0" size="small" type="primary">开始</el-button>
                            </li>
                            <li>
                                <el-button @click="acReset(index)" v-if="item.resStatus!=0" size="small" type="danger">复位</el-button>
                            </li>
                            <li>
                                <el-button @click="acStop(index)" v-if="item.resStatus==1" size="small" type="success">完成</el-button>
                            </li>
                        </ul>
                        <div class="status">{{ item.resStatusName }}</div>
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
                me.userInfo = me.$eq.datas.userInfo;
                console.log(me.userInfo)
                me.events.items = me.userInfo.events;
                me.phases.items = me.userInfo.phases;
                me.refresh();
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{ 
                userInfo:{},
                events:{
                    items:[],
                    index:0
                },
                phases:{
                    items:[],
                    index:0
                },
                aths:[],
                liveVideos:[]
            }
        },
        methods:{  
            init (){
                var me = this;
                try {  
                } catch (error) {
                    console.log(error)
                }
            } ,
            refresh (){
                var me = this;
                try {  
                } catch (error) {
                    console.log(error)
                }
            } ,
            acStart (index){
                var me = this;
                try {  
                } catch (error) {
                    console.log(error)
                }
            } ,
            acReset (index){
                var me = this;
                try {  
                } catch (error) {
                    console.log(error)
                }
            } ,
            acStop (index){
                var me = this;
                try {  
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
</style>