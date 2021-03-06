import os
import csv
import pymysql
from datetime import datetime

# db접속 및 데이터 import
def dbConnect():
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
    con.close()
    return result

# 메뉴 경로 계산 및 유지시간 전체 계산
def calcPathCost(result):
    
    # login / logout 시간 정보에 대한 table 인덱스 정보 별도 저장    
    idx_login =[]       # login 시점 index
    idx_logout = []     # logout 시점 index 
    login_dtm = []      # login시간
    logout_dtm = []     # logout 시간 
    
    for i,elem in enumerate(result):

        if 'login' in elem:
            idx_login.append(i)
            login_dtm.append(result[i][1])

        elif 'logout' in elem: 
            idx_logout.append(i)
            logout_dtm.append(result[i][1])


    # 메뉴방문 경로 집계를 위한 데이터 별도 저장
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

    # 메뉴 방문경로에 대해 중복없는 값 전체 추출
    duplicated = list(set(map(tuple,pathCalc)))

    # 메뉴 방문에 대한 중복 기준 카운트 집계 및 메뉴 유지시간 계산
    pathResult = []
    for i in range(len(duplicated)):
        
        tmp = list(duplicated[i]) 
        cnt = 0
        cntLength = 0
        tmpTime = []
        tmpTimeDelta = []            
        
        for j in range(len(pathCalc)):
            
            if (list(duplicated[i]) == list(pathCalcTime[j][:-2])) :
                
                cnt = cnt+1     #경로 발생 카운트 증분
                cntLength = len(pathCalcTime[j][:-2]) # 해당 경로 추출
                endTime = datetime.strptime(pathCalcTime[j][-1],'%Y%m%d%H%M%S') #경로유지종료시간
                startTime = datetime.strptime(pathCalcTime[j][-2],'%Y%m%d%H%M%S') # 경로유지시작시간
                
                tmpTime.append(str(endTime-startTime)) # 활동시간 문자열 
                tmpTimeDelta.append(endTime-startTime) # 활동시간 변위
        
        # 메뉴 방문시간 집계 정렬
        tmpTime.sort()
        tmpTimeDelta.sort()

        tmp.append(tmpTime[-1])
        tmp.append(tmpTime[0])
        tmp.append(tmpTimeDelta[-1])

        # 메뉴 방문 횟수 집계 
        # tmp.append(cntLength)
        tmp.append(cnt)
        
        pathResult.append(tmp)

    # 최종 데이터 인덱싱 데이터 정리
    modePath = []
    for i in range(len(pathResult)):
        modePath.append([pathResult[i][-1],i,pathResult[i][-2]])

    # 경로 빈출 및 최대시간 기준 정렬
    outputIndex = sorted(modePath,key = lambda x : (-x[0],-x[2]))
    
    return pathResult,outputIndex

# csv 출력 
def writeCSV(data,number):
    with open('2-4/result.csv','w',newline='',encoding='utf-8') as file:    
        writer = csv.writer(file)
        for i in range(number):
            writer.writerow(data[0][data[1][i][1]][:-2])
    
if __name__ == "__main__":
    result = dbConnect()
    output = calcPathCost(result)
    writeCSV(output,3)  # 0,1,2(top3만 출력)