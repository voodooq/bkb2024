<template>
    <div class="eventPage">
        <div class="header">
            <div class="top">
                <i @click="$router.back()" class="fa fa-chevron-left iconBtn"></i>
                <div class="title">
                    <div class="game">{{sysInfo.gameInfo.gameName}}</div>
                    <div class="event">{{eventInfo.eventName}}</div>
                </div>
                <div class="ac">&nbsp</div>
            </div>
            <div class="navs">
                <i class="fa fa-hand-o-left btn" @click="onPickItemBtn(-1)"></i>
                <div class="navItems" ref = "itemContainer">
                    <div class="items">
                        <div 
                            v-for="(item,index) in filters" :key="index"
                            :class="index==filterIndex?'item active':'item'"
                            @click="onPickItem(index)"
                        >
                            {{item.phaseName}}
                        </div>
                    </div>
                </div>
                <i class="fa fa-hand-o-right btn" @click="onPickItemBtn(1)"></i>
                <i class="fa fa-refresh btn" @click="refresh"></i>
            </div>
        </div>
        <div class="body">
            <comp-start-list
                v-if="currentPhase.phaseType =='startList' && eventInfo.typeCode=='I'"
                v-bind:sysInfo="sysInfo"
                v-bind:eventInfo="eventInfo"
                v-bind:phaseInfo="currentPhase"
            ></comp-start-list>
            <comp-start-list-team
                v-if="currentPhase.phaseType =='startList' && (eventInfo.typeCode=='T'  || eventInfo.typeCode=='X')"
                v-bind:sysInfo="sysInfo"
                v-bind:eventInfo="eventInfo"
                v-bind:phaseInfo="currentPhase"
            ></comp-start-list-team>
            <comp-pool-result
                v-if="currentPhase.phaseType=='poolResult'"
                v-bind:sysInfo="sysInfo"
                v-bind:eventInfo="eventInfo"
                v-bind:phaseInfo="currentPhase"
            ></comp-pool-result>
            <comp-pool-rank
                v-if="currentPhase.phaseType=='poolRank'"
                v-bind:sysInfo="sysInfo"
                v-bind:eventInfo="eventInfo"
                v-bind:phaseInfo="currentPhase"
            ></comp-pool-rank>
            <comp-dual-phase-result
                v-if="currentPhase.ac=='dualPhase' && currentPhase.hasNext>=0"
                v-bind:sysInfo="sysInfo"
                v-bind:eventInfo="eventInfo"
                v-bind:phaseInfo="currentPhase"
                v-bind:nextPhaseInfo="nextPhase"
            ></comp-dual-phase-result>
            <!--
            <comp-dual-phase-result-without-next
                v-if="currentPhase.ac=='dualPhase' && currentPhase.hasNext!=1"
                v-bind:sysInfo="sysInfo"
                v-bind:eventInfo="eventInfo"
                v-bind:phaseInfo="currentPhase" 
            ></comp-dual-phase-result-without-next>
            -->
            <comp-event-rank
                v-if="currentPhase.ac=='eventRank'"
                v-bind:sysInfo="sysInfo"
                v-bind:eventInfo="eventInfo"
                v-bind:phaseInfo="currentPhase"
            ></comp-event-rank>
        </div>
    </div>
</template>

