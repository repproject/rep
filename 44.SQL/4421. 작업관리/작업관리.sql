#작업기능실행기준 수행 이력 파악
select *
from (
	select exec_dtm, count(*)
    , SUM(CASE WHEN STD_EXEC_STAT_CD = 'T' THEN 1 ELSE 0 END) 호출건수
    , MAX(CASE WHEN STD_EXEC_STAT_CD = 'T' THEN STD_PARM1 ELSE '0' END) 최대건수 
    , MAX(CASE WHEN STD_EXEC_STAT_CD = 'R' THEN STD_PARM1 ELSE '0' END) 진행중PARM1
    , MIN(STD_PARM1) 최소PARM1
	from kadm_job_func_exec_strd
	where job_id = 'NVDC005'
	and act_id = 'NV_DC_SALE'
	and func_id = 'INS_NV_SALE'
	group by exec_dtm 
) a
order by a.exec_dtm desc    
;