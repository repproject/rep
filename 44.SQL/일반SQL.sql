select * from KMIG_BB_CMPX_TYP
where 1=1
#where bb_cmpx_id = 'A0000104'
and chg_dtm < now() - 2000000
;

select * from kmig_bb_cmpx_typ
order by CHG_DTM asc
;

update
#select * from 
KADM_PASI_CD_EXEC
set exec_parm_val = replace(exec_parm_val,"""",'')
#where pasi_id = 'BBMarketPrice'
;

select * from kadm_svc_pasi_item
#where pasi_id = 'BBMarketPrice'
;

select * from kmig_bb_cmpx_typ_mon_prc
order by chg_dtm desc
;

select * from kadm_job_act_exec
;
#delete
select * 
from kadm_tbl_col
where tbl_nm = 'kadm_job_schd_exec'
#and col_nm in ('exec_stat_cd')
;

select * from kadm_job_schd
;

use rep;