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
            <div 
                v-for="(item,index) in items" :key="index"
                class="pool"
            >
                <div class="poolHeader">
                    <div class="poolName">{{item.poolName}}</div>
                    <div class="poolName">时间：{{item.startTime}}</div>
                    <div class="poolName">剑道：{{item.piste}}</div>
                    
                </div>
                <div class="poolBody">
                    <div class="th tItem"> 
                        <div class="order">序号</div>
                        <div class="name">运动员</div>
                        <div class="vd">1</div>
                        <div class="vd">2</div>
                        <div class="vd">3</div>
                        <div class="vd">4</div>
                        <div class="vd">5</div>
                        <div class="vd">6</div>
                        <div class="vd">7</div> 
                    </div>
                    <div
                        v-for="(reg,regIndex) in item.items" :key="regIndex"
                        class="tr tItem"
                    >
                        <div class="order">{{reg.matchOrder}}</div>
                        <div class="name">{{reg.F_DelegationShortName}} {{reg.F_PrintLongName}}</div>
                        <div class="vd">{{reg.r1}}</div>
                        <div class="vd">{{reg.r2}}</div>
                        <div class="vd">{{reg.r3}}</div>
                        <div class="vd">{{reg.r4}}</div>
                        <div class="vd">{{reg.r5}}</div>
                        <div class="vd">{{reg.r6}}</div>
                        <div class="vd">{{reg.r7}}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import gameResult from './gameResult';
    export default {
        name:"CompPoolResult",
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
                    console.log('load pool result', me.eventInfo.eventCode);
                    gameResult.getPoolResult(me.eventInfo.eventCode).then(_res=>{
                        me.items=[];
                        try {
                            _res.forEach(r=>{
                                if (r.items.length>0){
                                    r.poolName = r.items[0].poolName;
                                    r.piste = r.items[0].piste;
                                    r.startTime = r.items[0].startTime;
                                }
                            })
                            me.items = _res;
                        } catch (err) {
                            console.log(err)
                        }
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
            .pool{
                margin-bottom:25px;
                .poolHeader{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    text-align: left;
                    padding-left: 15px;
                    border-left: 2px solid #0066ee;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                .poolBody{
                    font-size: 0.85em;

                    .tItem{
                        display: flex;
                        align-items: center;
                        background-color: #fff; 
                        .order{
                            width: 30px;
                            height: 40px;
                            line-height: 40px;
                            border:1px solid #eee;
                        }
                        .vd{
                            width: 24px;
                            height: 40px;
                            line-height: 40px;
                            border:1px solid #eee;
                        }
                        .win{
                            width: 50px;
                            height: 50px;
                            line-height: 50px;
                            border:1px solid #eee;
                        }
                        .name{
                            flex: 1;
                            height: 40px;
                            line-height: 40px;
                            border:1px solid #eee;
                            text-align: left;
                            padding-left:10px;
                        }
                    }
                }
            }
        }
    }
</style>