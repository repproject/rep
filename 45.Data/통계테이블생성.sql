-- KB시세통계
CREATE TABLE `rep`.`KMIG_KB_PRC_STAT` (
	`CMPX_IDF_ID`       VARCHAR(9)   NOT NULL COMMENT 'KB부동산 물건식별자(아파트단지)', -- 물건식별자ID
	`HOUSE_TYP_SEQ`     DECIMAL(3)   NOT NULL COMMENT 'KB부동산 주택형일련번호', -- 주택형일련번호
	`STD_YYMM`          VARCHAR(6)   NOT NULL COMMENT '기준년월', -- 기준년월
	`KB_LV1_REGN_CD`    VARCHAR(6)   NULL     COMMENT 'KB지역코드', -- KBLV1지역코드
	`KB_LV1_REGN_NM`    VARCHAR(20)  NOT NULL COMMENT 'KB부동산에서 가져온 지역명', -- KBLV1지역명
	`KB_LV2_REGN_CD`    VARCHAR(6)   NULL     COMMENT 'KB지역코드', -- KBLV2지역코드
	`KB_LV2_REGN_NM`    VARCHAR(20)  NOT NULL COMMENT 'KB부동산에서 가져온 지역명', -- KBLV2지역명
	`KB_LV3_REGN_CD`    VARCHAR(6)   NULL     COMMENT 'KB지역코드', -- KBLV3지역코드
	`KB_LV3_REGN_NM`    VARCHAR(20)  NOT NULL COMMENT 'KB부동산에서 가져온 지역명', -- KBLV3지역명
	`CMPX_IDF_NM`       VARCHAR(100) NULL     COMMENT 'KB부동산 물건명(단지명)', -- 물건식별자명
	`X_COOR_VAL`        FLOAT        NULL     COMMENT 'X좌표값', -- X좌표값
	`Y_COOR_VAL`        FLOAT        NULL     COMMENT 'Y좌표값', -- Y좌표값
	`HOUSE_TYP_NM`      VARCHAR(50)  NULL     COMMENT '주택형명', -- 주택형명
	`HOUSE_TYP_RPSN_NM` VARCHAR(50)  NULL     COMMENT '주택형명을 대표하는 주택형대표명 ex) 84A', -- 주택형대표명
	`ONLY_AERA`         FLOAT(10,2)  NULL     COMMENT '전용면적', -- 전용면적
	`SPLY_AERA`         FLOAT(10,2)  NULL     COMMENT '공급면적', -- 공급면적
	`UP_AVG_PRC`        DECIMAL(10)  NULL     COMMENT 'KB부동산 매매 상위평균가(단위 : 만원)', -- 상위평균가
	`GNRL_AVG_PRC`      DECIMAL(10)  NULL     COMMENT 'KB부동산 매매 일반평균가(단위 : 만원)', -- 일반평균가
	`DOWN_AVG_PRC`      DECIMAL(10)  NULL     COMMENT 'KB부동산 매매 하위평균가(단위 : 만원)', -- 하위평균가
	`UP_JS_AVG_PRC`     DECIMAL(10)  NULL     COMMENT 'KB부동산 전세 상위평균가(단위 : 만원)', -- 상위전세평균가
	`GNRL_JS_AVG_PRC`   DECIMAL(10)  NULL     COMMENT 'KB부동산 전세 일반평균가(단위 : 만원)', -- 일반전세평균가
	`DOWN_JS_AVG_PRC`   DECIMAL(10)  NULL     COMMENT 'KB부동산 전세 하위평균가(단위 : 만원)', -- 하위전세평균가
	`GNRL_GAP`          DECIMAL(10)  NULL     COMMENT '매매 일반평균가 - 전세 일반평균가', -- 일반GAP
	`1M_PRC`            DECIMAL(10)  NULL     COMMENT '1개월전가격', -- 1개월전가격
	`1M_JS_PRC`         DECIMAL(10)  NULL     COMMENT '1개월전전세가', -- 1개월전전세가
	`1M_GAP`            DECIMAL(10)  NULL     COMMENT '1개월전GAP', -- 1개월전GAP
	`1M_RISE_PRC`       DECIMAL(10)  NULL     COMMENT '1개월전상승매매가', -- 1개월전상승매매가
	`1M_ROR`            FLOAT(5,3)   NULL     COMMENT '1개월상승률', -- 1개월상승률
	`1M_GAP_ROR`        FLOAT(5,3)   NULL     COMMENT '1개월GAP대비상승률', -- 1개월GAP대비상승률
	`3M_PRC`            DECIMAL(10)  NULL     COMMENT '3개월전가격', -- 3개월전가격
	`3M_JS_PRC`         DECIMAL(10)  NULL     COMMENT '3개월전전세가', -- 3개월전전세가
	`3M_RISE_PRC`       DECIMAL(10)  NULL     COMMENT '3개월전상승매매가', -- 3개월전상승매매가
	`3M_GAP`            DECIMAL(10)  NULL     COMMENT '3개월전GAP', -- 3개월전GAP
	`3M_ROR`            FLOAT(5,3)   NULL     COMMENT '3개월상승률', -- 3개월상승률
	`3M_GAP_ROR`        FLOAT(5,3)   NULL     COMMENT '3개월GAP대비상승률', -- 3개월GAP대비상승률
	`6M_PRC`            DECIMAL(10)  NULL     COMMENT '6개월전가격', -- 6개월전가격
	`6M_JS_PRC`         DECIMAL(10)  NULL     COMMENT '6개월전전세가', -- 6개월전전세가
	`6M_GAP`            DECIMAL(10)  NULL     COMMENT '6개월전GAP', -- 6개월전GAP
	`6M_RISE_PRC`       DECIMAL(10)  NULL     COMMENT '6개월전상승매매가', -- 6개월전상승매매가
	`6M_ROR`            FLOAT(5,3)   NULL     COMMENT '6개월상승률', -- 6개월상승률
	`6M_GAP_ROR`        FLOAT(5,3)   NULL     COMMENT '6개월GAP대비상승률', -- 6개월GAP대비상승률
	`1Y_PRC`            DECIMAL(10)  NULL     COMMENT '1년전가격', -- 1년전가격
	`1Y_JS_PRC`         DECIMAL(10)  NULL     COMMENT '1년전전세가', -- 1년전전세가
	`1Y_GAP`            DECIMAL(10)  NULL     COMMENT '1년전GAP', -- 1년전GAP
	`1Y_RISE_PRC`       DECIMAL(10)  NULL     COMMENT '1년전상승매매가', -- 1년전상승매매가
	`1Y_ROR`            FLOAT(5,3)   NULL     COMMENT '1년상승률', -- 1년상승률
	`1Y_GAP_ROR`        FLOAT(5,3)   NULL     COMMENT '1년GAP대비상승률', -- 1년GAP대비상승률
	`2Y_PRC`            DECIMAL(10)  NULL     COMMENT '2년전가격', -- 2년전가격
	`2Y_JS_PRC`         DECIMAL(10)  NULL     COMMENT '2년전전세가', -- 2년전전세가
	`2Y_GAP`            DECIMAL(10)  NULL     COMMENT '2년전GAP', -- 2년전GAP
	`2Y_RISE_PRC`       DECIMAL(10)  NULL     COMMENT '2년전상승매매가', -- 2년전상승매매가
	`2Y_ROR`            FLOAT(5,3)   NULL     COMMENT '2년상승률', -- 2년상승률
	`2Y_GAP_ROR`        FLOAT(5,3)   NULL     COMMENT '2년GAP대비상승률', -- 2년GAP대비상승률
	`3Y_PRC`            DECIMAL(10)  NULL     COMMENT '3년전가격', -- 3년전가격
	`3Y_JS_PRC`         DECIMAL(10)  NULL     COMMENT '3년전전세가', -- 3년전전세가
	`3Y_RISE_PRC`       DECIMAL(10)  NULL     COMMENT '3년전상승매매가', -- 3년전상승매매가
	`3Y_GAP`            DECIMAL(10)  NULL     COMMENT '3년전GAP', -- 3년전GAP
	`3Y_ROR`            FLOAT(5,3)   NULL     COMMENT '3년상승률', -- 3년상승률
	`3Y_GAP_ROR`        FLOAT(5,3)   NULL     COMMENT '3년GAP대비상승률', -- 3년GAP대비상승률
	`4Y_PRC`            DECIMAL(10)  NULL     COMMENT '4년전가격', -- 4년전가격
	`4Y_JS_PRC`         DECIMAL(10)  NULL     COMMENT '4년전전세가', -- 4년전전세가
	`4Y_RISE_PRC`       DECIMAL(10)  NULL     COMMENT '4년전상승매매가', -- 4년전상승매매가
	`4Y_GAP`            DECIMAL(10)  NULL     COMMENT '4년전GAP', -- 4년전GAP
	`4Y_ROR`            FLOAT(5,3)   NULL     COMMENT '4년상승률', -- 4년상승률
	`4Y_GAP_ROR`        FLOAT(5,3)   NULL     COMMENT '4년GAP대비상승률', -- 4년GAP대비상승률
	`5Y_PRC`            DECIMAL(10)  NULL     COMMENT '5년전가격', -- 5년전가격
	`5Y_JS_PRC`         DECIMAL(10)  NULL     COMMENT '5년전전세가', -- 5년전전세가
	`5Y_RISE_PRC`       DECIMAL(10)  NULL     COMMENT '5년전상승매매가', -- 5년전상승매매가
	`5Y_GAP`            DECIMAL(10)  NULL     COMMENT '5년전GAP', -- 5년전GAP
	`5Y_ROR`            FLOAT(5,3)   NULL     COMMENT '5년상승률', -- 5년상승률
	`5Y_GAP_ROR`        FLOAT(5,3)   NULL     COMMENT '5년GAP대비상승률', -- 5년GAP대비상승률
	`10Y_PRC`           DECIMAL(10)  NULL     COMMENT '10년전가격', -- 10년전가격
	`10Y_JS_PRC`        DECIMAL(10)  NULL     COMMENT '10년전전세가', -- 10년전전세가
	`10Y_RISE_PRC`      DECIMAL(10)  NULL     COMMENT '10년전상승매매가', -- 10년전상승매매가
	`10Y_GAP`           DECIMAL(10)  NULL     COMMENT '10년전GAP', -- 10년전GAP
	`10Y_ROR`           FLOAT(5,3)   NULL     COMMENT '10년상승률', -- 10년상승률
	`10Y_GAP_ROR`       FLOAT(5,3)   NULL     COMMENT '10년GAP대비상승률', -- 10년GAP대비상승률
	`REG_USER_ID`       DECIMAL(10)  NOT NULL COMMENT '등록자ID', -- 등록자ID
	`REG_DTM`           DATETIME     NOT NULL COMMENT '등록일시', -- 등록일시
	`CHG_USER_ID`       DECIMAL(10)  NOT NULL COMMENT '수정자ID', -- 수정자ID
	`CHG_DTM`           DATETIME     NOT NULL COMMENT '수정일시' -- 수정일시
)
COMMENT 'KB시세를 통계 테이블로 생성';

-- KB시세통계
ALTER TABLE `rep`.`KMIG_KB_PRC_STAT`
	ADD CONSTRAINT `PK_KMIG_KB_PRC_STAT` -- KB시세통계 기본키
		PRIMARY KEY (
			`CMPX_IDF_ID`,   -- 물건식별자ID
			`HOUSE_TYP_SEQ`, -- 주택형일련번호
			`STD_YYMM`       -- 기준년월
		);