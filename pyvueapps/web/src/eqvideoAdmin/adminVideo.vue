<template>
    <div class="result">
        <div class="athList">
            <div class="tool">
                <div class="filter">
                    <div class="item">
                        <el-select v-model="events.index" style= "width:100%" size="small"  @change="refresh">
                            <el-option 
                              
                                v-for = "(item, index) in events.items" 
                                :key="index"  
                                :label="item.eventName" 
                                :value="index">
                            </el-option>
                        </el-select>
                    </div>
                    <div class="item">
                        <el-select v-model="phases.index" style= "width:100%" size="small"  @change="refresh">
                            <el-option 
                               
                                v-for = "(item, index) in phases.items" 
                                :key="index"  
                                :label="item.phaseName" 
                                :value="index"></el-option>
                        </el-select>
                    </div>
                </div>
                <div class="search">
                    <el-input
                        size="small"
                        placeholder="请输入内容"
                        suffix-icon="el-icon-search"
                        v-model="search.searchText">
                    </el-input>
                </div>
                <div class="acs">
                    <div class="item">
                        <el-button @click="refresh" size="small" type="success" ><i class="fa fa-refresh"></i> 刷新</el-button>
                    </div>
                    <div class="item">
                        <el-button size="small" type="primary" ><i class="fa fa-download"></i> 导入</el-button>
                    </div>
                </div>
            </div>

            <div class="athletes"> 
                <el-row :gutter="15">
                    <el-col 
                        :span="4"
                        v-for="(item,index) in aths.items" :key="index"                    
                    >
                        <div class="videoItem">
                            <div class="videoPan">
                                <div class="thumb"></div>
                                <div class="info">
                                    <div class="title">
                                        <div class="ath">{{item.athName}}</div>
                                        <div class="horseName">{{item.horseName}}</div>
                                    </div>
                                    <div class="org">{{item.orgName}}</div>
                                </div>
                            </div>
                        </div>                        
                    </el-col>
                </el-row>
            </div>
        </div>  

    </div>
</template>

<script>
    class TResField{
        constructor(fieldName , caption=1 , tab =1, edit=1 , insert=1 , width=80 ){
            this.fieldName = fieldName;
            this.caption = caption;
            this.tab = tab;
            this.edit = edit ;
            this.insert = insert ;
            this.width = width;
        }
    }
    class TResDict{
        constructor(){
            this.fields=[
                new TResField('eventName','项目名称', 1 , 0 , 0 , 80),
                new TResField('phaseName','等级名称', 1 , 0 , 0 , 80),
                new TResField('orgName','单位名称'),
                new TResField('athName','选手姓名'),
                new TResField('athGender','性别'),
                new TResField('birthday','生日'),
                new TResField('athCode','选手编号'),
                new TResField('athFeId','FE编号'),
                new TResField('tel','电话'),
                new TResField('horseName','马匹名称'),
                new TResField('horseChip','马匹芯片'),
                new TResField('horseFeId','马匹FE'),
                new TResField('horseAge','马龄'),
                new TResField('spareHorse','备用马匹') 
            ];
            this.fieldDict={};
            this.init();
        }
        init(){
            var me = this;
            try {
                me.fields.forEach( f=>{
                    me.fieldDict[f.fieldName] = f;
                });
                console.log(me.fieldDict)
            } catch (error) {
                console.log(error)
            }
        }
    }
    export default {
        mounted(){
            var me = this;
            try {
                var sessionData = me.$eq.getAdminSessionData();
                me.gameInfo = sessionData.gameInfo;
                me.events.items = sessionData.events;
                me.phases.items = sessionData.phases;
                me.refresh();                
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{
                gameInfo:{},
                events:{
                    items:[],
                    index:0,
                },
                eventCode:"",
                phases:{
                    items:[],
                    index:0,
                },
                phaseCode:"",
                search:{
                    searchText:""
                },
                aths:{
                    items:[],
                    tags:["info" , "primary" , "success"],
                    index:0
                },
                resFields: new TResDict(),
                resInfoDlg:{
                    show: false,
                    resId:0,
                    resInfo:{}
                }
            }
        },
        methods:{
            refresh(){
                var me = this;
                try { 
                    me.resInfoDlg.show = false;
                    var ps = {
                        eventCode: me.events.items[me.events.index].eventCode ,
                        phaseCode: me.phases.items[me.phases.index].phaseCode ,
                    };
                    var key = "getResults" ;
                    me.$eq.api.msQuery(key , ps).then(res=>{
                        console.log(ps,res)
                        me.aths.items = res.data.recordset;
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            onPickEvent(ind){
                var me = this;
                try {
                    me.refresh();
                } catch (error) {
                    console.log(error)
                }
            },
            onPickPhase(ind){
                var me = this;
                try {
                    me.refresh();
                } catch (error) {
                    console.log(error)
                }
            }, 
        }
        
    }
</script>

<style lang="less" scoped>
    .result{        
        
        .athList{
            margin-right: 15px;
            .tool{
                display: flex; 
                align-content: center;
                padding: 15px 15px;                
                .filter{
                    display: flex;
                    justify-content: space-between;
                    align-content: center;
                    .item{
                        width: 160px;
                        padding-right: 10px;
                    } 
                }
                .search{

                }
                .acs{
                    display: flex;
                    align-items: center;
                    .item{
                        padding-left: 10px;                        
                    }
                }

            }
            .athletes{ 
                padding: 15px;
                .videoItem{
                    background-color: #fff;
                    box-shadow: 0 0 10px 0  #f0f0f0;
                    margin-bottom: 15px;
                    .videoPan{
                        .thumb{
                            position: relative;
                            height: 0;
                            padding-bottom: 100px;
                            background-color: #333;
                        }
                        .info{
                            padding: 10px;
                            .title{
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                font-weight: bold;
                                margin-bottom: 5px;
                            }
                            .org{
                                text-align: left;
                                color: #777;
                                font-size: 0.9em;
                            }
                        }
                    }
                }
            }
        } 
    } 

</style>