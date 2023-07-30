import asyncio
#charcterai
from characterai import PyAsyncCAI
#ai voice
from voicevox import Client
#voice play
import requests, json
import io
import wave
import pyaudio
import time

#speak
import openai
import speech_recognition as sr

#papgao
import urllib.request

###########################################
################## KEY ####################
#naver key
client_id = "" # 개발자센터에서 발급받은 Client ID 값
client_secret = "" # 개발자센터에서 발급받은 Client Secret 값

#OpenAi key
key = ''
openai.api_key = key

#character.ai key
charcter_key = PyAsyncCAI('')
###########################################
###########################################

def papago(encText,jatranslate): #(Text, TRUE OR FALSE)
    if jatranslate == True: #True = auto > ja translation
        data = "source=auto&target=ja&text=" + encText
    elif jatranslate == False:#False = auto > ja translation
        data = "source=auto&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        decode = json.loads(response_body.decode('utf-8'))
        result = decode['message']['result']['translatedText']
        return result
    else:
        return print("Error Code:" + rescode)

#True = whisper, flase = google
usewhisper = True

# speech recognition set-up
r = sr.Recognizer()
mic = sr.Microphone(device_index=0)
r.dynamic_energy_threshold=False
r.energy_threshold = 400

#whisper
def whisper(audio):
    with open('speech.wav','wb') as f:
        f.write(audio.get_wav_data())
    speech = open('speech.wav', 'rb')
    wcompletion = openai.Audio.transcribe(
        model = "whisper-1",
        file=speech
    )
    user_input = wcompletion['text']
    print(f'you:{user_input}')
    return user_input

#voice class
class Voicevox:
    def __init__(self,host="127.0.0.1",port=50021):
        self.host = host
        self.port = port

    def speak(self,text=None,speaker=47): # VOICEVOX Character number

        params = (
            ("text", text),
            ("speaker", speaker) 
        )

        init_q = requests.post(
            f"http://{self.host}:{self.port}/audio_query",
            params=params
        )

        res = requests.post(
            f"http://{self.host}:{self.port}/synthesis",
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(init_q.json())
        )
        audio = io.BytesIO(res.content)
        
        with wave.open(audio,'rb') as f:
            p = pyaudio.PyAudio()

            def _callback(in_data, frame_count, time_info, status):
                data = f.readframes(frame_count)
                return (data, pyaudio.paContinue)

            stream = p.open(format=p.get_format_from_width(width=f.getsampwidth()),
                            channels=f.getnchannels(),
                            rate=f.getframerate(),
                            output=True,
                            stream_callback=_callback)

            # Voice play
            stream.start_stream()
            while stream.is_active():
                time.sleep(0.1)

            stream.stop_stream()
            stream.close()
            p.terminate()

#main
async def main():
    client = charcter_key #Charcter api
    await client.start()

    char = input('Enter CHAR: ')
    chat = await client.chat.get_chat(char)

    history_id = chat['external_id']
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    while True:
        #whisper stt
        with mic as source:
            print("\nListening...")
            r.adjust_for_ambient_noise(source, duration = 0.5) #duration = Ambient noise calibration time.
            audio = r.listen(source)
            try:
                if usewhisper:
                    user_input = whisper(audio)
                else:
                    user_input = r.recognize_google(audio)
                    print(user_input)
            except:
                continue
     
        
        #ai Response Translation
        message = papago(user_input,True)

        data = await client.chat.send_message(
            char, message, history_external_id=history_id, tgt=tgt
        )

        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']

        #ai voice
        print("오디오생성중")
        vv = Voicevox() #host port
        
        print(f"{name}:{text}") #original text
        print(f"{name}:"+papago(text,False)) #translation text
        #voice play
        vv.speak(text=text)

asyncio.run(main())