<script>
    import  gameResult from './gameResult' 

    import CompStartList from './pgStartList.vue'
    import CompStartListTeam from './pgStartListTeam.vue'
    import CompPoolResult from './pgPoolResult.vue'
    import CompPoolRank from './pgPoolRank.vue'
    import CompDualPhaseResult from './pgDualPhaseResult.vue'
    import CompDualPhaseResultWithoutNext from './pgDualPhaseResultWithoutNext.vue'
    import CompEventRank from './pgEventRank.vue'
    export default {
        components:{
            CompStartList,
            CompStartListTeam,
            CompPoolResult,
            CompPoolRank,
            CompDualPhaseResult,
            CompDualPhaseResultWithoutNext,
            CompEventRank
        },
        mounted(){
            var me =this;
            try { 
                me.init(); 
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{ 
                eventCode:"",
                eventData:{},
                eventInfo:{},
                filters:[],
                filterIndex:0,
                currentPhase:{},
                nextPhase:{},
                localKey:"femo.localKey",
                localEventCodeKey:"femo.localEventCodeKey",
                sysInfo:{
                    gameInfo: {},
                    imgs: {
                        top:""
                    },
                    events: [],
                    dicts: {
                        event: [
                            { code: "T", lab: "团体赛" },
                            { code: "I", lab: "个人赛" },
                        ],
                        gender: [
                            { code: "M", lab: "男子" },
                            { code: "F", lab: "女子" }
                        ],
                        category: [

                        ],
                        weapon: [
                            { code: "花剑", lab: "花剑" },
                            { code: "重剑", lab: "重剑" },
                            { code: "佩剑", lab: "佩剑" }
                        ]
                    },
                },
                indexs:{
                    weaponIndex:0,
                    genderIndex:0,
                    eventIndex:0,
                },
                events:[],
                localKey:"femo.localKey",
                localEventCode:""
            }
        },
        methods:{
            init(){
                var me =this;
                try {
                    var content = window.sessionStorage.getItem(me.localEventCodeKey);
                    if( content && content!=null && content.length>0){
                        try {
                            me.eventCode = content;
                        } catch (err) {
                            indexs = null;
                        }
                    }
                    if( me.eventCode=="" ){
                        me.$royter.replace('femo');
                    }
                    else{
                        gameResult.loadSysDatas().then(_=>{
                            me.sysInfo =  gameResult.sysInfo;
                            me.eventInfo = gameResult.sysInfo.events.find( ev=>{
                                return ev.eventCode == me.eventCode;
                            });
                            console.log( me.eventInfo);
                            return gameResult.getDualPhases(me.eventInfo.eventCode)
                        }).then(_ps=>{
                            var filters =[{
                                    phaseType:"startList",
                                    phaseName :"参赛名单",
                                    ac:"startList"
                                }
                            ];
                            if ( me.eventInfo.hasPool && me.eventInfo.hasPool > 0){
                                filters.push({
                                    phaseType:"poolResult",
                                    phaseName :"小组赛成绩",
                                    ac:"poolResult"
                                },{
                                    phaseType:"poolRank",
                                    phaseName :"小组赛排名",
                                    ac:"poolRank"
                                },)
                            }
                            _ps.forEach(p=>{
                                p.ac = "dualPhase";
                                filters.push(p)
                            });
                            filters.push({
                                    phaseType:"eventRank",
                                    phaseName :"总排名",
                                    ac:"eventRank"
                            })

                            me.filters = filters;
                            console.log(me.filters)

                            me.onPickItem( me.filterIndex)
                        }) 
                    }
                } catch (error) {
                    console.log(error)
                }
            },
            onPickItem(index){
                var me =this;
                try {
                    me.filterIndex = index;
                    var v = me.$refs['itemContainer']; 
                    me.refresh();
                } catch (error) {
                    console.log(error)
                }
            },
            onPickItemBtn(flag){
                var me =this;
                try {
                    var count = me.filters.length;
                    if( flag>0 && me.filterIndex<count-1){
                        me.filterIndex = me.filterIndex + 1
                    }
                    else if( flag<0 && me.filterIndex>0){
                        me.filterIndex = me.filterIndex - 1
                    }
                    me.refresh();
                } catch (error) {
                    console.log(error)
                }
            },
            loadIndex(){
                var me =this;
                try {
                    var content = window.sessionStorage.getItem(me.localKey);
                    var indexs = null;
                    if( content && content!=null){
                        try {
                            indexs = JSON.parse(content);
                            me.indexs = indexs;
                        } catch (err) {
                            indexs = null;
                        }
                    }
                } catch (error) {
                    console.log(error)
                }
            },
            refresh(){
                var me =this;
                try {    
                    me.currentPhase = {};
                    me.$nextTick(_=>{
                        me.currentPhase = me.filters[me.filterIndex] ;
                        if( me.currentPhase && me.currentPhase.nextPhaseId && me.currentPhase.nextPhaseId>0){                        
                            me.nextPhase = me.filters.find( p=>{
                                return p.phaseId && p.phaseId == me.currentPhase.nextPhaseId;
                            });
                            me.currentPhase.hasNext = me.nextPhase && me.nextPhase!=null ?1 :0;
                        }
                        else{
                            me.nextPhase = {}
                            me.currentPhase.hasNext = 0 ;
                        }
                        console.log( me.currentPhase)
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            showEventPage( eventCode ){
                var me =this;
                try { 
                    var content = JSON.stringify(me.indexs);
                    window.sessionStorage.setItem( me.localKey , content);
                    window.sessionStorage.setItem( me.localEventCode , eventCode);
                    me.$router.push({
                        path:"femoEvent"
                    })
                } catch (error) {
                    console.log(error)
                }
            },
        }
    }
</script>

<style lang="less" scoped>
    .eventPage{
        .header{
            position: fixed;
            width: 100%;
            z-index: 999;
            .top{
                background-color: #0066ee;
                color: #fff;
                padding: 5px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                .iconBtn{
                    height: 42px;
                    line-height: 42px;
                    width: 42px;
                    text-align: center;
                }
            }
            .navs{
                display: flex;
                align-items: center;
                background-color: #fff;
                box-shadow: 0 0 10px 0 #e0e0e0;
                .btn{
                    height: 40px; 
                    padding-top: 13px;
                    width: 40px;
                    text-align: center;
                    background-color: #f1f2f3;
                    border:2px solid #fff;
                }
                .navItems{
                    flex: 1;
                    overflow-x: auto;
                    .items{
                        white-space: nowrap;
                        font-size: 0.9em;
                        .item{
                            display: inline-block;
                            padding: 5px 10px;
                            margin: 0 5px;
                            border-radius: 7px;
                        }
                        .item.active{
                            background-color: #0077fe;
                            color:#fff;
                            font-weight: bold;
                        }
                    }
                }
            }
        }
        .body{
            padding: 15px;
            padding-top: 110px;
        }
    }


</style>