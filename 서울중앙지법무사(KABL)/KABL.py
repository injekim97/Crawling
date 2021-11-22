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
    
    
    
    
    

# # AWS DB 연동(AWS)
# def get_db():
#     db = pymysql.connect(
#         host='ec2-13-125-144-25.ap-northeast-2.compute.amazonaws.com',
#         port=3306,
#         user='admin',
#         passwd='1/zw;GytAwx*',
#         db='KABL',
#         charset='utf8'
#     )
#     return db






# AWS DB 연동 (Azure)
def get_db():
    db = pymysql.connect(
        host='52.141.5.164',
        port=3306,
        user='admin',
        passwd='1/zw;GytAwx*',
        db='KABL',
        charset='utf8'
    )
    return db
 

    
    
    



# AWS Inquiry TABLE DB에 데이터 넣기
def insert_inquiry(data):
    db = get_db()
    mycursor = db.cursor()

    try:
        sql = "INSERT INTO Inquiry (Num,Title,regDate,context,OrgIndex,Link) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (data[1],data[2],data[3],data[4],data[0],data[5])
        mycursor.execute(sql, val)

        db.commit()
        db.close()

    except Exception as e:
        print('db insert inquiry error', e)
        db.close()



        

        
def board_data():
    board = []
    org = 1

    try :
        
        
        try : 
            # 해당 게시글이 삭제되었을 때
            delete = driver.find_element_by_xpath("//*[@id='contents']/div/div").text

            if delete == '' :
                driver.back()
                pass
        
        except :
            print("해당 게시글이 삭제 되서, 클릭 할 수 없기 때문에 에러 발생")
            
            
            
        case_num = driver.find_element_by_xpath(f"//*[@id='table_kjaa']/tbody/tr[{i}]/td[1]").text     # tr[1] ~ tr[10]
        title = driver.find_element_by_xpath(f"//*[@id='table_kjaa']/tbody/tr[{i}]/td[2]/a").text    # tr[1] ~ tr[10]
        regdate = driver.find_element_by_xpath(f"//*[@id='table_kjaa']/tbody/tr[{i}]/td[4]").text

        board.append(org)
        board.append(case_num)
        board.append(title)
        board.append(regdate)

        
        # 여기서부터 게시글을 클릭하여 데이터내용을가져옴
        driver.implicitly_wait(10)
        board_click = driver.find_element_by_xpath(f"//*[@id='table_kjaa']/tbody/tr[{i}]/td[2]/a").click()    # tr[1] ~ tr[10]
        
        
        try :
            # 해당 게시글이 삭제되었을 때
            delete = driver.find_element_by_xpath("//*[@id='contents']/div/div").text

            if delete == '' :
                driver.back()
                pass

        except :
            print("해당 게시글이 삭제 되서, 클릭 할 수 없기 때문에 에러 발생")



        context = driver.find_element_by_xpath("//*[@id='contents']/div/div/div/div[2]/div[2]").text
        context = context.replace("--------------- 원글 내용 ---------------","")
        context = context.replace("\n","")
            
        board.append(context)

        link = driver.current_url
        board.append(link)
        driver.back()
        print(board)

        insert_inquiry(board)
        return board

            
    except Exception as e:
        print("데이터 추출 Error:",e)
        
        
        
    
# ---------------------------------------- main -------------------------------------------------------------
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
print("------------------- Linux 에서 Crawling 작업을 시작하겠습니다----------------------")
print("==================================================================================")
print("--------------------------------서울중앙지법무사협회--------------------------------")
print("\n\n")



url =  "https://lawlandr.kabl.kr/mod/board/list.do?MID=lawland_onlinecns_01&page=1"
driver.get(url)
lawlandr_board = 1   # 게시글 수



try :    
    while True :
   
        # 페이지네이션 1->2->3->10
        for page in range(3,13):
            scroll_dowmn_page2()
            print("현재 작업중인 page(3이 1페이지를 뜻함) :",page)
            case = driver.find_element_by_xpath(f"//*[@id='contents']/div/div/div[2]/div[3]/ul/li[{page}]").click()
              
            lawlandr_board += 1
            
            
            # 이건 페이지네이션을 위한 확인 용도임
            #print("********************************************page:",page)
            #print("********************************************lawlandr_board:",lawlandr_board)
            
            # 작업중인 페이지 page 12, lawlandr_board 10이면 다음페이지로 이동 (페이지네이션)
            if page == 12 and lawlandr_board == 11:
                next_page = driver.find_element_by_xpath("//*[@id='contents']/div/div/div[2]/div[3]/ul/li[13]/a").click()
                lawlandr_board = 1   # 게시글 수 초기화 --> 다음페이지로 넘겨주기 위해
                
                
            for i in range(1,11): 
                print("현재 작업중인 게시글(1~10) :",i) 
                board_data() 
                print("\n\n\n")



# 가끔식 에러가 뜨는데, 속도가 빨라서 그런거임 
except Exception as e:
    print("데이터 로딩 error",e)


