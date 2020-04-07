프로젝트 이름 : 스마트홈

주 개발 언어 : 파이썬 

필요 패키지&모듈 : flask 패키지, bluepy 패키지, RPi.GPIO 모듈, threading 모듈 

모바일 어플리케이션 : 안드로이드 스튜디오 in Java

----------------------------------------------------------------------------------------

아두이노 : 아두이노 스케치로 소스코드를 작성하였습니다. 1초마다 온습도, 소음, 조도 값을 블루투스 모듈에 시리얼 전송하였습니다. 그리고 만약 블루투스 모듈을 통해 값(= 불을 킬 LED 행과 열)이 전송되었을 경우, 값을 읽어 해당 LED의 불을 켰습니다.    

라즈베리파이 : 파이썬으로 소스코드를 작성했습니다. bluepy 패키지를 이용하여 아두이노의 블루투스 모듈과 연결을 하였습니다. 블루투스 연결할 때, 블루투스 모듈의 맥주소를 이용하여 연결을 하였습니다. 웹 서버는 flask를 이용하여 구축하였습니다. 메인 웹 페이지를 출력하는 URL('/')을 제외하고 요청을 받으면 센서값을 업데이트하여 json데이터로 응답을 보내주는 URL('/update')과 요청으로 불을 킬 LED의 행과 열을 입력받아 블루투스로 전송하는 URL('input')을 라우팅하였습니다. 
클라이언트(웹/앱)로부터 요청이 오면 아두이노에서 센서 값을 받아 응답으로 보내주는 경우, 1.5초 동안 블루투스 연결을 통해 센서 값이 들어오길 기다리다가 센서 값이 들어오면 해당 센서 값을 json 데이터로 클라이언트에 보내도록 구현하였습니다.
클라이언트(웹/앱)에서 불을 켤 LED의 행과 열을 전송하는 경우, POST 방식으로 구현을 하였는데 파라미터 값을 읽어 블루투스에 전송하도록 구현하였습니다.

LCD에 센서 값을 출력하는 것은 블루투스에서 센서 값이 들어올 때마다 화면에 값을 출력하도록 구현하였습니다.
4 digit 7 segment display로 현재 시각을 출력하는 것은 time모듈을 사용하였고 실시간으로 시간을 출력하기 위해서 thread를 생성하여 무한루프를 돌렸습니다.

웹 페이지 : html과 자바스크립트를 이용하였고 자바스크립트에서 XMLHttpRequest객체를 이용하여 비동기적으로 request와 response를 구현하였습니다. 또한 setInterval 함수를 사용하여 1.5초 간격으로 센서 값을 요청하도록 구현하였습니다.

안드로이드 앱 : 안드로이드 스튜디오를 사용하였고 AsyncHttpClient 객체를 생성하여 request와 response를 구현하였습니다.
