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
            <el-table
                :data="items" stripe style="width: 100%" size="mini"
            >
                <el-table-column prop="rank" label="排名" width="50"></el-table-column>
                <el-table-column prop="orgName" label="单位" width="100"></el-table-column>
                <el-table-column label="名称" >
                    <template slot-scope="scope">
                        <div class="master" ><b>{{scope.row.regName}}</b></div>
                        <div class="detail">{{scope.row.teamMember}}</div>
                    </template>
                </el-table-column> 
                <el-table-column label="奖牌" width="50" >
                    <template slot-scope="scope">
                        <img class="medalImg" v-if="scope.row.medalCode!=''" :src="medalImgs[scope.row.medalCode]" alt="">
                    </template>
                </el-table-column>
                <el-table-column prop="irm" label="判罚" width="50"></el-table-column>
            </el-table>

        </div>
    </div>
</template>

<script>
import gameResult from './gameResult';
    export default {
        name:"CompEventRank",
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
                items:[],
                medalImgs:[]
            }
        }
        ,methods:{
            refresh(){
                var me = this;
                try {
                    console.log('load eventRank', me.eventInfo.eventCode);
                    me.medalImgs = gameResult.sysInfo.imgs.medals;
                    gameResult.getEventRank(me.eventInfo.eventCode).then(_res=>{
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
            .medalImg{
                width: 32px;
                height: 32px;
            }
        }
    }
</style>