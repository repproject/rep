select count(*) from kred_nv_cmpx; #55201
select count(*) from kred_apt_deal_cmpx; #42567
select * from kred_nv_cmpx;
select * from kred_apt_Deal_cmpx;
truncate KRED_KEY_MAPP_CMPX;
#A) 지번기준 1:1매핑 26679/42567 62%
INSERT INTO KRED_KEY_MAPP_CMPX
#select count(*)
select NC.NV_CMPX_ID,  ADC.REAL_DEAL_CMPX_ID, 'A', 1000000001, NOW(), 1000000001, NOW()
from kred_apt_deal_cmpx adc
inner join kred_nv_cmpx nc
on adc.legl_dong_cd = nc.legl_dong_cd
and replace(adc.hnum,' ','') = replace(nc.bas_addr,' ','')
where adc.real_deal_cmpx_id in (
	select adc.real_deal_cmpx_id
	from kred_apt_deal_cmpx adc
	inner join kred_nv_cmpx nc
	on adc.legl_dong_cd = nc.legl_dong_cd
	and replace(adc.hnum,' ','') = replace(nc.bas_addr,' ','')
	group by adc.real_deal_cmpx_id
	having count(*) = 1
)
and nc.nv_cmpx_id in (
	select nc.nv_cmpx_id
	from kred_apt_deal_cmpx adc
	inner join kred_nv_cmpx nc
	on adc.legl_dong_cd = nc.legl_dong_cd
	and replace(adc.hnum,' ','') = replace(nc.bas_addr,' ','')
	group by nc.nv_cmpx_id
	having count(*) = 1
)
;
#B) 지번기준 1:1(아파트,재건축) 2892
# 26679 + 2892 = 29560/42567 =  69%
#select * from (
	INSERT INTO KRED_KEY_MAPP_CMPX
	select NC.NV_CMPX_ID, ADC.REAL_DEAL_CMPX_ID,  'B', 1000000001 reg_user_id, NOW() reg_dtm, 1000000001 chg_user_id, NOW() chg_dtm
	#select count(*)
	#select *
	from kred_apt_deal_cmpx adc
	inner join kred_nv_cmpx nc
	on adc.legl_dong_cd = nc.legl_dong_cd
	and replace(adc.hnum,' ','') = replace(nc.bas_addr,' ','')
	and nc.nv_cmpx_id in (
		select nc.nv_cmpx_id
		from kred_apt_deal_cmpx adc
		inner join kred_nv_cmpx nc
		on adc.legl_dong_cd = nc.legl_dong_cd
		and replace(adc.hnum,' ','') = replace(nc.bas_addr,' ','')
		and nc.nv_cmpx_knd in ('APT','JGC')
		group by nc.nv_cmpx_id
		having count(*) = 1
	)
    and nc.nv_Cmpx_id not in  (
		select kmc.nv_cmpx_id
		from KRED_KEY_MAPP_CMPX KMC
	)
	where adc.real_deal_cmpx_id in (
		select adc.real_deal_cmpx_id
		from kred_apt_deal_cmpx adc
		inner join kred_nv_cmpx nc
		on adc.legl_dong_cd = nc.legl_dong_cd
		and replace(adc.hnum,' ','') = replace(nc.bas_addr,' ','')
		and nc.nv_cmpx_knd in ('APT','JGC')
		group by adc.real_deal_cmpx_id
		having count(*) = 1
	)
	and adc.real_deal_cmpx_id not in  (
		select kmc.real_Deal_cmpx_id
		from KRED_KEY_MAPP_CMPX KMC
	)
    #and adc.real_deal_cmpx_id = '39726'
    #and nc.nv_cmpx_id = '120782'
