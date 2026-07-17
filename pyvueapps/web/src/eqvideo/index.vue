<template>
    <div class="pg index">
        <router-view class="indexPg"></router-view>
        <div class="nav">
            <div
                v-for="(item,index) in navs.items"  :key="index"
                :class="$route.path.indexOf(item.code)>=0?'navItem active':'navItem'"
                @click="onPickNav(index)"
            >
                <i :class="item.icon"></i> {{item.lab}} 
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        mounted(){
            var me = this;
            try {
                me.$eq.loadSessionUserInfo();
            } catch (error) {
                console.log(error);
            }
        },
        data(){
            return{
                navs:{
                    items:[
                        {code:"home" , lab:"主页" , icon:"fa fa-home"},
                        {code:"game" , lab:"赛事" , icon:"fa fa-server"},
                        {code:"about" , lab:"我的" , icon:"fa fa-user-o"},
                    ],
                    index:0
                }
            }
        },
        methods:{
            onPickNav(ind){
                var me = this;
                try {
                    me.navs.index = ind;
                    var url = "/index/" + me.navs.items[me.navs.index].code;
                    me.$router.push({
                        path: url
                    })
                } catch (error) {
                    console.log(error);
                }
            }
        }
    }
</script>

<style lang="less" scoped>
    @import url('../assets/comm/comm.less');
    .index{
        .nav{
            position: fixed;
            background-color: #fff;;
            bottom: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            .navItem{
                height: 40px;
                line-height: 40px;
                flex: 1; 
                
            }
            .navItem.active{
                border-top: 1px solid #0077fe;
                color: #0077fe;
                font-weight: bold;
            }
        }
    }
</style>