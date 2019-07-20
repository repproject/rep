-- KB물건식별자
CREATE TABLE `rep`.`KMIG_KB_CMPX` (
	`CMPX_IDF_ID` VARCHAR(9)   NOT NULL COMMENT 'KB부동산 물건식별자(아파트단지)', -- 물건식별자ID
	`CMPX_IDF_NM` VARCHAR(100) NULL     COMMENT 'KB부동산 물건명(단지명)', -- 물건식별자명
	`KB_REGN_CD`  VARCHAR(6)   NULL     COMMENT 'KB지역코드', -- KB지역코드
	`X_COOR_VAL`  FLOAT        NULL     COMMENT 'X좌표값', -- X좌표값
	`Y_COOR_VAL`  FLOAT        NULL     COMMENT 'Y좌표값', -- Y좌표값
	`REG_USER_ID` DECIMAL(10)  NOT NULL COMMENT '등록자ID', -- 등록자ID
	`REG_DTM`     DATETIME     NOT NULL COMMENT '등록일시', -- 등록일시
	`CHG_USER_ID` DECIMAL(10)  NOT NULL COMMENT '수정자ID', -- 수정자ID
	`CHG_DTM`     DATETIME     NOT NULL COMMENT '수정일시' -- 수정일시
)
COMMENT 'KB물건식별자';

-- KB물건식별자
ALTER TABLE `rep`.`KMIG_KB_CMPX`
	ADD CONSTRAINT `PK_KMIG_KB_CMPX` -- KB물건식별자 기본키
		PRIMARY KEY (
			`CMPX_IDF_ID` -- 물건식별자ID
		);
