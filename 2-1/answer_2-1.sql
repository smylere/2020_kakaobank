EXPLAIN
WITH TMP AS 
	(
	SELECT DISTINCT
		CORE.DAY_NAME
		,CORE.MENU_NM
	FROM
		(
		SELECT 
			DAYNAME(CAST(A.LOG_TKTM AS DATE)) AS DAY_NAME
			,B.MENU_NM
		FROM 
			KAKAOBANK.MENU_LOG A, 
			(
			SELECT DISTINCT
				MENU_NM 
			FROM 
				KAKAOBANK.MENU_LOG 
			WHERE 
				MENU_NM NOT IN ('login','logout')
			)B
		) CORE 																				-- 곱집합 메뉴명/날짜 별도 계산
	)
SELECT
	TMP.DAY_NAME
	,ROW_NUMBER() OVER(PARTITION BY TMP.DAY_NAME ORDER BY CNT DESC,TMP.MENU_NM ASC) RNK		-- RANK계산
	,CASE 
		WHEN SUB.CNT IS NOT NULL THEN TMP.MENU_NM
		WHEN SUB.CNT IS NULL THEN '-'
		END AS MENU_NM																		-- 메뉴명 체크(없을경우 '-')
	,CASE 
		WHEN SUB.CNT IS NOT NULL THEN SUB.CNT 
		WHEN SUB.CNT IS NULL THEN '-'
		END AS CNT																			-- 메뉴 카운트(없을경우 '-')
FROM 
	TMP 
LEFT JOIN
	(
	SELECT 
		DAYNAME(CAST(LOG_TKTM AS DATE)) AS DAY_NAME
		,MENU_NM
		,COUNT(MENU_NM) AS CNT 																-- 메뉴 진입 COUNT
	FROM 
		KAKAOBANK.MENU_LOG ML 
	WHERE
		1=1
		AND ML.MENU_NM NOT IN('login','logout')												-- LOGIN / LOGOUT 내역 제외
	GROUP BY 
		DAY_NAME
		,MENU_NM
	) SUB ON TMP.DAY_NAME = SUB.DAY_NAME AND TMP.MENU_NM = SUB.MENU_NM
ORDER BY
	CASE
		WHEN TMP.DAY_NAME = 'Monday' THEN 1
		WHEN TMP.DAY_NAME = 'Tuesday' THEN 2
		WHEN TMP.DAY_NAME = 'Wednesday' THEN 3
		WHEN TMP.DAY_NAME = 'Thursday' THEN 4
		WHEN TMP.DAY_NAME = 'Friday' THEN 5
		WHEN TMP.DAY_NAME = 'Saturday' THEN 6
		WHEN TMP.DAY_NAME = 'Sunday' THEN 7
	END ASC
	,SUB.CNT DESC
	,TMP.MENU_NM ASC
;