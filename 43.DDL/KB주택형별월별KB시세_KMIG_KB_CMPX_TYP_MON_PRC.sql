-- 주택형별월별KB시세
CREATE TABLE `rep`.`KMIG_KB_CMPX_TYP_MON_PRC` (
	`CMPX_IDF_ID`     VARCHAR(9)  NOT NULL COMMENT 'KB부동산 물건식별자(아파트단지)', -- 물건식별자ID
	`HOUSE_TYP_SEQ`   DECIMAL(3)  NOT NULL COMMENT 'KB부동산 주택형일련번호', -- 주택형일련번호
	`STD_YYMM`        VARCHAR(6)  NOT NULL COMMENT '기준년월', -- 기준년월
	`UP_AVG_PRC`      DECIMAL(10) NULL     COMMENT 'KB부동산 매매 상위평균가(단위 : 만원)', -- 상위평균가
	`GNRL_AVG_PRC`    DECIMAL(10) NULL     COMMENT 'KB부동산 매매 일반평균가(단위 : 만원)', -- 일반평균가
	`DOWN_AVG_PRC`    DECIMAL(10) NULL     COMMENT 'KB부동산 매매 하위평균가(단위 : 만원)', -- 하위평균가
	`UP_JS_AVG_PRC`   DECIMAL(10) NULL     COMMENT 'KB부동산 전세 상위평균가(단위 : 만원)', -- 상위전세평균가
	`GNRL_JS_AVG_PRC` DECIMAL(10) NULL     COMMENT 'KB부동산 전세 일반평균가(단위 : 만원)', -- 일반전세평균가
	`DOWN_JS_AVG_PRC` DECIMAL(10) NULL     COMMENT 'KB부동산 전세 하위평균가(단위 : 만원)', -- 하위전세평균가
	`REG_USER_ID`     DECIMAL(10) NOT NULL COMMENT '등록자ID', -- 등록자ID
	`REG_DTM`         DATETIME    NOT NULL COMMENT '등록일시', -- 등록일시
	`CHG_USER_ID`     DECIMAL(10) NOT NULL COMMENT '수정자ID', -- 수정자ID
	`CHG_DTM`         DATETIME    NOT NULL COMMENT '수정일시' -- 수정일시
)
COMMENT '주택형별월별KB시세';

-- 주택형별월별KB시세
ALTER TABLE `rep`.`KMIG_KB_CMPX_TYP_MON_PRC`
	ADD CONSTRAINT `PK_KMIG_KB_CMPX_TYP_MON_PRC` -- 주택형별월별KB시세 기본키
		PRIMARY KEY (
			`CMPX_IDF_ID`,   -- 물건식별자ID
			`HOUSE_TYP_SEQ`, -- 주택형일련번호
			`STD_YYMM`       -- 기준년월
		);