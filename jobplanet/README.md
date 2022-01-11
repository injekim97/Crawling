# Crawling > jobplanet



* 2021.01.11 : 잡플래닛 "특정기업" 면접 질문 데이터 추출 
* Notice : 해당 소스코드는 특정기업 에서 select box 인 직군 선택(IT/개발), 직책 선택(대졸-사원) 후 크롤링을 함. 그렇기 때문에 기업마다 select box 위치가 다르면 에러 발생 (기업에 맞게 코드 수정 필요)        
* filter 기능을 사용하지 않으려면 모든 기업에서 크롤링 작동함. line 62~ 84 삭제 후 실행 할 것   


# How to use?   
#1. line 23 send_key("ID") 에 jobplanet ID 입력   
#2. line 28 send_key("password") 에 jobplanet password 입력    
#3. line 41 send_key("기업명") 에 면접 데이터 크롤링 할 기업명 입력    