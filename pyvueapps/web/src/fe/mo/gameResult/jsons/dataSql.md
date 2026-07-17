

数据结构

# 赛事信息  gameInfo
    gameId , gameCode , gameName , address , gameDesc , openDate , closeDate
select 
	g.F_SportID as gameId ,
	g.F_SportCode as gameCode ,
	gd.F_SportShortName as gameName ,
	(
		select top 1 vd.F_VenueShortName From TC_Venue v join TC_Venue_Des vd on vd.F_VenueID = v.F_VenueID
	) as [address],
	convert(varchar(10), g.F_OpenDate, 121) as openDate,
	convert(varchar(10), g.F_CloseDate, 121) as closeDate ,
	g.F_DisciplineCode as gameDesc 
from TS_Sport g
join TS_Sport_Des gd on g.F_SportID = gd.F_SportID and gd.F_LanguageCode = 'CHN' 
for Json path ,  without_array_wrapper 

# 字典 
## 剑种  dictWeapon( code , name )
select * from  (
	select 'F' as code , N'花剑'   as [name] union 
	select 'E' as code , N'重剑'   as [name] union 
	select 'S' as code , N'佩剑'   as [name] 
) a for json path  
## 性别  dictGender( code , name )
select * from  (
	select 'M' as code , N'男子'   as [name] union 
	select 'W' as code , N'女子'   as [name] 
) a for json path  
## 类别  dictType( code , name )
select * from  (
	select 'T' as code , N'团体赛'   as [name] union 
	select 'I' as code , N'个人赛'   as [name] 
) a for json path  

# 比赛单项 eventInfo
    eventId , eventCode , eventName , eventOrder ,
    weaponCode , typeCode , genderCode ,  categoryCode ,
    eventTime , hasPool
select 
	e.F_EventID as eventId ,
	e.F_XMLID as eventCode ,
	e.F_Order as eventOrder ,
	ed.F_EventShortName ,
	s.F_GenderCode  as genderCode ,
	e.F_WeaponType as weaponCode ,
	e.F_Category as categoryCode ,
	case 
		when e.F_PlayerRegTypeID = 1 then 'I' 
		when e.F_PlayerRegTypeID = 3 then 'T' 
		else ''
	end as typeCode,
	convert(varchar(10), F_OpenDate , 121) as openDate ,
	convert(varchar(8) ,F_OpenDate , 108) as openTime 
	, case when isnull( poolPhase.poolPhaseCount,0)>0 then 1 else 0 end as hasPool
	,*
from TS_Event  e join TS_Event_Des ed on ed.F_LanguageCode='CHN' and e.F_EventID = ed.F_EventID
join TC_Sex s on s.F_SexCode = e.F_SexCode 
left join (
	select F_EventID , count(*) as poolPhaseCount from TS_Phase where F_PhaseType = 1 and F_Level>0 group by F_EventID 
) poolPhase on poolPhase.F_EventID = e.F_EventID  

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

select 
	e.F_EventID as eventId , e.F_XMLID as eventCode , ed.F_EventShortName as eventName ,
	p.F_PhaseID as phaseId , p.F_Order as phaseOrder , p.F_PhaseCode as phaseCode , pd.F_PhaseShortName as phaseName 
	,p.F_Level as phaseLevel 
	,p.F_PhaseType as phaseType  
	,isnull( m.matchCount ,0) as matchCount 
	, case 
		when (p.F_Level=1 and p.F_PhaseType=3) or (p.F_Level=1 and p.F_PhaseType=5) then isnull(
			(select top 1  np.F_PhaseID  From TS_Phase np where np.F_EventID = p.F_EventID and p.F_Order + 1 = np.F_Order and np.F_Level = p.F_Level and np.F_PhaseType = p.F_PhaseType) ,
			0
		) 
		else 0
	end as nextPhaseId 
from TS_Phase p 
join TS_Phase_Des pd on p.F_PhaseID = pd.F_PhaseID and pd.F_LanguageCode = 'CHN'
join TS_Event e on e.F_EventID = p.F_EventID
join TS_Event_Des ed on ed.F_EventID = e.F_EventID and ed.F_LanguageCode = 'CHN' 
left join (
	select F_PhaseID , count(*) as matchCount from TS_Match group by F_PhaseID
) m on m.F_PhaseID = p.F_PhaseID


# 个人赛参赛名单 startList  startList_<eventCode>
    athOrder , orgCode ,  orgName , athCode , athName , points , teamCode 
select 
	e.F_EventID as eventId , e.F_XMLID as eventCode , 
	isnull( i.F_IniDisPos ,0) as athOrder ,
	d.F_DelegationCode as orgCode ,
	dd.F_DelegationShortName as orgName ,
	r.F_RegisterCode as athCode ,
	rd.F_PrintLongName as athName  ,
	i.F_InscriptionRank as pointRank
