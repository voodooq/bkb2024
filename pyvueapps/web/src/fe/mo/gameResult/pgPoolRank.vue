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
                <el-table-column prop="poolRank" label="排名" width="50"></el-table-column>
                <el-table-column label="单位/姓名" >
                    <template slot-scope="scope">
                        <div>{{scope.row.F_DelegationShortName}}</div>
                        <div>{{scope.row.F_PrintLongName}}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="diff" label="diff" width="40"></el-table-column>
                <el-table-column prop="indexWin" label="win" width="60"></el-table-column>
                <el-table-column prop="hr" label="hr" width="40"></el-table-column>
                <el-table-column prop="hs" label="hs" width="40"></el-table-column>
                <el-table-column label="晋级" width="50" >
                    <template slot-scope="scope">
                        <i :class="scope.row.qualify==1?'fa fa-flag qualifyFlag':''"></i>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
import gameResult from './gameResult';
    export default {
        name:"CompPoolRank",
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
                    console.log('load pool rank list', me.eventInfo.eventCode);
                    gameResult.getPoolRank(me.eventInfo.eventCode).then(_res=>{
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
                            var falg = item.F_DelegationShortName.indexOf(me.searchText)>=0 || item.F_PrintLongName.indexOf(me.searchText)>=0 ;
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
            .qualifyFlag{
                color: #0a9147;
            }
        }
    }
</style>