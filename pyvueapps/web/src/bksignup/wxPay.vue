<template>
    <div class="wxPay">
        <div class="apiItem">
            <div class="lab">dirUrl</div> 
            <div class="result">
                <el-input v-model="dirUrl" size = "small"></el-input>
            </div>
        </div>
        <div class="apiItem">
            <div class="lab">getOpenId</div>
            <div class="btn">
                <el-button type = "primary" @click="acGetOpenId">GetOpenId</el-button>
            </div>
            <div class="result">
                <el-input v-model="openIdResult" size = "small"></el-input>
            </div>
        </div>
        <div class="apiItem">
            <div class="lab">requestOrder</div>
            <div class="btn">
                <el-button type = "primary" @click="acRequestOrder">requestOrder</el-button>
            </div>
            <div class="result">
                <textarea v-model="orderResult" name="" id="" cols="30" rows="10"></textarea>
            </div>
        </div> 
    </div>
</template>

<script>
    const inf = require('./bkapi')
    console.log(inf)
    export default {
        mounted(){
            var me = this;
            try {
                console.log(me.$route)
                me.$nextTick().then(_=>{
                    return inf.wxpay.getOpenId()
                }).then(_openIdRes=>{       
                    me.dirUrl = inf.wxpay.config.wx.dirUrl;             
                    console.log(_openIdRes)
                })
            } catch (error) {
                console.log(error)
            }
        },
        data(){
            return{
                dirUrl:"",
                openIdResult:"",
                orderResult:""
            }
        },
        methods:{
            acGetOpenId(){

            },
            acRequestOrder(){

            }
        }
        
    }
</script>

<style lang="scss" scoped>

</style>