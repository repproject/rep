## DB Connect ##

## ---- Library
library(DBI)
library(RMySQL)

## ---- Create DB Connection
con <- dbConnect(drv = RMySQL::MySQL(), host = "ceasar.iptime.org", port = 3306,
                 dbname = "rep", user = "repuser", password = "0(tjwlscjf)")

##---- Encoding
dbGetQuery(conn = con, "SET NAMES euckr")

##---- Read Table
# 물건식별자
kmig_kb_cmpx <- DBI::dbReadTable(conn = con, name = "kmig_kb_cmpx")
# 주택형
kmig_kb_cmpx_typ <- DBI::dbReadTable(conn = con, name = "kmig_kb_cmpx_typ")
# 매매가, 전세가
kmig_kb_cmpx_typ_mon_prc <- DBI::dbReadTable(conn = con, name = "kmig_kb_cmpx_typ_mon_prc")

head(kmig_kb_cmpx)

## ---- Disconnect DB
DBI::dbDisconnect(conn = con)