#order by adc.real_Deal_cmpx_id
#) a
#group by a.nv_cmpx_id 
#having count(*) > 1
;
#C) 부번호제외 1:1 단지 MIG 163개 
#29560 + 163 + 31 =  29754/42567 = 69.89%
INSERT INTO KRED_KEY_MAPP_CMPX
#select count(*)
select NC.NV_CMPX_ID,  ADC.REAL_DEAL_CMPX_ID, 'C', 1000000001, NOW(), 1000000001, NOW()
#select adc.real_Deal_cmpx_id 단지ID, adc.real_deal_cmpx_nm, adc.real_deal_cmpx_Seq_val 일련번호, adc.hnum, adc.legl_dong_orgl_num_cd 본번호, adc.legl_dong_vice_num_cd 부번호, adc.legl_dong_hnum_cd 번지코드
#     , nc.nv_cmpx_id, nc.nv_cmpx_knd, nc.bas_addr, nc.tot_hshl_cnt
from kred_apt_deal_cmpx adc
inner join kred_nv_cmpx nc
on adc.legl_dong_cd = nc.legl_dong_cd
and nc.nv_cmpx_knd in ('APT','JGC') #option
and trim(replace(SUBSTRING_INDEX(adc.hnum,'-',1),' ','')) = trim(replace(SUBSTRING_INDEX(nc.bas_addr,'-',1),' ',''))
where adc.real_deal_cmpx_id in (
	select adc.real_deal_cmpx_id
	from kred_apt_deal_cmpx adc
	inner join kred_nv_cmpx nc
	on adc.legl_dong_cd = nc.legl_dong_cd
    and nc.nv_cmpx_knd in ('APT','JGC') #option
	and trim(replace(SUBSTRING_INDEX(adc.hnum,'-',1),' ','')) = trim(replace(SUBSTRING_INDEX(nc.bas_addr,'-',1),' ',''))
	group by adc.real_deal_cmpx_id
	having count(*) = 1
)
and nc.nv_cmpx_id in (
	select nc2.nv_cmpx_id
	from kred_apt_deal_cmpx adc
	inner join kred_nv_cmpx nc2
	on adc.legl_dong_cd = nc2.legl_dong_cd    
    and nc2.nv_cmpx_knd in ('APT','JGC') #option
	and trim(replace(SUBSTRING_INDEX(adc.hnum,'-',1),' ','')) = trim(replace(SUBSTRING_INDEX(nc2.bas_addr,'-',1),' ',''))
	group by nc2.nv_cmpx_id
	having count(*) = 1
)
and adc.real_deal_cmpx_id not in  (
	select kmc.real_Deal_cmpx_id
	from KRED_KEY_MAPP_CMPX KMC
)
#and adc.real_deal_cmpx_id = '15250'
#and nc.nv_cmpx_id = '10023'
#15250/10023
;

###########################################################################################################################################################################################




#C)번지가 일치하지 않으나 단지명이 일치하는 경우 290
#select count(*)
select adc.real_Deal_cmpx_id 단지ID, adc.real_deal_cmpx_nm, adc.real_deal_cmpx_Seq_val 일련번호, adc.hnum, adc.legl_dong_orgl_num_cd 본번호, adc.legl_dong_vice_num_cd 부번호, adc.legl_dong_hnum_cd 번지코드
     , ld.legl_dong_nm, ld.legl_dong_whl_nm, nc.nv_cmpx_id, nc.nv_cmpx_knd, nc.bas_addr, nc.tot_hshl_cnt
     , trim(replace(SUBSTRING_INDEX(adc.hnum,'-',1),' ','')) hnum_trim
     , replace(SUBSTRING_INDEX(nc.bas_addr,'-',1),' ','') bas_trim
     , (
		select count(*)
		from kred_apt_deal_cmpx adc2
		inner join kred_nv_cmpx nc2
		on adc2.legl_dong_cd = nc2.legl_dong_cd    
		and trim(replace(SUBSTRING_INDEX(adc2.hnum,'-',1),' ','')) = trim(replace(SUBSTRING_INDEX(nc2.bas_addr,'-',1),' ',''))
        where adc2.real_deal_cmpx_id = adc.real_deal_cmpx_id		
     ) adc_cnt
     ,  (
		select count(*)
		from kred_apt_deal_cmpx adc2
		inner join kred_nv_cmpx nc2
		on adc2.legl_dong_cd = nc2.legl_dong_cd    
		and trim(replace(SUBSTRING_INDEX(adc2.hnum,'-',1),' ','')) = trim(replace(SUBSTRING_INDEX(nc2.bas_addr,'-',1),' ',''))
        where nc2.nv_cmpx_id = nc.nv_cmpx_id
     ) nc_cnt
