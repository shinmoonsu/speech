import speech_recognition as sr
from pygame import mixer,time
from gtts import gTTS
import re,os,sys,urllib.parse

order = {
    'naverSearch'   :   {
        'reg'   :   '네이버|검색',
        'type'  :   'search',
        'run'   :   'https://search.naver.com/search.naver?query=[SEARCH_KEYWORD]'
    },
    'naverSearch'   :   {
        'reg'   :   '네이버|메인 화면',
        'type'  :   'external',
        'run'   :   'https://naver.com'
    },
    'YOUTUBE'   :   {
        'reg'   :   '유튜브|검색',
        'type'  :   'search',
        'run'   :   'https://www.youtube.com/results?search_query=[SEARCH_KEYWORD]'
    },
    'GOOGLE 지도'   :   {
        'reg'   :   '구글지도|검색',
        'type'  :   'search',
        'run'   :   'https://www.google.co.kr/maps/place/[SEARCH_KEYWORD]'
    },
    'GOOGLE'   :   {
        'reg'   :   '구글|검색',
        'type'  :   'search',
        'run'   :   'https://www.google.com/search?q=[SEARCH_KEYWORD]'
    },
    
    'moneybook'   :   {
        'reg'   :   '네이버|가계부',
        'type'  :   'external',
        'run'   :   'https://moneybook.naver.com/mybook/write.nhn'
    }

    
}
class speech():
    # def whatMean():
    mp = "d:/audio.mp3" 
    data = ""
    mix = mixer
    
    def url(self, target):
        os.system('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" '+target)

    def search(self, order_key):
        print('naverSearch', self.data)
        searchWord = re.sub(order[order_key]['reg'],'',self.data)
        searchWord = re.sub('에서 ','', searchWord)
        searchWord = urllib.parse.quote_plus(searchWord.strip())
        
        print(order[order_key]['reg'],self.data, searchWord)
        
        target = re.sub('\[SEARCH_KEYWORD\]',searchWord, order[order_key]['run'])
        print(target)
        self.url(target)
        


    def whatMean(self):
        
        # print(self.data)
        # print(mean, len(mean))
        
        for k in order:
            print(self.data)
            p = re.compile(order[k]['reg'], re.I)
            mean = p.findall(self.data)
            print(order[k]['reg'])
            if len(mean)>=2:
                self.speak("Ok!! Connecting")
                if order[k]['type'] == 'external':
                    self.url(order[k]['run'])
                elif order[k]['type'] == 'search':
                    self.search(k)
                else:
                    getattr(self, order[k]['run'])()

                self.data = ""
                break

    def recordAudio(self):
    # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # print("Say something!")
            audio = r.listen(source)

        try:
            # Uses the default API key
            # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            self.data = r.recognize_google(audio,language='ko-kr')
            # print(self.data.encode('cp949'))
            self.whatMean()
            
        except sr.UnknownValueError:
            # return
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
    def speak(self, audioString):
        print(audioString)
        # self.mix.music.set_endevent()
        # tts = gTTS(text=audioString, lang='en')
        # tts.save(self.mp)
        self.tell()
        # os.system("mpg321 audio.mp3")
    
    def tell(self):
        self.mix.init()
        self.mix.music.load(self.mp)
        self.mix.music.play()
        clock = time.Clock()
        while self.mix.music.get_busy():
            clock.tick(30)
        self.mix.quit()
        

if __name__ == '__main__':
    
    while True:
        sp = speech()
        sp.recordAudio()

