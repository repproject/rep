SELECT * FROM kadm_com_cd_dtl
;
SELECT * FROM KADM_JOB
;
SELECT * FROM KADM_JOB_ACT
;
SELECT * FROM KADM_ACT
;
SELECT * FROM KADM_ACT_FUNC
;
SELECT * FROM KADM_FUNC
;
SELECT * FROM KMIG_KB_REGN
;

/* 작업관련 전체조회 */
SELECT F.FUNC_ID
FROM KADM_JOB       J
   , KADM_JOB_ACT  JA
   , KADM_ACT       A
   , KADM_ACT_FUNC AF
   , KADM_FUNC      F
WHERE J.JOB_ID = JA.JOB_ID   
AND JA.ACT_ID = A.ACT_ID

AND A.ACT_ID = AF.ACT_ID
AND AF.FUNC_ID = F.FUNC_ID
AND J.JOB_ID = 'KBDC004'
ORDER BY JA.EXEC_SEQ ASC, AF.EXEC_SEQ ASC

;

/* 지역, 단지명, 형별 조회 */
select e.KB_REGN_NM, d.kb_regn_nm, c.kb_regn_nm, a.CMPX_IDF_ID, b.cmpx_idf_nm, a.HOUSE_TYP_NM, p.STD_YYMM, p.UP_AVG_PRC, p.GNRL_AVG_PRC, p.DOWN_AVG_PRC, p.UP_JS_AVG_PRC, p.GNRL_JS_AVG_PRC, p.DOWN_JS_AVG_PRC
from kmig_kb_cmpx_typ a
left outer join kmig_kb_cmpx b
on a.cmpx_idf_id = b.cmpx_idf_id
left outer join kmig_kb_regn c
on b.KB_REGN_CD = c.kb_regn_cd
left outer join kmig_kb_regn d
on c.UP_KB_REGN_CD = d.kb_regn_cd
left outer join kmig_kb_regn e
on d.up_kb_regn_cd = e.kb_regn_cd
left outer join KMIG_KB_CMPX_TYP_MON_PRC p
on a.CMPX_IDF_ID = p.cmpx_idf_id
and a.HOUSE_TYP_SEQ = p.house_typ_seq
#where CMPX_IDF_NM like '%삼신(6차)%'
;

select distinct cmpx_idf_id from KMIG_KB_CMPX_TYP_MON_PRC
where gnrl_js_avg_prc = 0
;
where cmpx_idf_id = 'KBA000058'
order by house_typ_seq, std_yymm desc
;
select * from kmig_kb_cmpx_typ
where cmpx_idf_id = 'KBA000058'
;
update
#select * from 
kmig_kb_cmpx_typ_mon_prc
set up_avg_prc = 'null'
where cmpx_idf_id = 'KBA000001'
and HOUSE_TYP_SEQ = '1'
and std_yymm = '200306'
;

select count(*) from KMIG_KB_CMPX_TYP_MON_PRC
;

/* 네이버 단지 조회 */
SELECT * 
FROM KMIG_NV_CMPX NV #31337 - 20(지역단지중복) = 31317
/*INNER JOIN KRED_LEGL_REGN LR3
ON NV.GOV_LEGL_DONG_CD = LR3.LEGL_REGN_CD
INNER JOIN KRED_LEGL_REGN LR2
ON LR2.LEGL_REGN_CD = LR3.UP_LEGL_REGN_CD
INNER JOIN KRED_LEGL_REGN LR1
ON LR1.LEGL_REGN_CD = LR2.UP_LEGL_REGN_CD*/
WHERE 1=1
AND NV_CMPX_ID = '1000000004'
#AND NV.NV_CMPX_NM = '미진동백'
#AND LR3.LEGL_REGN_NM = '작전동'
;

SELECT * FROM KRED_LEGL_REGN
