SELECT KR1.KB_REGN_NM, KR2.KB_REGN_NM, KR3.KB_REGN_NM, KC.CMPX_IDF_NM, KCT.HOUSE_TYP_NM, KCTMP.GNRL_AVG_PRC, KCTMP.GNRL_JS_AVG_PRC, 
FROM KMIG_KB_REGN KR1
INNER JOIN kmig_kb_regn KR2
ON KR1.KB_REGN_CD = KR2.UP_KB_REGN_CD
INNER JOIN kmig_kb_regn KR3
ON KR2.KB_REGN_CD = KR3.UP_KB_REGN_CD
INNER JOIN KMIG_KB_CMPX KC
ON KR3.KB_REGN_CD = KC.KB_REGN_CD
INNER JOIN KMIG_KB_CMPX_TYP KCT
ON KC.CMPX_IDF_ID = KCT.CMPX_IDF_ID
INNER JOIN KMIG_KB_CMPX_TYP_MON_PRC KCTMP
ON KCT.CMPX_IDF_ID = KCTMP.CMPX_IDF_ID
AND KCT.HOUSE_TYP_SEQ = KCTMP.HOUSE_TYP_SEQ
AND KCTMP.GNRL_AVG_PRC - KCTMP.GNRL_JS_AVG_PRC < 10000
AND KCTMP.STD_YYMM = '201711'
WHERE KR1.KB_REGN_CD = '010000'
ORDER BY GNRL_AVG_PRC DESC
;

SELECT *
FROM KMIG_KB_REGN KR1
   , kmig_kb_regn KR2
WHERE KR1.KB_REGN_CD = KR2.UP_KB_REGN_CD



;
SELECT *
FROM KMIG_KB_CMPX_TYP

;

SELECT COUNT(*)
FROM KMIG_KB_CMPX_TYP_MON_PRC
WHERE STD_YYMM = '201711'
;
SELECT *
FROM KMIG_KB_CMPX
#WHERE CMPX_IDF_ID = 'KBA000001'
WHERE CMPX_IDF_NM LIKE '%미진동백%'
;
SELECT * FROM KMIG_KB_CMPX_TYP_MON_PRC
WHERE CMPX_IDF_ID < 'KBA001000'
ORDER BY CMPX_IDF_ID ASC, HOUSE_TYP_SEQ ASC, STD_YYMM ASC 
;

SELECT NOW()
;
SELECT *
FROM KMIG_KB_CMPX_TYP


;

SELECT *
FROM KMIG_KB_CMPX
WHERE CMPX_IDF_ID IN (	SELECT CMPX_IDF_ID	FROM KMIG_KB_CMPX_TYP_MON_PRC	GROUP BY CMPX_IDF_ID	HAVING MAX(STD_YYMM) < '201711')    


;

SELECT *
FROM KADM_ACT_FUNC
;

SELECT *
FROM KADM_JOB


;

SELECT a.CMPX_IDF_ID, a.HOUSE_TYP_SEQ, b.KB_REGN_CD as SMALL_KB_REGN_CD FROM KMIG_KB_CMPX_TYP a, kmig_kb_cmpx b where a.cmpx_idf_id = b.cmpx_idf_id AND a.CMPX_IDF_ID NOT IN (SELECT CMPX_IDF_ID	FROM KMIG_KB_CMPX_TYP_MON_PRC	GROUP BY CMPX_IDF_ID	HAVING MAX(STD_YYMM) < '201711') ORDER BY CMPX_IDF_ID ASC, a.HOUSE_TYP_SEQ
;

/* 법정동 기준 네이버건물 진행 조회 */
SELECT (SELECT COUNT(*) FROM KRED_LEGL_REGN) 전체법정동건수
     , (SELECT COUNT(*) FROM KRED_LEGL_REGN WHERE LEGL_REGN_CD < (SELECT MAX(GOV_LEGL_DONG_CD) FROM KMIG_NV_CMPX)) 진행법정동건수
;
/* NVDC003 - 네이버 단지정보 갱신 */
SELECT (SELECT COUNT(*) FROM kmig_nv_cmpx) 전체네이버단지갯수
     , (SELECT COUNT(*) FROM KMIG_NV_CMPX WHERE CMPL_YYMM IS NOT NULL) 갱신된네이버단지갯수
;     
/* NVDC004 - 네이버 단지형 정보 */
SELECT (SELECT COUNT(*) FROM kmig_nv_cmpx) 전체네이버단지갯수
     , (SELECT COUNT(*) FROM KMIG_NV_CMPX WHERE NV_CMPX_ID IN (SELECT NV_CMPX_ID FROM KMIG_NV_CMPX_TYP)) 갱신된네이버단지갯수

;
/* KBDC006 - KB 단지 갱신 */
SELECT (SELECT COUNT(*) FROM KMIG_KB_REGN WHERE LV_CD = '3') 전체KB소지역갯수
     , (SELECT COUNT(*) FROM KMIG_KB_REGN WHERE LV_CD = '3' AND KB_REGN_CD IN (SELECT KB_REGN_CD FROM KMIG_KB_CMPX)) 단지존재KB소지역갯수
     , (SELECT COUNT(*) FROM KMIG_KB_REGN WHERE LV_CD = '3' AND KB_REGN_CD IN (SELECT KB_REGN_CD FROM KMIG_KB_CMPX WHERE TOT_HSHL_CNT IS NOT NULL)) 갱신된소지역갯수
;

select * from kmig_nv_cmpx
where NV_CMPX_ID = '13276'
;

SELECT * 
     