# Crawling > instagram
인턴 다니는 회사에서 인플루언서의 팔로워 팔로잉 수를 매일 저장하며, 게시글에 어떤 사람이 유입되는지를 알기 위한 프로젝트 


***
# instagram crawling project process 1 

1일 1회 크롤링 [최종목표]
- ip당 400번 크롤링 제한 
 
- Master (닉네임,게시물,팔로워,팔로우,내용)
- detail(게시글)  



04.26 인스타 닉네임, 게시물 수 추출
https://www.instagram.com/ID



* 조건1 해당 게시물이 그대로여도, 
★★★★ 닉네임 팔로워도 팔로우나 , 내용이 바뀔 수 있음 ★★★★   
-> 매일 1일 1크롤링해서 값을 저장해야함.  


* 조건2: 게시물의 갯수가 예(이전: 222) , 오늘(223)일 때 즉, 높을경우에 크롤링을 시작  
-> 그대로면 크롤링 X   


* 조건3: 팔로워/팔로우 수가 예를들어 1045명인데 1044나 1046 줄거나 늘었을 때, 닉네임 값을 가져와야함   
팔로워를 눌러서 닉네임에 F12 개발자모드로 XPATH 클릭   
이름값만 추출하면됨 예)  darumkorea 라면,  darumkorea를 가져오면된다.   



* 조건4: 사진을 한번 클릭후에 오른쪽 3시방향 >로 클릭(좌우 스크롤)   
게시글(posting)-> 답글(자기가 단것), 상대방이 단것 // 좋아요 갯수, 좋아요 누가 눌렀는지 전부 저장  



* 조건5: 동영상을 한번 클릭후에 오른쪽 3시방향 >로 클릭(좌우 스크롤)   
게시글(posting)-> 답글(자기가 단것), 상대방이 단것 // 조회수 갯수랑 조회수를 클릭하면 , 좋아요 수가 나오는데 여기선 숫자만 추출  

 



***
# instagram crawling project process 2


------------ Data path ------------------   
Which directory should be used by logstash and its plugins  
for any persistent needs. Defaults to LOGSTASH_HOME/data  
path.data: /var/lib/logstash (기본 값임)  



1번 여기서수정  
1. logstash 를 새로 mount 된 disk로 바꾸기  
-> path.data: /datadrive로 변경 OK

2. elk 뛰우기(Linux)   
-> 뛰움 OK   

3. 내 로컬에 apache 설치 후 web 띄우기  
-> 띄움 OK 
-> 그 이야기는 log file이 쌓인다는 뜻 
-> 로그 파일 경로 : logs/access.log  



4. 제 로컬에 logstash 깔려있음  
-> pc logstash.conf파일을 apache log 디렉토리로 보내서 체크  


5. kibana 인덱스 확인  
=> 4번되면 가능.  



***
* 2021.11.15 : 인스타그램 (대체 로그인: 페이스북 포함)    
-> 21.05.12에 위의 조건1-5를 포함한 최종 구현 파일 3개 업로드     
-> [Facebook] 파일명(CSV) -> facebook으로 대체 로그인 후 인플루언서 정보를 CSV로 저장 
-> [instgram] 파일명(CSV) -> instgram으로 로그인 후 인플루언서 정보를 CSV로 저장 
-> 0512_1800 [최종] - CSV 파일을 읽어와서 비교 -> 위 두가지 중 하나를 실행하여 CSV로 저장된 파일을 읽어와서 현재의 인플루언서와 비교 




<img src = "https://blog.kakaocdn.net/dn/kZ3mW/btq3y7iSTwG/0yVRLS5U678viEpKs9ePg0/img.png" width="100%" height="100%">   
-> CSV로 저장된 값 (닉네임, 게시글 수, 팔로워 수, 팔로잉 수, 대쉬보드)   
　 
　
　






<img src = "https://blog.kakaocdn.net/dn/rsoid/btq4J8NJre9/Dx76khKrv1GIhqL3rUdeNk/img.png" width="100%" height="100%">   
-> CSV로 저장된 값 (게시글 내용 및 댓글, 해당 게시글 좋아요 수, 좋아요 누른 사람의 닉네임)  