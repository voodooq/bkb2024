<template>
    <div class="pg"> 
        <!--
        <div class="pgFilter">              
            <el-input
                placeholder="请输入单位或名称"
                suffix-icon="el-icon-search"
                v-model="searchText"
                @change="onSearch">
            </el-input>
        </div>
        -->
        <div class="pgItems"> 
            <div class="tabBody">
                <div 
                    v-for = "(item , index) in items" :key="index"
                    class="team"
                >
                    <div class="master">
                        <div class="order">{{item.teamOrder}}</div>
                        <div class="title">{{item.teamName}}</div>
                    </div>
                    <div class="detail">
                        {{item.members}}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import gameResult from './gameResult';
    export default {
        name:"CompStartListTeam",
        props:{
            sysInfo:{
                gameInfo:{}
            },
            eventInfo:{},
            phaseInfo:{}
        },
        mounted(){
            var me = this;
            try {
                me.refresh();
            } catch (error) {
                console.log(error);
            }
        },
        activated(){
            var me = this;
            try {
                console.log('startlistteam activated')
            } catch (error) {
                console.log(error);
            }
        },
        deactivated(){
            var me = this;
            try {
                console.log('startlistteam desactivated')
            } catch (error) {
                console.log(error);
            }
        }
        ,data(){
            return{
                searchText:"", 
                items:[]
            }
        }
        ,methods:{
            refresh(){
                var me = this;
                try {
                    console.log('load team start list', me.eventInfo.eventCode);
                    gameResult.getStartListTeam(me.eventInfo.eventCode).then(_res=>{
                        me.items = _res;
                        console.log(me.items)
                    })
                    
                } catch (error) {
                    console.log(error)
                }
            } ,
            onSearch(){
                var me = this;
                try {
                    var items = me.searchText && me.searchText!="" ? me.items.filter(item=>{
                            var falg = item.teamName.indexOf(me.searchText)>=0 || item.members.indexOf(me.searchText)>=0 ;
                            return falg;
                        }):me.items;
                    me.items = items;
                    console.log(me.items);
                } catch (error) {
                    console.log(error)
                }
            } 
        }
        
    }
</script>

<style lang="less" scoped>
    .pg{
        .pgFilter{
            margin-bottom: 15px;
        }
        .pgItems{
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 0 10px 0 #e3e3e3;
            .col{
                padding: 12px 0;            
            } 
            .tabHeader{
                background-color: #f5f7fa;
                font-weight: bold;
                display: flex;
            }          
            .tabBody{
                .team{
                    padding: 10px 15px;
                    border-bottom: 1px solid #e6e6e6;
                    .master{
                        display: flex;
                        align-items: center;
                        .order{
                            height: 32px;
                            line-height: 32px;
                            width: 32px;
                            text-align: center;
                            margin-right: 10px;
                            border-radius: 5px;
                            background-color: #f5f6f7;
                        }
                        .title{
                            font-weight: bold;
                        }
                    }
                    .detail{
                        text-align: left;
                        padding-left: 45px;
                    }
                }
            }
        }
    }
</style>