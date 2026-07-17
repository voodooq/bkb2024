

数据结构

# 赛事信息  gameInfo
    gameId , gameCode , gameName , address , gameDesc , openDate , closeDate
# 字典 
## 剑种  dictWeapon( code , name )
## 性别  dictGender( code , name )
## 类别  dictType( code , name )

# 比赛单项 eventInfo
    eventId , eventCode , eventName , eventOrder ,
    weaponCode , typeCode , genderCode ,  catoryCode ,
    eventTime 
# 比赛阶段 phase
    /*
        phaseType:
            startList   参赛名单
            poolMatch   小组赛对阵表
            poolRank    小组赛排名
            matchDual-1   对阵图-有晋级
            matchDual-2   对阵图-无晋级
            eventRank   项目总排名
    */
    phaseOrder , phaseCode , phaseType , phaseId , nextPhaseCode , matchCount

# 参赛名单 startList  startList_<eventCode>
    athOrder , orgCode ,  orgName , athCode , athName , points , teamCode 
# 参赛名单 startListTeam startListTeam_<eventCode>
    teamnOrder , teamCode , teamName 

# 小组赛
## 分组 poolList poolList_<eventCode>
    poolOrder , poolCode , poolName , startTime , pist(剑道)
## 分组对阵(斜线表) poolMatch_<eventCode>
    poolCode , matchOrder , orgName , athName , c1, c2 ,c3 ,c4 ,c5, c6, c7, c8, c9, c10 , indexWin , diff , hs , size(7)
## 小组赛总排名 poolRank_<eventCode>
    displayOrder , poolRank , athCode , athName , orgName , poolName , m , vm , diff , td , tr , qualify

# 对阵图
## 比赛场次 match_<eventCode>
phaseCode , matchOrder , matchId 
## 参赛人员及得分 matchResult_<eventCode> 
matchId , haOrder(1-主队 ， 2-客队) , regName , orgName ,  win  , score 


# 总排名 eventRank_<eventCod>
displayOrder , rank , medalCode , regName , orgName , irm  , teamMember



