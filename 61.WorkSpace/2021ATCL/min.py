#import csv
import pandas as pd

#f = open("D:/NaverCloud/R/2021_ATCL/21년_ATCL_SOPData추출.xlsx", 'r', encoding='utf-8')
df = pd.read_excel("D:/NaverCloud/R/2021_ATCL/21년_ATCL_SOPData추출.xlsx")
print(df[1])

print(df)
#rdr = csv.reader(f)
# for line in rdr:
#     print(line)
# f.close()