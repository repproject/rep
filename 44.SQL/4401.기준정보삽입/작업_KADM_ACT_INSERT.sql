SELECT * FROM kadm_act
;
INSERT INTO `rep`.`kadm_act`
(`ACT_ID`,
`ACT_NM`,
`ACT_DESC`,
`USE_YN`,
`REF1`,
`REF2`,
`REF3`,
`REF4`,
`REF5`,
`REG_USER_ID`,
`REG_DTM`,
`CHG_USER_ID`,
`CHG_DTM`)
VALUES
('NV_UP_CMPX',
'KB주택형월별시세 갱신',
'KB주택형월별시세 갱신',
'Y',
NULL,
NULL,
NULL,
NULL,
NULL,
1000000001,
NOW(),
1000000001,
NOW());
