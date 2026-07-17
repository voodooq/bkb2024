<template>
    <div  class="results">
        <div class="resultToolbar">
            <div class="filter">
                <div class="item">
                    <ul class="lstFilter">
                        <li
                            v-for="(item,index) in resInfo.filters.events.items" :key="index"
                            :class="resInfo.filters.events.index == index?'active':''"
                            @click="resInfo.filters.events.index = index"
                        >
                            {{item.eventName}}
                        </li>
                    </ul>
                </div>
                <div class="item">
                    <ul class="lstFilter">
                        <li
                            v-for="(item,index) in resInfo.filters.phases.items" :key="index"
                            :class="resInfo.filters.phases.index == index?'active':''"
                            @click="resInfo.filters.phases.index = index"
                        >
                            {{item.phaseName}}
                        </li>
                    </ul>
                </div>
            </div>
            <div class="search">
                <el-input
                    size="small"
                    placeholder="请输入内容"
                    suffix-icon="el-icon-search"
                    v-model="resInfo.search.searchText">
                </el-input>
            </div>
            <div class="acs">
                <div class="item">
                    <el-button size="small" type="success" ><i class="fa fa-refresh"></i> 刷新</el-button>
                </div>
                <div class="item">
                    <el-button size="small" type="primary" ><i class="fa fa-download"></i> 导入</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name:"Results",
        props:{
            resInfo:{
                filters:{
                    events:{
                        items:[
                            {eventCode:"E1", eventName:"盛装舞步"} ,
                            {eventCode:"E2", eventName:"场地障碍"} ,
                        ],
                        index:0
                    },
                    phases:{
                        items:[
                            {phaseCode:"J1", phaseName:"初一"} ,
                            {phaseCode:"J2", phaseName:"初二"} ,
                            {phaseCode:"J3", phaseName:"初三"} ,
                            {phaseCode:"S1", phaseName:"中一"} ,
                            {phaseCode:"S2", phaseName:"中二"} ,
                            {phaseCode:"S3", phaseName:"中三"} ,
                        ],
                        index:0
                    },
                },
                search:{
                    searchText:""
                }
            }
        }
    }
</script>

<style lang="less" scoped>
    .results{
        .resultToolbar{
            display: flex;
            justify-content: space-between;
            align-content: center;
            
            .filter{
                display: flex;
                align-content: center;
                .item{
                    padding: 0 5px;
                    ul.lstFilter{
                        display: flex;
                        border:1px solid #0077fe;
                        color: #0077fe;
                        li{
                            height: 32px ;line-height: 32px;
                            padding: 0 5px;
                        }
                        li:hover{
                            cursor: pointer;
                        }
                        li.active{
                            background-color: #0077fe;
                            color: #fff;
                        }
                    }
                }
            }

            .acs{
                display: flex;
                align-items: center;
                .item{
                    margin-left: 10px;
                }
            }
        }
    }
</style>