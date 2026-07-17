<template>
    <div class="duals">
        <div class="dualHeader">
            <div class="current item">{{phaseInfo.phaseName}}</div> 
        </div>
        <div class="dualMatchs">
            <div class="currentMatchBlock">
                <div 
                    v-for = "(item ,index) in currentMatchs" :key = "index"
                    class="match current"
                >
                    <div :class="item.homeWinSets==1? 'reg home active':'reg home'">
                        <div class="org">{{item.homeOrgName}} <b>{{item.homeAthName}}</b></div> 
                        <div class="points">{{item.homwPoints}}</div> 
                    </div>
                    <div :class="item.awayWinSets==1? 'reg away active':'reg away'">
                        <div class="org">{{item.awayOrgName}} <b>{{item.awayAthName}}</b></div>  
                        <div class="points">{{item.awayPoints}}</div> 
                    </div>
                </div>
            </div>
            <div class="linkBlock1">
                <div 
                    v-for = "(item ,index) in currentMatchs" :key = "index"
                    class="link"
                > &nbsp
                </div>
            </div> 
        </div>
    </div>
</template>

<script>
import gameResult from './gameResult';
    export default {
        name:"CompDualPhaseResultWithoutNext",
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
                currentMatchs:[],
                nextMatchs:[]
            }
        }
        ,methods:{
            refresh(){
                var me = this;
                try {
                    gameResult.getDualPhaseMatch(me.phaseInfo.phaseId).then(_curMatchs=>{
                        me.currentMatchs = _curMatchs; 
                        console.log( me.currentMatchs);
                    })
                } catch (error) {
                    console.log(error)
                }
            }
        }
        
    }
</script>

<style lang="less" scoped>
    .duals{
        .dualHeader{
            display: flex;
            align-items: center;
            justify-content: space-around;
            margin-bottom: 15px;
            .item{
                background-color: #0066ee;
                color: #fff;
                padding: 10px 15px ;
                border-radius: 7px;
            }
        }

        .dualMatchs{
            display: flex;
            font-size: 0.85em;
            padding-left: 110px;
            .currentMatchBlock{
                .match{
                    .reg{
                        width: 140px;
                        padding: 0 5px;
                        background-color: #fff;
                        height: 32px;
                        margin-bottom: 24px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }
                    .reg.active{
                        box-shadow: 0 0 10px 0 #e6e7e8;
                        background-color: #0ba376;
                        color: #fff;
                    }
                }
            }
            .nextMatchBlock{
                padding-top: 28px;
                .match{
                    .reg{
                        width: 140px;
                        padding: 0 5px;
                        background-color: #fff;
                        height: 32px;
                        margin-bottom: 80px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }
                }
            }

            .linkBlock1{
                width: 20px;
                padding-top: 16px;
                .link{
                    height: 56px;
                    margin-bottom: 56px;
                    border:1px solid #666;
                    border-left: 0;
                }
            }

            .linkBlock2{
                width: 20px;
                padding-top: 44px;
                .link{
                    height: 56px;
                    margin-bottom: 56px;
                    border-top:1px solid #666;
                }
            }

            .linkBlock3{
                width: 20px;
                padding-top: 44px;
                .link{
                    height: 112px;
                    margin-bottom: 112px;
                    border:1px solid #666;
                    border-left: 0;
                }
            }
        }
    }
</style>