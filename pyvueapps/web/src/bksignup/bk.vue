<template>
    <div>
        bk test;

        <button @click="requireValid">request valid </button>

        <button @click="checkLogin">checkLogin </button>

        <ul>
            <li>

                <button @click="getUserData">getUserData </button>
                
            </li>
            <li>

                <button @click="createMember">create member </button>
                
            </li>
            <li>

                <button @click="query">query DB</button>
                
            </li>
        </ul>
    </div>
</template>

<script>
var bk = require('./bkapi').bkapi;
    export default {
        mounted(){
            var me = this;
            console.log('bk signup test...');

            bk.getGameData().then(gameData=>{
                console.log('-----------  gamedata ---------');
                console.log( bk.gameData );

                return bk.getSession()
            }).then( sessionResult =>{
                console.log(' ---------  session ----')
                var isLogin = bk.isLogin()
                console.log( bk.session , isLogin) 
            })
        },
        data(){
            return{
                tel:"18601386396"
            }
        },
        methods:{
            requireValid(){
                var me = this; 
                bk.requestSessionValid( me.tel).then(_res=>{
                        console.log('--------  get valid ---------')
                        console.log(_res)
                })

            },
            checkLogin(){
                var me = this; 
                bk.checkLogin( "652580").then(_res=>{
                        console.log('--------  get valid ---------')
                        console.log(_res)
                })

            },
            getUserData(){
                var me = this; 
                bk.updateUserData(true).then(_res=>{
                        console.log('--------  update userData ---------')
                        console.log(_res); 
                })

            },
            createMember(){
                var me = this; 
                var teamKey = '8c849a1c27a248a2a77f30bbda8668c4'
                //functionCode, genderCode, idTypeCode, idCode, memTel, photoImg, idImgList
                bk.memberCreate(
                    teamKey ,
                    '李江明' ,
                    '01',
                    'M',
                    '01',
                    '32040219800101001X',
                    '13813500000',
                    '',
                    ''
                ).then(_res=>{
                        console.log('--------  create member ---------')
                        console.log(_res); 
                })

            },
            query(){
                var me = this; 
                var dbKey = "sysData/admin/signup/team"
                var dbPs={
                    mem:"小"
                };
                bk.query(dbKey , dbPs).then(_res=>{
                    console.log('------------query ----------')
                    console.log(_res)
                })
            }
        }
        
    }
</script>

<style lang="scss" scoped>

</style>
