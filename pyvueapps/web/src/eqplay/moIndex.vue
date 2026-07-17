<template>
    <div class="moIndex">
        <div class="navs">
            <ul class="lstNav">
                <li
                    v-for="(item,index) in navs.items" :key="index"
                    :class="$route.path.indexOf(item.code)>0?'active':''"
                    @click="acNav(item.code)"
                >
                    <i :class="item.icon"></i> {{item.lab}}
                </li>
            </ul>
        </div>
        <router-view  class="mainPage"></router-view>
    </div>
</template>

<script>
    export default {
        mounted(){
                var me = this;
                try {
                    document.title="马术考级视频系统"
                } catch (error) {
                    console.log(error)
                }
        },
        data(){
            return{
                navs:{
                    items:[
                        {code:"live" , lab:"直播", icon:"fa fa-rss"} ,
                        {code:"vod" , lab:"回放", icon:"fa fa-camera"} ,
                    ]                    
                }
            }
        },
        methods:{
            acNav(code){
                var me = this;
                try {
                    var url = "/eqmo/"+code;
                    me.$router.push({
                        path: url
                    })
                } catch (error) {
                    console.log(error)
                }
            }
        }
        
    }
</script>

<style lang="less" scoped>
    .moIndex{
        .navs{
            position: fixed;
            bottom: 0;
            width: 100%;
            box-shadow: 0 0 10px 0 #ddd;
            background-color: #fff;
            z-index: 999;
            .lstNav{
                display: flex;
                align-items: center;
                li{
                    flex: 1;
                    height: 40px;
                    line-height: 40px;
                }
                li.active{
                    border-top: 1px solid #0077fe;
                    color: #0077fe;
                }
            }
        }
    }

    .mainPage{
        padding-bottom: 55px;
    }
</style>