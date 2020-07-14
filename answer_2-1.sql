-- explain
select distinct
	main.day
	,main.menu_nm
	,case 
		when sub.cnt is not null then sub.cnt 
		when sub.cnt is null then '-'
		end as cnt
from 
	(
	select distinct 
		dayname(cast(LOG_TKTM as date)) as day
		,b.menu_nm
	from 
		KAKAOBANK.MENU_LOG a 
	cross join 
		(
		select distinct
			menu_nm 
		from 
			KAKAOBANK.MENU_LOG 
		where 
			menu_nm not in ('login','logout')
		)b
	) main 
left join 
	(
	select 
		dayname(cast(LOG_TKTM as date)) as day
		,menu_nm
		,count(menu_nm) as cnt 
	from 
		KAKAOBANK.MENU_LOG ml 
	where
		1=1
		and ml.MENU_NM not in('login','logout')
	group by 
		day
		,menu_nm
	) sub on main.menu_nm = sub.menu_nm and main.day = sub.day
order by 
     CASE
          WHEN main.day = 'Monday' THEN 1
          WHEN main.day = 'Tuesday' THEN 2
          WHEN main.day = 'Wednesday' THEN 3
          WHEN main.day = 'Thursday' THEN 4
          WHEN main.day = 'Friday' THEN 5
          WHEN main.day = 'Saturday' THEN 6
          WHEN main.day = 'Sunday' THEN 7
     END ASC
     ,cnt desc
     ,main.menu_nm asc
;	








