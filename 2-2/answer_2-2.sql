SELECT 
	A.MENU_NM AS CURRENT_MENU
	,B.MENU_NM AS PRIVIOUS_MENU
	,COUNT(A.MENU_NM) AS CNT
	,TRUNCATE((COUNT(A.MENU_NM) / SUM(COUNT(A.MENU_NM))OVER(PARTITION BY A.MENU_NM)),2) AS RATE -- 소수 셋째자리 이하 버림(소수 둘째자리까지)
FROM 
	(
	SELECT 
		ROW_NUMBER() OVER(ORDER BY LOG_ID ) AS ORD_NO -- LOG_ID 대신 고유 인덱스 재배치(결측배제) 
		,USR_NO 
		,MENU_NM
		,LOG_TKTM 
	FROM 
		KAKAOBANK.MENU_LOG
	ORDER BY 
		USR_NO,LOG_TKTM 
	) A -- 집계 기준 메뉴 리스트 추출 
LEFT JOIN
	(
	SELECT 
		ROW_NUMBER() OVER(ORDER BY LOG_ID ) +1 AS ORD_NO -- LOG_ID 대신 고유 인덱스 재배치(결측배제) 
		,USR_NO 
		,MENU_NM
		,LOG_TKTM
	FROM 
		KAKAOBANK.MENU_LOG
	ORDER BY 
		USR_NO, LOG_TKTM 
	) B ON A.ORD_NO = B.ORD_NO AND A.USR_NO = B.USR_NO  -- 집계기준 대상 테이블 대비 직전 메뉴 추출
WHERE 
	1=1
	AND B.ORD_NO IS NOT NULL
GROUP BY 
	A.MENU_NM
	,B.MENU_NM
ORDER BY 
	A.MENU_NM ASC
	,B.MENU_NM ASC
	,CNT DESC
;
