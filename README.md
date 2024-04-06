# the_lazy_bird

![늦게일어나는새](https://github.com/pollux-choh/the_lazy_bird/assets/108918384/fbb34f57-71c1-4aa3-a926-3a0e3625e538)

열정만큼은 넘치지만, 일어나는 시간은 항상 늦은 새입니다

### '먹을게 없엉....'

당신도 늦게 일어나서 모이를 찾고 있다는거 알아요.

*<li>* python은 해야 하지만, git clone 하는 것도 귀찮을때
*<li>* 내 스팀 라이브러리 처럼 받아놓은 git 소스는 많은데, 실행해본 건 없을때
*<li>* 빌드에러 나면 그냥 vs code 닫고 싶을때  
  
우리 같은 사람들을 위한 python, streamlit, llm 코드 repository
  
  
## 그래도 이건 읽자
> 실행을 내가 해줄 수는 없자나..  
> 
> 나 아직 mac book이 없다구!🤦‍♂️  
> 
> 그래서 윈도우용으로만 준비되어 있어.


### Case 1 : 내컴퓨터가 Windows 일때
<ol>

#### 1) cmd 열기
>... 이정도는 알겠지... 시작 > cmd

#### 2) 폴더 만들고 소스코드 복사하기
```cmd
Microsoft Windows [Version 10.0.22631.3296]
(c) Microsoft Corporation. All rights reserved.

# d 드라이브로 이동
C:\Users\lazy_bird> d:

# 파이썬 연습하는 폴더 만들기
D:\> mkdir ws-python

# ws-python 폴더로 이동
D:\> cd ws-python

# git 소스 코드 복사하기
D:\ws-python> git clone https://github.com/pollux-choh/the_lazy_bird.git

.... (중간생략) ....

# 다운 받은 소스 코드 폴더로 이동
D:\ws-python> cd the_lazy_bird

# 파이썬 가상환경 생성
D:\ws-python\the_lazy_bird> python -m venv venv

# 가상환경으로 전환하기
D:\ws-python\the_lazy_bird> venv\Scripts\activate

# 의존되는 패키지들 설치하기
(venv) D:\ws-pollux\the_lazy_bird> pip install -r requirements.txt

# 분명 pip도 업그레이드 하라는 메세지가 나왔지만, 우리 작고 하찮은 새는 못봤을꺼야
(venv) D:\ws-pollux\the_lazy_bird> python.exe -m pip install --upgrade pip

# streamlit으로 main.py 실행하기
(venv) D:\ws-pollux\the_lazy_bird> streamlit run main\main.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:9999            <-- 이 주소를 웹브라우저에 입력해.
  Network URL: http://192.168.1.xxx:9999      <-- 여기에 너 컴퓨터 IP가 찍혔을꺼야.

```



