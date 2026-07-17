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
                        <el-select v-model="phases.index" style= "width:100%" size="small"  @change="refresh" >
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
                    <div class="item">
                        <el-button @click="acShowEditAdd" size="small" type="primary" ><i class="fa fa-plus"></i> 新增</el-button>
                    </div>
                </div>
            </div>

            <div class="athletes">
                
                <el-table :data="aths.items" border style="width: 100%" size="small">    
                    <el-table-column label="操作" width="80">
                        <template slot-scope="scope"> 
                            <el-button v-if="scope.row.resStatus>0" type="danger" size="mini" @click="acVideoReset(scope.row)">复位</el-button>  
                        </template>
                    </el-table-column>
                    <el-table-column prop="resId" label="ID" width="60"></el-table-column>
                    <el-table-column label="出场序" width="70">
                        <template slot-scope="scope">
                            <input class="resOrderInput" v-model="scope.row.resOrder" type="text" @change="acUpdateResOrder(scope.row)">
                        </template>
                    </el-table-column>                
                    <el-table-column prop="athName" label="姓名" width="120"></el-table-column>
                    <el-table-column prop="athGender" label="性别" width="60"></el-table-column>
                    <el-table-column prop="orgName" label="单位" width="260"></el-table-column>
                    <el-table-column prop="horseName" label="马匹" width="120"></el-table-column>
                    <el-table-column label="状态" width="80">
                        <template slot-scope="scope">
                            <div slot="reference" class="name-wrapper">
                                <el-tag :type="aths.tags[scope.row.resStatus]" size="medium">{{ scope.row.resStatusName }}</el-tag>
                            </div> 
                        </template> 
                    </el-table-column>
                    <el-table-column label="时间" width="120">
                        <template slot-scope="scope">                               
                            <div class="time" >                                
                                <el-popover trigger="hover" placement="top" >
                                    <p v-if = "scope.row.endTm==0">
                                        
                                        <el-date-picker
                                            @input="changeTime(scope.row)"
                                            v-model="scope.row.time"
                                            type="datetimerange"
                                            range-separator="至"
                                            start-placeholder="开始日期"
                                            end-placeholder="结束日期">
                                        </el-date-picker>
                                    </p>
                                    <p v-if = "scope.row.endTm>0">
                                        <el-time-picker is-range
                                            @input="changeTime(scope.row)"
                                            v-model="scope.row.time"
                                            range-separator="至"
                                            start-placeholder="开始时间"
                                            end-placeholder="结束时间"
                                            placeholder="选择时间范围">
                                        </el-time-picker> 
                                    </p>
                                    <div slot="reference" class="name-wrapper">
                                        <el-tag size="medium" v-if = "scope.row.endTm>0">{{ scope.row.timeStr }} + {{ scope.row.duration }}</el-tag>
                                        <el-tag size="medium" v-if = "scope.row.endTm==0" >设置时间</el-tag>
                                    </div>
                                </el-popover> 
                            </div>
                        </template>
                    </el-table-column>                
                    <el-table-column
                        label="VOD"
                        width="160">
                        <template slot-scope="scope">
                            <el-popover trigger="hover" placement="top" v-if="scope.row.vodFlag>0">
                            <p>{{ scope.row.vodUrl }}</p>
                            <div slot="reference" class="name-wrapper">
                                <el-tag size="medium">{{ scope.row.videoCode }}</el-tag>
                            </div>
                            </el-popover>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作">
                        <template slot-scope="scope">
                            <el-button size="mini" @click="acVideoEdit(scope.row)">修改</el-button> 
                            <el-button v-if="scope.row.resStatus==0" type="success" size="mini" @click="acVideoStart(scope.row)">开始</el-button> 
                            <el-button v-if="scope.row.resStatus==1" type="warning" size="mini" @click="acVideoStop(scope.row)">停止</el-button>  
                            <el-button v-if="scope.row.resStatus>1" type="primary" size="mini" @click="acVideoM3u8(scope.row)">回放</el-button> 
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <div class="videoPan">
            
        </div>
        <el-dialog title="参赛选手" :visible.sync="resInfoDlg.show" :close-on-click-modal="false">
            <el-divider></el-divider>
            <div class="editForm">
                <el-row :gutter="15">
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">编号</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.athCode"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">姓名</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.athName"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">性别</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.athGender"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">生日</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.birthday"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">教练</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.coach"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">电话</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.tel"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="24">
                        <div class="item">
                            <div class="label">单位</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.orgName"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">马匹名称</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.horseName"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">马匹芯片</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.horseChip"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">马匹FE</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.horseFeId"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">马匹年龄</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.horseAge"></el-input>
                            </div>
                        </div>
                    </el-col>
                    <el-col :span="8">
                        <div class="item">
                            <div class="label">备用马匹</div>
                            <div class="edit">
                                <el-input style="width:100%" size="small" v-model="resInfoDlg.resInfo.spareHorse"></el-input>
                            </div>
                        </div>
                    </el-col>
                </el-row>
            </div>
            <el-divider></el-divider>
            <div class="postBtn">
                <el-button @click="acCancelEdit" type="warning" size="small"><i class="fa fa-reply"></i> 取消</el-button>
                <el-button @click="acPostEdit" type="success" size="small"><i class="fa fa-save"></i> 保存</el-button>
            </div>
        </el-dialog>

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
                ,curDate: new Date()
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
                        me.aths.items = res.data.recordset;
                        me.aths.items.forEach( r=>{
                            r.startTime =r.utcStart>0? new Date( r.utcStart *1000): new Date();
                            r.endTime = r.utcEnd>0? new Date( r.utcEnd *1000): new Date();
                            r.time = [r.startTime  , r.endTime]
                        })
                        console.log(me.aths.items)
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
            acShowEditAdd(){
                var me = this;
                try {
                    me.resInfoDlg.resId = 0 ;
                    me.resInfoDlg.resInfo = {
                        gameCode: me.gameInfo.gameCode,
                        eventCode: me.events.items[me.events.index].eventCode ,
                        phaseCode: me.phases.items[me.phases.index].phaseCode ,
                        orgName:"",
                        athName:"",
                        athGender:"",
                        birthday:"",
                        coach:"",
                        athCode:"",
                        athFeId:"",
                        tel:"",
                        horseName:"",
                        horseChip:"",
                        horseFeId:"",
                        horseCode:"",
                        horseAge:"",
                        spareHorse:""
                    };
                    console.log( me.resInfoDlg.resInfo)
                    me.resInfoDlg.show = true;
                } catch (error) {
                    console.log(error)
                }
            },
            acCancelEdit(){
                var me = this;
                try {
                    me.resInfoDlg.show = false;
                } catch (error) {
                    console.log(error)
                }
            },
            acPostEdit(){
                var me = this;
                try {
                    me.resInfoDlg.show = false;
                    var ps = me.resInfoDlg.resInfo;
                    var key = me.resInfoDlg.resId>0?"resultEdit":"resultCreate";
                    me.$eq.api.msQuery(key , ps).then(res=>{
                        me.refresh();
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acVideoEdit(resInfo){
                var me = this;
                try {
                    me.resInfoDlg.resId = resInfo.resId ;
                    me.resInfoDlg.resInfo = resInfo;
                    me.resInfoDlg.show = true;
                } catch (error) {
                    console.log(error)
                }
            }, 
            acVideoStart(resInfo){
                var me = this;
                try {
                    me.$eq.setVideoStatus(resInfo.resId , 1).then(_=>{
                        me.refresh();
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acVideoStop(resInfo){
                var me = this;
                try {
                    me.$eq.setVideoStatus(resInfo.resId , 2).then(_=>{
                        me.refresh();
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acVideoReset(resInfo){
                var me = this;
                try {
                    me.$eq.setVideoStatus(resInfo.resId , 0).then(_=>{
                        me.refresh();
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acVideoM3u8(resInfo){
                var me = this;
                try {
                    me.$eq.api.generateVod(resInfo.videoCode , resInfo.tmFrom , resInfo.tmEnd).then(res=>{
                        if( res && res.status==1){
                            me.$eq.setVodFlag(resInfo.resId , 1).then(_res=>{
                                me.$message.success('已生成点播回放资源')
                            })
                        }
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            acUpdateResOrder (resInfo){
                var me = this;
                try {
                    var ps = {
                        resId:resInfo.resId,
                        resOrder: resInfo.resOrder
                    };
                    var key = "setVideoOrder";
                    me.$eq.api.msQuery(key, ps).then(_res => {
                       me.refresh(); 
                    });
                } catch (error) {
                    console.log(error)
                }
            },
            changeTime (resInfo){
                var me = this;
                try {
                    var start = resInfo.time[0].getTime()/1000 + 8*3600;
                    var end = resInfo.time[1].getTime()/1000 + 8*3600;

                    var ps = {
                        resId:resInfo.resId,
                        start ,
                        end
                    };
                    var key = "setTime";
                    me.$eq.api.msQuery(key, ps).then(_res => {
                       me.refresh(); 
                    });
                } catch (error) {
                    console.log(error)
                }
            }
        }
        
    }
</script>

<style lang="less" scoped>
    .result{        
        
        .athList{
            margin-right: 15px;
            background-color: #fff;
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
            }
        }
        .videoPan{
            width:320px;
            position: fixed;
            right: 50px;
            top: 85px;
            background-color: #fff;
        }
    }

    .editForm{
        .item{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            .label{
                width: 80px;
                padding-right: 5px;
                text-align: right;
            }
            .edit{
                flex: 1;
            }
        }
    }

    .resOrderInput{
        width: 40px;
        text-align: center;
    }

    .time{
        display: flex;
        align-items: center;
        .duration{
            padding: 0 10px;
        }
    }

</style>