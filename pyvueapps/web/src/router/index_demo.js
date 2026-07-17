import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'


import Login from '../eqvideo/login'
import Index from '../eqvideo/index'
import eqHome from '../eqvideo/home'
import eqGame from '../eqvideo/game'
import eqAbout from '../eqvideo/about'
import eqGameVideos from '../eqvideo/gameVideos'
import GameVideos from '../eqvideo/gameVideos.vue'
import gameVideoPlay from '../eqvideo/video.vue'
import eqControl from '../eqvideo/control.vue'

import eqAdminLogin from '../eqvideoAdmin/adminLogin.vue'
import eqAdminIndex from '../eqvideoAdmin/adminIndex.vue'
import eqAdminGame from '../eqvideoAdmin/adminGame.vue'
import eqAdminResult from '../eqvideoAdmin/adminResult.vue'
import eqAdminVideo from '../eqvideoAdmin/adminVideo.vue'

import eqMo from '../eqplay/moIndex.vue'
import eqMoLive from '../eqplay/moLive.vue'
import eqMoVod from '../eqplay/moVod.vue'
import eqMoPlayVod from '../eqplay/moPlayVod.vue'
import eqLed from '../eqplay/ledLive.vue'

import go from '../gojsapp/go.vue'


import feMo from '../fe/mo/gameResult/index.vue'
import feMoEvent from '../fe/mo/gameResult/eventPage.vue'


import bk from '../bksignup/bktest.vue'
import bk1 from '../bksignup/bk.vue'
import wxPay from '../bksignup/wxPay.vue'

Vue.use(Router)
export default new Router({
    //mode: "history",
    routes: [{
        path: '/',
        name: 'HelloWorld',
        component: HelloWorld
    }, {
        path: '/go',
        name: 'Go',
        component: go
    }, {
        path: '/login',
        component: Login
    }, {
        path: '/index',
        component: Index,
        children: [{
                path: "home",
                component: eqHome
            },
            {
                path: "game",
                component: eqGame
            },
            {
                path: "about",
                component: eqAbout
            },
        ]
    }, {
        path: '/gameVideos',
        component: GameVideos
    }, {
        path: '/video',
        component: gameVideoPlay
    }, {
        path: '/control',
        component: eqControl
    }, {
        path: "/eqAdminLogin",
        component: eqAdminLogin

    }, {
        path: "/eqAdminIndex",
        component: eqAdminIndex,
        children: [{
                path: "game",
                component: eqAdminGame
            },
            {
                path: "result",
                component: eqAdminResult
            },
            {
                path: "video",
                component: eqAdminVideo
            }
        ]

    }, {
        path: "/eqmo",
        component: eqMo,
        children: [{
                path: "live",
                component: eqMoLive
            },
            {
                path: "vod",
                component: eqMoVod
            }
        ]

    }, {
        path: "/eqmoVod",
        component: eqMoPlayVod
    }, {
        path: "/eqLed",
        component: eqLed
    }, { //-----------------------------  fe mo publish -----------------
        path: "/femo",
        component: feMo
    }, {
        path: "/femoEvent",
        component: feMoEvent
    }, { //-----------------------------  bksignup test -----------------
        path: "/bk",
        component: bk
    }, {
        path: "/bk1",
        component: bk1
    }, {
        path: "/wxpay",
        component: wxPay
    }]
})