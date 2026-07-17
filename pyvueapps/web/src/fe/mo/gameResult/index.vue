<template>
    <div class="gameResult">
        <div class="top">
            <img :src="sysInfo.imgs.top" alt="">
            <div class="gameInfo">
                <div class="game">{{sysInfo.gameInfo.gameName}}</div>
                <div class="address">{{sysInfo.gameInfo.place}}</div>
            </div>
        </div>
        <div class="body">
                
            <div class="filter">
                <div class="r">
                    <div class="lab"><i class="fa fa-filter"></i> 剑种</div>
                    <div class="items">
                        <div
                            @click="indexs.weaponIndex=index;refresh()"
                            v-for="(item,index) in sysInfo.dicts.weapon"  :key="index"
                            :class="index == indexs.weaponIndex?'item active':'item'">
                                {{item.name}}
                        </div>
                    </div>
                </div>
                <div class="r">
                    <div class="lab"><i class="fa fa-user-plus"></i> 性别</div>
                    <div class="items">
                        <div
                            @click="indexs.genderIndex=index;refresh()"
                            v-for="(item,index) in sysInfo.dicts.gender"  :key="index"
                            :class="index == indexs.genderIndex?'item active':'item'">
                                {{item.name}}
                        </div>
                    </div>
                </div>
                <div class="r">
                    <div class="lab"><i class="fa fa-puzzle-piece"></i> 类别</div>
                    <div class="items">
                        <div
                            @click="indexs.eventIndex=index;refresh()"
                            v-for="(item,index) in sysInfo.dicts.event"  :key="index"
                            :class="index == indexs.eventIndex?'item active':'item'">
                                {{item.name}}
                        </div>
                    </div>
                </div>
            </div>
            <div class="events">
                <div class="eventItem" v-for="(item , index) in events" :key="index" @click="showEventPage(item.eventCode)">
                    <div class="eventName"> <i class="fa fa-sliders"></i> {{item.eventName}}</div>
                    <div class="icon">
                        <i class="fa fa-chevron-right"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import  gameResult from './gameResult' 
    export default {
        mounted(){
            var me =this;
            try { 
                gameResult.loadSysDatas().then(_=>{
                    me.sysInfo = gameResult.sysInfo;
                    return me.$nextTick();
                }).then(_=>{
                    me.refresh();
                })
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{ 
                sysInfo:{
                    gameInfo: {},
                    imgs: {
                        top:""
                    },
                    events: [],
                    dicts: {
                        event: [
                            { code: "T", name: "团体赛" },
                            { code: "I", name: "个人赛" },
                        ],
                        gender: [
                            { code: "M", name: "男子" },
                            { code: "F", name: "女子" }
                        ],
                        category: [

                        ],
                        weapon: [
                            { code: "花剑", name: "花剑" },
                            { code: "重剑", name: "重剑" },
                            { code: "佩剑", name: "佩剑" }
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
                localEventCodeKey:"femo.localEventCodeKey",
            }
        },
        methods:{
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
                    var eventCode = me.sysInfo.dicts.event[me.indexs.eventIndex].code ;
                    var genderCode = me.sysInfo.dicts.gender[me.indexs.genderIndex].code ;
                    var weaponCode = me.sysInfo.dicts.weapon[me.indexs.weaponIndex].code ;
                    var events = me.sysInfo.events.filter ( e=>{
                        var flag = e.typeCode == eventCode && 
                            e.genderCode == genderCode && 
                            e.weaponCode == weaponCode;
                        return flag;
                    });
                    me.events = events;                  
                } catch (error) {
                    console.log(error)
                }
            },
            showEventPage( eventCode ){
                var me =this;
                try { 
                    var content = JSON.stringify(me.indexs);
                    window.sessionStorage.setItem( me.localKey , content);
                    window.sessionStorage.setItem( me.localEventCodeKey , eventCode);
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
    .gameResult{
        .top{
            img{
                width: 100%;
            }
            position: relative;
            .gameInfo{
                width: 100%;
                position:absolute;
                bottom: 0px;
                font-weight: bold;
                color: #fff; 
                background-color: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: space-around;
                padding: 10px 0;
            }
        }

        .filter{
            background-color: #fff;
            padding: 0 10px;
            margin-bottom: 20px;
            .r{
                background-color: #fff;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 15px;
                border-bottom:1px solid #e2e2e2;
                .lab{
                    font-weight: bold;
                }
                .items{
                    display: flex;
                    align-items: center;
                    .item{
                        margin-left: 10px;
                        padding: 5px 10px;
                        border-radius: 5px;
                    }
                    .item.active{
                        background-color: #0066ee;
                        color: #fff;
                    }
                }
            }
            .r:last-child{
                border: 0;
            }
        }

        .body{
            padding: 15px;
            .events{
                background-color: #fff;
                border-radius: 7px;
                box-shadow: 0 0 10px 0 #e8e8e8;
                padding-left: 15px;
                .eventItem{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-bottom: 1px solid #f2f3f9;
                    .eventName{
                        height: 48px;
                        line-height: 48px;
                        i{
                            padding-right: 10px;
                        }
                    }
                    .icon{
                        padding-right: 5px;
                    }
                }
            }

        }
    }
</style>