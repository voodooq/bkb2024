<template>
    <div class="duals">
        <div class="dualHeader">
            <div class="current item">{{phaseInfo.phaseName}}</div>
            <div v-if="nextPhaseInfo.phaseId>0" class="next item">{{nextPhaseInfo.phaseName}}</div>
        </div>
        <div class="dualMatchs">
                <div class="matchPan">
                    <div 
                        v-for="(item , index) in currentMatchs" :key="index"
                        class="match"
                    >
                        <div class="regs">
                            <div :class="item.homeWinSets>0?'reg home active':'reg home' ">
                                <div class="orgName">{{item.homeOrgName}} {{item.homeAthName}}</div>
                                <div class="score">{{item.homwPoints}}</div>
                            </div>
                            <div class="matchInfo">
                                <div class="tm"  v-if="item.startTime && item.startTartim!=''">时间：{{item.startTime}} </div>
                                <div class="piste" v-if="item.piste && item.piste!=''">剑道：{{ item.piste}}</div>
                            </div>
                            <div :class="item.awayWinSets>0?'reg away active':'reg away' ">
                                <div class="orgName">{{item.awayOrgName}} {{item.awayAthName}}</div>
                                <div class="score">{{item.awayPoints}}</div>
                            </div>
                        </div>
                        <div class="link1"></div>
                        <div class="link2"></div>
                        <div class="winReg">
                            <div class="orgName">{{item.winOrgName}} {{item.winAthName}}</div>
                        </div>
                    </div>
                </div>
                <div v-if="phaseInfo.nextPhaseId>0" class="matchLinks">
                    <div class="item" v-for="(item,index) in matchLinks" :key="index" ></div>
                </div>
        </div>
    </div>
</template>

<script>
import gameResult from './gameResult';
    export default {
        name:"CompDualPhaseResult",
        props:{
            sysInfo:{
                gameInfo:{}
            },
            eventInfo:{},
            phaseInfo:{},
            nextPhaseInfo:{},
            matchLinks:[]
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
                    /*
                    gameResult.getDualPhaseMatch(me.phaseInfo.phaseId).then(_curMatchs=>{
                        me.currentMatchs = _curMatchs;
                        return gameResult.getDualPhaseMatch(me.nextPhaseInfo.phaseId);
                    }).then(_nextMatchs=>{
                        me.nextMatchs = _nextMatchs;

                        console.log( me.currentMatchs)
                        console.log( me.nextMatchs)
                    })
                    */
                    gameResult.getDualPhaseMatch(me.phaseInfo.phaseId).then(_curMatchs=>{
                        _curMatchs.forEach( r=>{
                            r.winOrgName = "";
                            r.winAthName = ""; 
                            if( r.homeWinSets==1){
                                r.winOrgName = r.homeOrgName;
                                r.winAthName = r.homeAthName;
                            }
                            else if( r.awayWinSets==1){
                                r.winOrgName = r.awayOrgName;
                                r.winAthName = r.awayAthName;
                            }
                        });
                        var matchLinks =[];
                        if( me.phaseInfo.nextPhaseId>0 ){
                            var count = _curMatchs.length / 2;
                            for( var i = 0 ; i<count ; i++){
                                matchLinks.push(i)
                            }
                        }
                        me.matchLinks = matchLinks;
                        
                        me.currentMatchs = _curMatchs;
                        console.log(me.phaseInfo, me.currentMatchs);
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
            font-size: 0.85em;;
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
                    border:1px solid #999;
                    border-left: 0;
                }
            }

            .linkBlock2{
                width: 20px;
                padding-top: 44px;
                .link{
                    height: 56px;
                    margin-bottom: 56px;
                    border-top:1px solid #999;
                }
            }

            .linkBlock3{
                width: 20px;
                padding-top: 44px;
                .link{
                    height: 112px;
                    margin-bottom: 112px;
                    border:1px solid #aaa;
                    border-left: 0;
                }
            }
        }
    }

    .matchPan{
        .match{
            width:320px;
            display: flex;
            align-items: center;
            padding-bottom: 40px;
            .regs{
                width: 180px;
                .reg{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 5px;
                    height: 40px;
                    line-height: 40px;
                    box-sizing: border-box;
                    border:1px solid #ddd;
                }
                .reg.active{
                    background-color: #08992c;
                    color: #fff;
                    border:1px solid #066347;
                }
                .matchInfo{
                    display: flex;
                    align-items: center;
                    justify-content: flex-end;
                    height: 40px ;
                    line-height: 40px;
                    padding-right: 5px; 
                    .tm{
                        padding-right: 10px;
                    }
                }
            }
            .link1{
                width: 25px;
                height: 80px; 
                border:1px solid #aaa;
                border-left: 0;
            }
            .link2{
                width: 25px;
                height: 0px; 
                border:1px solid #aaa;
                border-left: 0;
            }
            .winReg{
                display: flex;
                width: 140px;
                align-items: center;
                justify-content: space-between;
                padding: 0 5px;
                height: 40px;
                line-height: 40px;
                box-sizing: border-box;
                border:1px solid #ddd;
            }
        }
    }
    .matchLinks{
        padding-top: 60px;
        .item{
            width:25px;
            height: 160px;
            margin-bottom: 160px;
            border:1px solid #aaa;
            border-left: 0;

        }
    }
</style>