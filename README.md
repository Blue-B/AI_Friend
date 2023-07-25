# AI_Friend
Python 3.11.3 환경 테스트 완료

1.Command.txt파일의 명령어를 복사하여 터미널에 실행해주세요.
2.https://github.com/VOICEVOX/voicevox_engine/releases/tag/0.14.5 링크로 이동하여 해당하는 플랫폼의 엔진 본체를 다운받아주세요(ex Windows（GPU/CUDA版）)

3.start.bat를 메모장으로 열어 2번째 라인 'OneReality - windows-nvidia' 대신에 다운받은 엔진 폴더를 입력해주세요. (엔진폴더 하위에 run.exe파일이 있어야함)

4.pip install -r requirements 명령으로 필요한 패키지를 전부 설치해주세요.

5.main.py의 ####Key### 주석부분의 api key를 입력해주세요.


# API Keys
client_id,client_secret >> https://developers.naver.com/apps/#/register?api=ppg_n2mt 파파고 api 신청후 발급받은 key를 입력

OpenAi key
key = ''   >> https://platform.openai.com/account/api-keys  openai에서 secret key생성후 입력 

character.ai key
charcter_key = PyAsyncCAI('') >> character.ai 로그인후 개발자도구의 Network탭에서 '/dj-rest-auth/auth0/' 검색후 key값을 복사하여 입력


# 보이스 샘플
기본값 보이스는 영상속에 설정된 'ナースロボ＿タイプＴ'(47) 캐릭터 샘플로 지정되어 있음 

https://voicevox.su-shiki.com/su-shikiapis/#step3
사이트 이동후 'こちら' 클릭하여 apikey 발급
발급받은 key를 STEP 2에 입력후 버튼 클릭
'利用可能なキャラクターIDを取得' 하단 생성된 주소 이동 or 버튼 클릭 
'{"permitted_synthesis_morphing":"ALL"},"name":"小夜/SAYO","speaker_uuid":"a8cc6d22-aad0-4ab8-bf1e-2f843924164a","styles":[{"name":"ノーマル","id":46}]'
voicevox의 원하는 캐릭터 이름을 CTRL + F로 검색후 id에 해당하는 number를 복사

main.py의 83번줄 # VOICEVOX Character number 주석 옆에 speaker 피라미터로 복사한 number값을 붙여넣으면됨




