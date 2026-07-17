<template>
    <div class="gameInfo">
        <div class="formEdit">
            <el-row :gutter="15">
                <el-col :span="8">
                    <div class="editRow">
                        <div class="lab">编号</div>
                        <div class="edit">
                            <el-input disabled style="width:100%" v-model="gameInfo.gameCode"></el-input>
                        </div>
                    </div>
                </el-col>
                <el-col :span="16">
                    <div class="editRow">
                        <div class="lab">名称</div>
                        <div class="edit">
                            <el-input style="width:100%" v-model="gameInfo.gameName"></el-input>
                        </div>
                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="editRow">
                        <div class="lab">开始时间</div>
                        <div class="edit">
                            <el-input style="width:100%" v-model="gameInfo.openDate"></el-input>
                        </div>
                    </div>
                </el-col> 
                <el-col :span="8">
                    <div class="editRow">
                        <div class="lab">结束时间</div>
                        <div class="edit">
                            <el-input style="width:100%" v-model="gameInfo.closeDate"></el-input>
                        </div>
                    </div>
                </el-col> 
                <el-col :span="8">
                    <div class="editRow">
                        <div class="lab">举办地点</div>
                        <div class="edit">
                            <el-input style="width:100%" v-model="gameInfo.address"></el-input>
                        </div>
                    </div>
                </el-col> 
                <el-col :span="24">
                    <div class="editRow">
                        <div class="lab">备注说明</div>
                        <div class="edit">
                            <el-input style="width:100%" v-model="gameInfo.gameDesc"></el-input>
                        </div>
                    </div>
                </el-col> 
                <el-col :span="24">
                    <el-divider> 媒体地址 </el-divider>
                </el-col>
                <el-col :span="24">
                    <div class="editRow">
                        <div class="lab">RtmpUrl</div>
                        <div class="edit">
                            <el-input style="width:100%" v-model="gameInfo.rtmpUrl"></el-input>
                        </div>
                    </div>
                </el-col> 
                <el-col :span="24">
                    <div class="editRow">
                        <div class="lab">FlvUrl</div>
                        <div class="edit">
                            <el-input style="width:100%" v-model="gameInfo.flvUrl"></el-input>
                        </div>
                    </div>
                </el-col> 
                <el-col :span="24">
                    <div class="editRow">
                        <div class="lab">M3u8Url</div>
                        <div class="edit">
                            <el-input style="width:100%" v-model="gameInfo.m3u8Url"></el-input>
                        </div>
                    </div>
                </el-col> 
                <el-col :span="24">
                    <div class="editRow">
                        <div class="lab">VodUrl</div>
                        <div class="edit">
                            <el-input style="width:100%" v-model="gameInfo.vodUrl"></el-input>
                        </div>
                    </div>
                </el-col> 
                <el-col :span="24">
                    <el-divider></el-divider>
                </el-col>                
            </el-row>
            <div class="formBtns">
                <el-button type="warning"><i class="fa fa-reply"></i> 重置</el-button>
                <el-button @click="post" type="success"><i class="fa fa-save"></i> 保存</el-button>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name:"GameInfo",
        props:{
            gameInfo:{
                gameId :0 ,
                gameCode:"",
                gameName:"",
                gameDesc:"",
                address:"",
                openDate:"",
                endDate:""
            }
        },
        data(){
            return {}
        },
        methods:{
            post(){
                var me = this;
                try {
                    console.log(me.gameInfo)
                    var key = "saveGameInfo";
                    me.$eq.api.msQuery(key, me.gameInfo).then(_res => {
                        if( _res && _res.data && _res.data.execResult && _res.data.execResult.rowCount>0){
                            var game = me.$eq.getAdminSessionData()
                            game.gameInfo = me.gameInfo;
                            me.$eq.setAdminSessionData(game);
                            me.$message.success('保存成功')
                        }
                        else{
                            me.$message.error('提交失败')
                        }
                        console.log(_res)
                    })
                } catch (error) {
                    console.log(error)
                }
            }
        }
        
    }
</script>

<style lang="less" scoped>
    .gameInfo{
        .formEdit{
            .editRow{
                display: flex;
                align-items: center;
                margin-bottom: 15px;
                .lab{
                    width: 90px;
                    text-align: right;
                    padding-right: 10px;
                }
                .edit{
                    flex: 1;
                }
            }
        }
    }
</style>