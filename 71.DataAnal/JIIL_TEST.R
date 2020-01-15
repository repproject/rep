#install.packages("dbConnect")
library("dbConnect")
#install.packages("RMySQL")
library("RMySQL")
#install.packages("RODBC")
library("RODBC")
#install.packages("DBI")
library("DBI")
library("ggplot2")

library("data.table")
library("lubridate")
library('scales')
#intall.packages("PerformanceAnalytics")
library("PerformanceAnalytics")
library("readxl")




DB<-dbConnect(dbDriver("MySQL"),dbname = "rep", user = "root", password ="5427", host = "localhost")

##---- Encoding
dbGetQuery(conn = con, "SET NAMES euckr")



;

## DB Connect ##

## ---- Library
library(DBI)
library(RMySQL)

## ---- Create DB Connection
con <- dbConnect(drv = RMySQL::MySQL(), host = "ceasar.iptime.org", port = 3306,
                 dbname = "rep", user = "repuser", password = "0(tjwlscjf)")

##---- Encoding
dbGetQuery(conn = con, "SET NAMES euckr")

## SQL
data_avg_deal_amt <- dbGetQuery(conn = con, "SELECT DEAL_YYMM, AVG(DEAL_AMT) AVG_DEAL_AMT FROM KMIG_DEAL_DTL WHERE GOV_LEGL_DONG_CD = '11710' GROUP BY DEAL_YYMM")

head(data_avg_deal_amt)

data_avg_deal_amt$DEAL_YYMM<-as.Date(paste0(as.character(data_avg_deal_amt$DEAL_YYMM), '01'), format='%Y%m%d')

plot(data_avg_deal_amt$AVG_DEAL_AMT)

p <- ggplot(data = data_avg_deal_amt) +
  geom_line(aes(x = DEAL_YYMM, y = AVG_DEAL_AMT), color = "red", linetype = 1) #+
  #(aes(x = YYMM, y = KB_APT_JS_INDX), color = "blue", linetype = 1) +
  #geom_line(aes(x = YYMM, y = INTE_RATE*20), color = "purple", linetype = 1) 

datebreaks <- seq(as.Date("2006-01-01"), as.Date("2019-11-01"), by="1 month")
datebreaks

p + scale_x_date(breaks=datebreaks, labels=date_format("%Y-%M")) #+theme(axis.text.x = element_text(angle=30, hjust=1))

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
