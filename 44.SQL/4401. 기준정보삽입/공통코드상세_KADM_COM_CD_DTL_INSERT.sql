INSERT INTO `rep`.`kadm_com_cd_dtl`
(`COM_CD_GRP`,
`COM_CD`,
`COM_CD_NM`,
`REF1`,
`REF2`,
`REF3`,
`REF4`,
`REF5`,
`REG_USER_ID`,
`REG_DTM`,
`CHG_USER_ID`,
`CHG_DTM`)
VALUES(
"MIG_RSN",
"KBNCDUP",
"지역매핑과 단지명으로 매핑했는데 2개이상이 나옴.(당산)",
'N',
NULL,
NULL,
NULL,
NULL,
1000000001,
NOW(),
1000000001,
NOW())
;
SELECT * FROM kadm_com_cd_dtl
;

SELECT * FROM KMIG_NV_CMPX