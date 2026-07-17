<template>
    <div class="adminGame">
        <GameInfo v-bind:gameInfo="gameInfo"></GameInfo>        
    </div>
</template>

<script>
    import GameInfo from './gameInfo.vue'
    export default {
        mounted(){
            var me = this;
            try {
                var sessionData = me.$eq.getAdminSessionData();
                me.gameInfo = sessionData.gameInfo;
            } catch (error) {
                console.log(error)
            }
        },
        components:{
            GameInfo 
        },
        data(){
            return{
                gameInfo:{}
            }
        }
    }
</script>

<style lang="less" scoped>
    .adminGame{
        width: 800px;
        background-color: #fff;
        padding: 15px;
        box-shadow: 0 0 10px #f0f0f0;
        margin: 0 auto;
    }
</style>