<template>
    <div class="pg"> 
        <!--
        <div class="pgFilter">              
            <el-input
                placeholder="请输入单位或姓名"
                suffix-icon="el-icon-search"
                v-model="searchText"
                @change="onSearch">
            </el-input>
        </div>
        -->
        <div class="pgItems">
            <div class="tabHeader">
                <div class="col order">
                    序号
                </div>
                <div class="col athName">
                    姓名
                </div>
                <div class="col orgName">
                    单位
                </div>
            </div>
            <div class="tabBody">
                <div 
                    v-for = "(item , index) in items" :key="index"
                    class="rowItem"
                >
                    <div class="col order">{{item.athOrder}}</div>
                    <div class="col athName">{{item.athName}}</div>
                    <div class="col orgName">{{item.orgName}}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import gameResult from './gameResult';
    export default {
        name:"CompStartList",
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
                console.log('startlist activated')
            } catch (error) {
                console.log(error);
            }
        },
        deactivated(){
            var me = this;
            try {
                console.log('startlist desactivated')
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
                    console.log('load start list', me.eventInfo.eventCode);
                    gameResult.getStartList(me.eventInfo.eventCode).then(_res=>{
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
                            var falg = item.athName.indexOf(me.searchText)>=0 || item.orgName.indexOf(me.searchText)>=0 ;
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
            .order{
                width: 60px;
            }
            .athName{
                width: 120px;
                text-align: left;
            }
            .orgName{
                flex: 1;
                text-align: left;
            }
            .tabHeader{
                background-color: #f5f7fa;
                font-weight: bold;
                display: flex;
            }          
            .tabBody{
                .rowItem{
                    display: flex;
                }

                .rowItem:nth-child(even){
                    background-color: #f7f8f9;
                }
            }
        }
    }
</style>