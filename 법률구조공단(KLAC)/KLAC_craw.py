# -*- coding: utf-8 -*-

import json
import time
import requests
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options







# croll 2번씩 내려감
def scroll_dowmn_page2():
    for i in range(2): # adjust integer value for need
        driver.execute_script("window.scrollBy(0, 200)")
        time.sleep(0.5)


# 법률 구조 공단 크롤링  - 질문자 데이터
def klac_data_Writer():
    writer = []
    Org = 3

    # 사건 제목 title
    # 상닫번호 num
    # 신청일 data
    # 진행현황 process_state
    # 작성자가 쓴 내용 content

    title = driver.find_element_by_xpath("//*[@id='content']/form[1]/div[2]/div/div[2]/div[1]/h2").text
    num =  driver.find_element_by_xpath("//*[@id='content']/form[1]/div[2]/div/div[2]/div[2]/dl[1]/dd").text
    data = driver.find_element_by_xpath("//*[@id='content']/form[1]/div[2]/div/div[2]/div[2]/dl[2]/dd").text
    #process_state = driver.find_element_by_xpath("//*[@id='content']/form[1]/div[2]/div/div[2]/div[2]/dl[3]/dd").text
    content = driver.find_element_by_xpath("//*[@id='content']/form[1]/div[2]/div/div[2]/div[3]").text
    content = content.replace("\n","")

    writer.append(Org)
    writer.append(num)
    writer.append(title)
    writer.append(content)
    #writer.append(process_state)
    writer.append(data)

    print(*writer)
    insert_inquiry(writer)
    return writer


# 법률 구조 공단 크롤링  - 답변자 데이터
def klac_data_Answer():
    answer =[]

    # 답변일 data2
    # 답변자(변호사)가 쓴 내용 answer_content

    answer_data = driver.find_element_by_xpath("//*[@id='content']/form[1]/div[2]/div/div[3]/div[1]/dl[1]/dd").text 
    num =  driver.find_element_by_xpath("//*[@id='content']/form[1]/div[2]/div/div[2]/div[2]/dl[1]/dd").text

    answer_content =  driver.find_element_by_xpath("//*[@id='content']/form[1]/div[2]/div/div[3]/div[2]").text
    answer_content = answer_content.replace("\n","")

    answer.append(num)
    answer.append(answer_content)
    answer.append(answer_data) # 사건 번호

    print(*answer)
    insert_answer(answer)
    return answer



# AWS DB 연동
#def get_db():
#    db = pymysql.connect(
#        host='ec2-13-125-144-25.ap-northeast-2.compute.amazonaws.com',
#        port=3306,
#        user='admin',
#        passwd='1/zw;GytAwx*',
#        db='KLAC',
#        charset='utf8'
#    )
#    return db


# Azure DB 연동
def get_db():
    db = pymysql.connect(
        host='52.141.5.164',
        port=3306,
        user='admin',
        passwd='1/zw;GytAwx*',
        db='KLAC',
        charset='utf8'
    )
    return db








# AWS Inquiry TABLE DB에 데이터 넣기
def insert_inquiry(data):
    db = get_db()
    mycursor = db.cursor()

    try:
        sql = "INSERT INTO Inquiry (OrgIndex,Num,Title,content,regDate,Link) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (data[0],data[1],data[2],data[3],data[4],a)
        mycursor.execute(sql, val)

        db.commit()
        db.close()

    except Exception as e:
        print('db insert inquiry error', e)
        db.close()

        
        
        

# AWS ANSWER TABLE DB에 데이터 넣기
def insert_answer(data):
    db = get_db()
    mycursor = db.cursor()

    try:
        sql = "INSERT INTO Answer (Num,content,regDate,Link) VALUES (%s, %s, %s, %s)"
        val = (data[0],data[1],data[2],a)
        mycursor.execute(sql, val)

        db.commit()
        db.close()

    except Exception as e:
        print('db insert inquiry error', e)
        db.close()


# 게시글 수가 100단위 일 때, next page
# [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000] 
arr = []
for i in range(1,31):
    i = 100 * i
    arr.append(i)






















# ---------------------------------------- main ----------------------------------------------------
options = Options()


#options.add_argument('lang=en') # 언어를 en(영어로)
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')


# fake-user-agent를 추가
options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
#options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

driver = webdriver.Chrome(executable_path='/home/ubuntu/chromedriver', options=options)





print("==================================================================================")
print("--------------------Linux에서 Crawling 작업을 시작하겠습니다----------------------")
print("==================================================================================")
print("--------------------------------법률구조공단(KLAC)--------------------------------")
print("작업 내용: 작성 게시글 1일 이전(00:00~23:59) 모든 데이터 추출 및 저장")
print("\n\n")



try :    
    url = "https://www.klac.or.kr/legalstruct/cyberConsultation/selectOpenArticleList.do?boardCode=3"
    driver.get(url)          
    time.sleep(2)
    scroll_dowmn_page2()
    
    board_num = 1
    
    try :
        
        while True :
                       
            # 페이지네이션 1->2->3->10
            for j in range(1,11):
                case = driver.find_element_by_xpath(f"//*[@id='content']/form[1]/div[2]/div/div[4]/a[{j}]").click()


                #게시글 클릭 1~10 
                for i in range(1,11):

                    driver.implicitly_wait(10)
                    case = driver.find_element_by_xpath(f"//*[@id='content']/form[1]/div[2]/div/div[3]/table/tbody/tr[{i}]").click()
                    
                    # 현재 웹 페이지 URL 추출
                    a = driver.current_url
                  

                    scroll_dowmn_page2()
                
                
                    try :
                        print("현재 진행중인 게시글 Number :",board_num)
                        board_num += 1

                        driver.implicitly_wait(10)
                        print("===============질문 게시글=================")
                        klac_data_Writer() # 법률 구조 공단 크롤링  - 질문자 데이터
                        
                        print("===============답변 게시글=================")
                        klac_data_Answer() # 법률 구조 공단 크롤링  - 답변자 데이터
                        
                        driver.back() # 뒤로가기

                        print("------------------------------------------------------------------")
                        
                        
                        # 1Next page 버튼 클릭
                        if board_num in arr:
                            driver.find_element_by_xpath("//*[@id='content']/form[1]/div[2]/div/div[4]/button[3]").click()

                    except Exception as e :
                        print("데이터 추출 error",e)

                      
    except Exception as e :
        print("게시글 클릭 error",e)

except Exception as e :
    print("데이터 로딩 error",e)