from kred_apt_deal_cmpx adc
inner join kred_legl_dong ld
on adc.legl_dong_cd = ld.legl_dong_cd
inner join kred_nv_cmpx nc
on adc.LEGL_DONG_CD = nc.legl_dong_cd
and adc.real_Deal_cmpx_nm = nc.nv_cmpx_nm
where  1=1
and not exists (
	select 1
	from kred_nv_cmpx nc
	where adc.legl_dong_cd = nc.legl_dong_cd
	and adc.hnum = nc.bas_addr
)
and adc.real_deal_cmpx_id not in  (
	select kmc.real_Deal_cmpx_id
	from KRED_KEY_MAPP_CMPX KMC
)
and exists (
	select 1
    from kred_nv_cmpx nc
    where nc.legl_dong_Cd = adc.legl_dong_cd
    and nc.nv_cmpx_nm = adc.real_deal_cmpx_nm
)
;
select seq, count(*)
from (
	select distinct legl_dong_cd, hnum, seq
	from kred_deal_dtl
    where seq is not null
) a
group by seq 
having count(*) > 1    
;
select legl_dong_cd,  real_deal_cmpx_nm, count(*)
from (
	select distinct legl_dong_cd, hnum, real_deal_cmpx_nm
	from kred_deal_dtl
    where seq is not null
) a
group by legl_dong_cd,  real_deal_cmpx_nm
having count(*) > 1    
;

;

select * from kred_nv_cmpx 
where nv_cmpx_nm like '%서울역센트럴자이'



;

select SUBSTRING_INDEX(bas_addr,'-',1)
from kred_nv_cmpx
#where nv_cmpx_id = '100985'
;












#38726-120782
;

select * from KRED_KEY_MAPP_CMPX
where real_Deal_cmpx_id = '39726'
;

#39726-120782


desc KRED_KEY_MAPP_CMPX
;






select *
from KRED_KEY_MAPP_CMPX
group by real_deal_cmpx_id 
having count(*) >1
;






select count(*)
from kred_apt_deal_cmpx
where real_deal_cmpx_id in (
	select REAL_DEAL_CMPX_ID
	from kred_apt_deal_cmpx adc
	inner join kred_nv_cmpx nc
	on adc.legl_dong_cd = nc.legl_dong_cd
	and adc.hnum = nc.bas_addr
	and nc.nv_cmpx_knd in ('APT','JGC')
	group by adc.real_deal_cmpx_id
	having count(*) > 1
)    

;

select count(*)
from kred_apt_deal_cmpx adc
inner join kred_nv_cmpx nc
on adc.legl_dong_cd = nc.legl_dong_cd
and adc.hnum = nc.bas_addr
and nc.nv_cmpx_knd in ('APT','JGC')
where adc.real_Deal_cmpx_id in (
	select adc.REAL_DEAL_CMPX_ID
	from kred_apt_deal_cmpx adc
	inner join kred_nv_cmpx nc
	on adc.legl_dong_cd = nc.legl_dong_cd
	and adc.hnum = nc.bas_addr
	and nc.nv_cmpx_knd in ('APT','JGC')
	group by nc.nv_cmpx_id
	having count(*) > 1
)    
order by real_deal_cmpx_id


;
select * from kred_nv_cmpx
;

#2) 실거래가만 존재
select *
from kred_apt_deal_cmpx adc
where not exists (
	select 1
    from kred_nv_cmpx nc
    where adc.legl_dong_cd = nc.legl_dong_cd
    and adc.hnum = nc.bas_addr
)
and not exists (
	select 1
    from kred_apt_deal_cmpx_road adcr
    where adcr.real_deal_cmpx_id = adc.REAL_DEAL_CMPX_ID
)
;
select * 
from kred_apt_Deal_cmpx_road adcr
;
select * from kred_nv_cmpx
;
select * from kred_legl_dong
where legl_dong_cd = '1114017400'



