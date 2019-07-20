-- 주택형
CREATE TABLE `rep`.`KMIG_KB_CMPX_TYP` (
	`CMPX_IDF_ID`   VARCHAR(9)  NOT NULL COMMENT 'KB부동산 물건식별자(아파트단지)', -- 물건식별자ID
	`HOUSE_TYP_SEQ` DECIMAL(3)  NOT NULL COMMENT 'KB부동산 주택형일련번호', -- 주택형일련번호
	`HOUSE_TYP_NM`  VARCHAR(50) NULL     COMMENT '주택형명', -- 주택형명
	`REG_USER_ID`   DECIMAL(10) NOT NULL COMMENT '등록자ID', -- 등록자ID
	`REG_DTM`       DATETIME    NOT NULL COMMENT '등록일시', -- 등록일시
	`CHG_USER_ID`   DECIMAL(10) NOT NULL COMMENT '수정자ID', -- 수정자ID
	`CHG_DTM`       DATETIME    NOT NULL COMMENT '수정일시' -- 수정일시
)
COMMENT '주택형';

-- 주택형
ALTER TABLE `rep`.`KMIG_KB_CMPX_TYP`
	ADD CONSTRAINT `PK_KMIG_KB_CMPX_TYP` -- 주택형 기본키
		PRIMARY KEY (
			`CMPX_IDF_ID`,   -- 물건식별자ID
			`HOUSE_TYP_SEQ`  -- 주택형일련번호
		);