from TR_Inscription i 
join TR_Register r on r.F_RegisterID = i.F_RegisterID
join TR_Register_Des rd on r.F_RegisterID = rd.F_RegisterID  and rd.F_LanguageCode = 'CHN'
join TS_Event e on e.F_EventID = i.F_EventID and e.F_PlayerRegTypeID = 1
join TC_Delegation  d  on d.F_DelegationID = r.F_DelegationID  
join TC_Delegation_Des dd on dd.F_DelegationID = r.F_DelegationID  and dd.F_LanguageCode = 'CHN'
order by  e.F_EventCode ,  athOrder

# 团体赛参赛名单 startListTeam startListTeam_<eventCode>
    teamnOrder , teamCode , teamName 
select 
	e.F_EventID as eventId , e.F_XMLID as eventCode , 
	isnull( i.F_IniDisPos ,0) as teamOrder ,
	r.F_RegisterCode as teamCode ,
	rd.F_PrintLongName as teamName  
from TR_Inscription i 
join TR_Register r on r.F_RegisterID = i.F_RegisterID
join TR_Register_Des rd on r.F_RegisterID = rd.F_RegisterID  and rd.F_LanguageCode = 'CHN'
join TS_Event e on e.F_EventID = i.F_EventID and e.F_PlayerRegTypeID = 3
join TC_Delegation_Des dd on dd.F_DelegationID = r.F_DelegationID  and dd.F_LanguageCode = 'CHN'
# 团体参赛成员 startList  startListMember_<eventCode>
    athId , orgCode ,  orgName , athCode , athName , teamCode 
select 
	t.F_RegisterCode as teamCode ,
	r.F_RegisterID as athId ,
	r.F_RegisterCode as athCode ,
	rd.F_PrintLongName as athName ,
	d.F_DelegationCode as orgCode ,
	dd.F_DelegationShortName as orgName 
from TR_Inscription i  
join TR_Register t on t.F_RegisterID = i.F_RegisterID and t.F_RegTypeID = 3
join TR_Register_Des td on td.F_RegisterID = t.F_RegisterID and td.F_LanguageCode = 'CHN'
join TR_Register_Member m on i.F_RegisterID = m.F_RegisterID 
join TR_Register r on r.F_RegisterID = m.F_MemberRegisterID and r.F_RegTypeID = 1 
join TR_Register_Des rd on rd.F_RegisterID = r.F_RegisterID and rd.F_LanguageCode ='CHN'
join TC_Delegation d on d.F_DelegationID = t.F_DelegationID
join TC_Delegation_Des dd on d.F_DelegationID = dd.F_DelegationID and dd.F_LanguageCode ='CHN'

# 小组赛
## 分组 poolList poolList_<eventCode>
    poolOrder , poolCode , poolName , startTime , pist(剑道)
select 
	p.F_PhaseID as phaseId ,
	p.F_Order as phaseOrder ,
	p.F_PhaseCode as phaseCode ,
	pd.F_PhaseShortName as phaseName ,
	isnull(convert( varchar(8) , p.F_StartTime , 108) ,'') as startTime ,
	isnull(cd.F_CourtShortName,'') as pist

from TS_Phase p 
join TS_Phase_Des pd on pd.F_PhaseID = p.F_PhaseID and pd.F_LanguageCode='CHN' and p.F_Level = 1 and p.F_PhaseType = 1
left join TC_Court c on p.F_CourtID= c.F_CourtID
left join TC_Court_Des cd on c.F_CourtID = cd.F_CourtID and cd.F_LanguageCode ='CHN'
order by p.F_EventID , p.F_Order

## 分组对阵(斜线表) poolMatch_<eventCode>
    poolCode , matchOrder , orgName , athName , c1, c2 ,c3 ,c4 ,c5, c6, c7, c8, c9, c10 , indexWin , diff , hs , hr , size(7)
select
	pr.F_PhaseID as phaseId ,
	p.F_PhaseCode as poolCode ,
	pr.F_PhasePosition as matchOrder ,
	dd.F_DelegationShortName ,
	rd.F_PrintLongName ,
	pr.F_Result1 as r1 ,
	pr.F_Result2 as r2 ,
	pr.F_Result3 as r3 ,
	pr.F_Result4 as r4 ,
	pr.F_Result5 as r5 ,
	pr.F_Result6 as r6 ,
	pr.F_Result7 as r7 ,
	pr.F_IndexChar as indexWin ,
	pr.F_Diff as diff ,
	pr.F_TcGive as hs ,
	pr.F_TcReceive hr 
