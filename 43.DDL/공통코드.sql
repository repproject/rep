-- 공통코드리스트
CREATE TABLE `KADM_COM_CD_LST` (
	`COM_CD_GRP`      VARCHAR(20)  NOT NULL COMMENT '공통코드그룹', -- 공통코드그룹
	`COM_CD_GRP_NM`   VARCHAR(100) NULL     COMMENT '공통코드그룹명', -- 공통코드그룹명
	`COM_CD_GRP_DESC` VARCHAR(200) NULL     COMMENT '공통코드그룹설명', -- 공통코드그룹설명
	`REF1`            VARCHAR(100) NULL     COMMENT '참조1', -- 참조1
	`REF2`            VARCHAR(100) NULL     COMMENT '참조2', -- 참조2
	`REF3`            VARCHAR(100) NULL     COMMENT '참조3', -- 참조3
	`REF4`            VARCHAR(100) NULL     COMMENT '참조4', -- 참조4
	`REF5`            VARCHAR(100) NULL     COMMENT '참조5', -- 참조5
	`REG_USER_ID`     DECIMAL(10)  NULL     COMMENT '등록자ID', -- 등록자ID
	`REG_DTM`         DATE         NULL     COMMENT '등록일시', -- 등록일시
	`CHG_USER_ID`     DECIMAL(10)  NULL     COMMENT '수정자ID', -- 수정자ID
	`CHG_DTM`         DATE         NULL     COMMENT '수정일시' -- 수정일시
)
COMMENT '공통코드리스트';

-- 공통코드리스트
ALTER TABLE `KADM_COM_CD_LST`
	ADD CONSTRAINT `PK_KADM_COM_CD_LST` -- 공통코드리스트 기본키
		PRIMARY KEY (
			`COM_CD_GRP` -- 공통코드그룹
		);

-- 공통코드상세
CREATE TABLE `KADM_COM_CD_DTL` (
	`COM_CD_GRP`  VARCHAR(20)  NOT NULL COMMENT '공통코드그룹', -- 공통코드그룹
	`COM_CD`      VARCHAR(20)  NOT NULL COMMENT '공통코드', -- 공통코드
	`COM_CD_NM`   VARCHAR(100) NULL     COMMENT '공통코드명', -- 공통코드명
	`REF1`        VARCHAR(100) NULL     COMMENT '참조1', -- 참조1
	`REF2`        VARCHAR(100) NULL     COMMENT '참조2', -- 참조2
	`REF3`        VARCHAR(100) NULL     COMMENT '참조3', -- 참조3
	`REF4`        VARCHAR(100) NULL     COMMENT '참조4', -- 참조4
	`REF5`        VARCHAR(100) NULL     COMMENT '참조5', -- 참조5
	`REG_USER_ID` DECIMAL(10)  NULL     COMMENT '등록자ID', -- 등록자ID
	`REG_DTM`     DATE         NULL     COMMENT '등록일시', -- 등록일시
	`CHG_USER_ID` DECIMAL(10)  NULL     COMMENT '수정자ID', -- 수정자ID
	`CHG_DTM`     DATE         NULL     COMMENT '수정일시' -- 수정일시
)
COMMENT '공통코드상세';

-- 공통코드상세
ALTER TABLE `KADM_COM_CD_DTL`
	ADD CONSTRAINT `PK_KADM_COM_CD_DTL` -- 공통코드상세 기본키
		PRIMARY KEY (
			`COM_CD_GRP`, -- 공통코드그룹
			`COM_CD`      -- 공통코드
		);