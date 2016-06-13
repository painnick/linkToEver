# linktToEver

원하는 링크를 Evernote에 깔끔하게 저장하는 방법!

![Description imgae](https://raw.github.com/painnick/linkToEver/master/docs/images/linktoever.png)

# 소개

원하는 링크를 Evernote에 깔끔하게 저장하는 방법!

linkToEver는 Instapaper, Readabilty, Evernote를 이용합니다.

1. Instapaper에 원하는 링크를 저장하고
2. Readabilty를 통해 필요한 내용만 깔끔하게 추출한 뒤에
3. Evernote에 저장합니다.

> python을 공부할겸, 그 동안 느꼈던 불편을 해결하는 "생활코딩"으로 만들어 봤습니다.
> 프로그램 구조에 대해 깊게 생각하지 않았고, python을 이용해 간단하게 만드는 것을 목표로 만들었습니다.

# 준비물

이 프로그램을 이용하기 위해서는 아래와 같은 준비물이 필요합니다.

1. Instapaper 계정 : https://www.instapaper.com/에 접속하여 계정을 생성합니다. Instapaper App 또는 링크 등을 통해 원하는 링크를 저장합니다.
2. Instapaper App 등록 : 사용자가 등록한 링크를 linkToEver가 가져오기 위해서는 Instapaper API를 이용합니다. 해당 API를 사용하기 위해서는 https://www.instapaper.com/main/request_oauth_consumer_token에서 App을 등록해야 합니다.
3. Readabilty 계정 생성 : API를 사용하기 위해 계정이 필요합니다.
4. Readabilty App 등록 : https://www.readability.com/settings/account의 API Keys > Parser API Key를 확인합니다.
5. Evernote 계정 생성 : 최종 저장소니까 당연히 필요합니다.
6. Evernote App 등록 : https://dev.evernote.com/에서 "Get Started with the API"를 눌러 App을 등록합니다.

# 설치
```bash
sudo apt-get install python-dev
pip install -r required.txt
```

# 설정
config.ini.sample 파일을 config.ini라는 이름으로 복사합니다. 그리고, 2,4,6항에서 수집한 API 인증 정보를 저장합니다.

# 실행
python \_\_init\_\_.py를 실행합니다.