from TS_Phase_Result pr
join TS_Phase p on p.F_PhaseID = pr.F_PhaseID  and p.F_Level =1 
join TR_Register r on r.F_RegisterID = pr.F_RegisterID
join TR_Register_Des rd on rd.F_RegisterID = r.F_RegisterID and rd.F_LanguageCode='CHN'
join TC_Delegation d on d.F_DelegationID = r.F_DelegationID
join TC_Delegation_Des dd on dd.F_DelegationID = d.F_DelegationID and dd.F_LanguageCode='CHN'
order by p.F_PhaseID , pr.F_PhasePosition




## 小组赛总排名 poolRank_<eventCode>
    displayOrder , poolRank , athCode , athName , orgName , poolName , m , vm , diff , td , tr , qualify
select	
	e.F_EventID as eventId ,
	e.F_XMLID as eventCode ,
	e.F_PoolQualifyNo as eventPoolQualifyNo,
	poolRank.rankOrder as displayOrder ,
	poolRank.poolRank as poolRank  ,
	r.F_RegisterCode as athCode , 
	dd.F_DelegationShortName ,
	rd.F_PrintLongName , 
	pr.F_MatchCount as m  , 
	pr.F_IndexChar as indexWin ,
	pr.F_Diff as diff ,
	pr.F_TcGive as hs ,
	pr.F_TcReceive hr ,
	case 
		when isnull(poolRank.poolRank,0)>0 and isnull(poolRank.poolRank,0) <=e.F_PoolQualifyNo  then 1 
		else 0 
	end as qualify
from TS_Phase_Result pr
join TS_Phase p on p.F_PhaseID = pr.F_PhaseID   and p.F_Level = 1 
join TS_Event e on e.F_EventID = p.F_EventID
join TR_Register r on r.F_RegisterID = pr.F_RegisterID 
join(
	select F_RegisterID as regId , a.F_PhaseDisplayPos as rankOrder , a.F_PhaseRank as poolRank , p.F_EventID as eventId  from TS_Phase_Result a join TS_Phase p on p.F_PhaseID = a.F_PhaseID where p.F_Level = 0 
) poolRank on poolRank.regId = r.F_RegisterID and poolRank.eventId = e.F_EventID
join TR_Register_Des rd on rd.F_RegisterID = r.F_RegisterID and rd.F_LanguageCode='CHN'
join TC_Delegation d on d.F_DelegationID = r.F_DelegationID
join TC_Delegation_Des dd on dd.F_DelegationID = d.F_DelegationID and dd.F_LanguageCode='CHN' 
order by eventId ,  isnull(poolRank.poolRank,999999), isnull(poolRank.rankOrder,999999)



# 对阵图
## 比赛场次 match_<eventCode>
phaseCode , matchOrder , matchId 
## 参赛人员及得分 matchResult_<eventCode> 
matchId , haOrder(1-主队 ， 2-客队) , regName , orgName ,  win  , score 
select 
	m.F_PhaseID as phaseId ,
	m.F_Order as matchOrder ,
	m.F_MatchCode as matchCode , 

	hmr.F_RegisterID as homeRegId ,
	hrd.F_PrintShortName as homeAthName,
	hdd.F_DelegationShortName as homeOrgName,
	hmr.F_WinPoints as homwPoints ,
	hmr.F_WinSets as homeWinSets,

	amr.F_RegisterID as awayRegId ,
	ard.F_PrintShortName as awayAthName,
	[add].F_DelegationShortName as awayOrgName ,
	amr.F_WinPoints as awayPoints ,
	amr.F_WinSets as awayWinSets
from TS_Match m 
-- home 
left join TS_Match_Result hmr on hmr.F_HomeAway = 1 and hmr.F_MatchID = m.F_MatchID
left join TR_Register hr on hr.F_RegisterID = hmr.F_RegisterID
left join TR_Register_Des hrd on hr.F_RegisterID = hrd.F_RegisterID and hrd.F_LanguageCode ='CHN' 
left join TC_Delegation hd on hd.F_DelegationID = hr.F_DelegationID
left join TC_Delegation_Des hdd on hdd.F_DelegationID = hd.F_DelegationID and hdd.F_LanguageCode = 'CHN'
-- away 
left join TS_Match_Result amr on amr.F_HomeAway = 2 and amr.F_MatchID = m.F_MatchID
left join TR_Register ar on ar.F_RegisterID = amr.F_RegisterID
left join TR_Register_Des ard on ar.F_RegisterID = ard.F_RegisterID and ard.F_LanguageCode ='CHN' 
left join TC_Delegation ad on ad.F_DelegationID = ar.F_DelegationID
left join TC_Delegation_Des [add] on [add].F_DelegationID = ad.F_DelegationID and [add].F_LanguageCode = 'CHN'

order by m.F_PhaseID , m.F_Order 

# 总排名 eventRank_<eventCod>
displayOrder , rank , medalCode , regName , orgName , irm  , teamMember



