select deal_yymm, lpad(deal_ymd,2,'0'), real_deal_cmpx_nm, only_area, flr, deal_amt 
from kred_deal_dtl
where deal_yymm >= '202201'
and legl_dong_cd = '41450'
order by deal_yymm desc, lpad(deal_ymd,2,'0') desc
;
SELECT *
FROM kred_deal_dtl
;
