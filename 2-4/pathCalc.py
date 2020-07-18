import os
import csv
import pymysql
from datetime import datetime

con = pymysql.connect(host="localhost",
                      port =3306,
                      user="smylere",
                      password="password1234!",
                      db='KAKAOBANK',
                      charset='utf8')

cur = con.cursor()
sql = "select MENU_NM, LOG_TKTM from KAKAOBANK.MENU_LOG ORDER BY USR_NO,LOG_ID"
cur.execute(sql)

result = list(cur.fetchall())
    
idx_login =[]
idx_logout = []
login_dtm = []
logout_dtm = []
for i,elem in enumerate(result):

    if 'login' in elem:
        idx_login.append(i)
        login_dtm.append(result[i][1])

    elif 'logout' in elem: 
        idx_logout.append(i)
        logout_dtm.append(result[i][1])

pathCalc = []
pathCalcTime = []
for i in range(len(idx_login)):

    tmp = []
    tmpDuplicated = [] 
         
    for j in range(len(result[idx_login[i]:idx_logout[i]+1])):
        tmp.append(result[idx_login[i]+j][0])
        tmpDuplicated.append(result[idx_login[i]+j][0])
       
    pathCalc.append(tmp)
    pathCalcTime.append(tmpDuplicated+[login_dtm[i]]+[logout_dtm[i]])

duplicated = list(set(map(tuple,pathCalc)))

pathResult = []
for i in range(len(duplicated)):
    
    tmp = list(duplicated[i]) 
    cnt = 0
    cntLength = 0
    tmpTime = []
    tmpTimeDelta = []            
    
    for j in range(len(pathCalc)):
        
        if (list(duplicated[i]) == list(pathCalcTime[j][:-2])) :
            
            cnt = cnt+1
            cntLength = len(pathCalcTime[j][:-2])
            endTime = datetime.strptime(pathCalcTime[j][-1],'%Y%m%d%H%M%S')
            startTime = datetime.strptime(pathCalcTime[j][-2],'%Y%m%d%H%M%S')
            
            tmpTime.append(str(endTime-startTime)) # 활동시간 문자열 
            tmpTimeDelta.append(endTime-startTime) # 활동시간 변위
    
    tmpTime.sort()

    tmp.append(tmpTime[-1])
    tmp.append(tmpTime[0])
    tmp.append(tmpTimeDelta[-1])

    # tmp.append(cntLength)
    tmp.append(cnt)
    
    pathResult.append(tmp)


# 최종 데이터 인덱싱 데이터 정리
modePath = []
for i in range(len(pathResult)):
    modePath.append([pathResult[i][-1],i,pathResult[i][-2]])

# 경로 빈출 및 최대시간 기준 정렬
outputIndex = sorted(modePath,key = lambda x : (-x[0],-x[2]))

# print(pathResult[outputIndex[0][1]][:-2])
# print(pathResult[outputIndex[1][1]][:-2])
# print(pathResult[outputIndex[2][1]][:-2])

with open('2-4/result.csv','w',newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(pathResult[outputIndex[0][1]][:-2])
    writer.writerow(pathResult[outputIndex[1][1]][:-2])
    writer.writerow(pathResult[outputIndex[2][1]][:-2])
    
con.close()