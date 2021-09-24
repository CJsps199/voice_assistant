#IMPORT REQUIRED LIBRARIES
import sounddevice as sd
import numpy as np
from pylab import*
import matplotlib.pyplot as plt
from scipy.io import wavfile
import speech_recognition as sr
import os
import pyttsx3
from time import sleep
from datetime import datetime
import webbrowser
import requests
from playsound import playsound



# from weather import time_slot
#DECLARE GLOBAL VARIABLES
duration = 5
requested_date = ''
fs=8000
N=int(duration*fs)
r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 0.8)
# voices = engine.getProperty('voices')
# print("The available voices are: ")
# print(voices)
# engine.setProperty('voice', voices[12].id)

#SPEAKER
def speak(text):
  engine.say(text)
  engine.runAndWait()

def recognize_request():
    audio = ''
    duration = 5
    data = sd.rec(int(duration*fs),samplerate=fs,channels=1)
    playsound('start.wav')
    sd.wait()
    y = (np.iinfo(np.int32).max*(data/np.abs(data).max())).astype(np.int32)
    wavfile.write("input.wav", fs, y)
    AUDIO= ("input.wav")
    r= sr.Recognizer()
    with sr.AudioFile(AUDIO) as source:
        r.dynamic_energy_threshold = False
        r.energy_threshold=50
        audio = r.record(source)

	#Detecting text using speech processing
    playsound('stop.wav')
    text=""
    try:
        text =r.recognize_google(audio)
        print("The audio file contains: "+ text)
    except sr.UnknownValueError:
        playsound('error.wav')
        print("Couldn't recognize")
    except sr.RequestError:
        playsound('error.wav')
        speak("I can't access the Google API...")
    return text.lower()
#VOICE RECOGNITION FOR SUB_ROUTINES
def recognize_voice():
    audio = ''
    duration = 3
    fs=24000
    data = sd.rec(int(duration*fs),samplerate=fs,channels=1)
    # playsound('start.wav')
    sd.wait()
    y = (np.iinfo(np.int32).max*(data/np.abs(data).max())).astype(np.int32)
    wavfile.write("input.wav", fs, y)
    AUDIO= ("input.wav")
    r= sr.Recognizer()
    with sr.AudioFile(AUDIO) as source:
        r.dynamic_energy_threshold = False
        r.energy_threshold=10
        audio = r.record(source)

	#Detecting text using speech processing
    # playsound('stop.wav')
    text=""
    try:
        text =r.recognize_google(audio)
        print("The audio file contains: " + text)
    except sr.UnknownValueError:
        # playsound('error.wav')
        print("Couldn't recognize")
    except sr.RequestError:
        playsound('error.wav')
        speak("I can't access the Google API...")
    return text.lower()

	#VOICE RECORD FOR MAIN FUNCTION
def record_voice():
	#LISTEN FOR COMMAND
    audio = ''
    data = sd.rec(int(duration*fs),samplerate=fs,channels=1)
    playsound('start.wav')
    sd.wait()
    y = (np.iinfo(np.int32).max*(data/np.abs(data).max())).astype(np.int32)
    wavfile.write("input.wav", fs, y)
    AUDIO= ("input.wav")
    r= sr.Recognizer()
    with sr.AudioFile(AUDIO) as source:
        r.dynamic_energy_threshold = False
        r.energy_threshold=50
        audio = r.record(source)

	#Detecting text using speech processing
    playsound('stop.wav')
    text=""
    try:
        text =r.recognize_google(audio)
        print("The audio file contains: "+ text )
    except sr.UnknownValueError:
        playsound('error.wav')
        print("Couldn't recognize")
    except sr.RequestError:
        playsound('error.wav')
        speak("I can't access the Google API...")
    return text

def weather_forecast_two(date_asked):
	requested_date = date_asked.lower()
	day_cur = (datetime.now().date().strftime('%u'))
	day_cur_int = int(day_cur)
	day_req_int = 0
	local_time = datetime.now().time().strftime('%H')
	lt_int = int(local_time)

	if 'monday' in requested_date:
		day_req_int = 1
		
	if 'tuesday' in requested_date:
		day_req_int = 2
	
	if 'wednesday' in requested_date:
		day_req_int = 3

	if 'thursday' in requested_date:
		day_req_int = 4
		
	if 'friday' in requested_date:
		day_req_int = 5
		
	if 'saturday' in requested_date or 'weekend' in requested_date:
		day_req_int = 6

	if 'sunday' in requested_date:
		day_req_int = 7
		
	if 'tomorrow' in requested_date:
		day_req_int = int(day_cur_int + 1)

	if 'today' in requested_date:
		day_req_int = day_cur_int
		
	if day_req_int >= day_cur_int:
		day_res = int((day_req_int - day_cur_int) * 8)
		time_stamp = int((day_res - (lt_int / 3) + 4))

    #Following week
	if day_cur_int >= day_req_int:
		day_res = int(((day_req_int + 7) - day_cur_int) * 8)
		time_stamp = int((day_res - (lt_int / 3) + 4))

	time_stamp_corrected = int(time_stamp)
	if time_stamp_corrected >= 40:
		speak("I can fetch the forecast for a maximum of 5 days with the current API.")
		time_stamp_corrected = 39

	return time_stamp_corrected
	
def NewsFromBBC(news_category):
	cat_lst=['business','health','sports','science','technology','entertainment','general']
	cat=""
	for i in news_category.split():
		i=i.lower()
		if i in cat_lst:
			cat = i

		query_params = {
			"source": "bbc-news",
			"language": "en",
		   	"sortBy": "top",
		   	"apiKey": "14566905717a4e8e8697766ce4a9e48d",
			"category": cat
			}
		main_url = " https://newsapi.org/v2/top-headlines"
 
		# fetching data in json format
		res = requests.get(main_url, params=query_params)
		open_bbc_page = res.json()
 
    	# getting all articles in a string article
		article = open_bbc_page["articles"]
 
   	 	# empty list which will
    	# contain all trending news
		results = []
     
		for ar in article:
			results.append(ar["title"]) 
			results_int = int(len(results))
			result_length = int(results_int / 2)
		for i in range(result_length):
         
        # printing all trending news
		    result_obo = (i + 1, results[i])
		    speak(result_obo)
    	# BBC news api
    	# following query parameters are used
    	# source, sortBy and apiKey
	speak("That is it for now.")	

#MAIN FUNTION
def reply(text_version):
	#Identifying action and object
	obj_lst=['time','date','temperature','temp','forecast','weather','news','name','surname','history','story','desktop','documents','music','videos','downloads','pictures','picture','calculator','firefox','chrome','google','youtube','whatsapp','netflix','email','mail','emails','mails','terminal','shell','victron','connect','camera','radio','vibes','live','window','windows','app','application','screen','movie','episode','note','notes','reminder','reminders','task','tasks','photo','image','video','google','web','online','volume','audio','sound']
	action_lst=['what',"what's",'read','current','latest','go','open','activate','show','close','minimise','minimize','maximise','maximize','hide','show','full','leave','normal','play','continue','pause','resume','stop','take','remember','add','capture','have','check','search','list','increase','higher','up','decrease','lower','down','reduce','mute','off','none','unmute','on','activate','max','maximum','middle','half','medium']

	#SPLIT LOWER AND UPPER WORDS?
	action =""
	obj =""
	for i in text_version.split():
		i=i.lower()
		if i in obj_lst:
			obj= i
		if i in action_lst:
			action=i

	#STRIP THE OBJECTS?
	obj = obj.strip()
	action = action.strip()

	#DEBUGGING
	print("Action: " + action)
	print("Object: " + obj)

	#NAVIGATION
	

	#DATE & TIME & WEATHER
	if (action == 'what'or action == "what's" or action == 'read' or action == 'current' or action == 'latest'):
		if obj == 'time':
			time = datetime.now().time().strftime("%H %M")
			speak("It is now" + time)
		if obj == 'date':
			speak("Todays date is")
			date = datetime.now().strftime("%-d %B %Y")
			speak(date)
		if obj == 'temperature' or obj == 'temp':
			speak("I'll check for you.")
			url = 'https://api.openweathermap.org/data/2.5/weather?id=938694&appid=7a4e25d9875abca76452bd084f8c1ce7&units=metric'
			res = requests.get(url)
			data = res.json()
			temp = data['main']['temp']
			humidity = data['main']['humidity']
			pres = data['main']['pressure']
			speak('The temperature now is {} degrees celsius'.format(temp))
			speak('Humidity is {}'.format(humidity))
			speak(' And the air pressure is currently {} hecto pascal'.format(pres))
			
		if obj == 'forecast' or obj == 'weather':
			#weather_forecast()
			speak("For which date sir?")
			date_asked = record_voice()
			time_stamp_corrected = weather_forecast_two(date_asked)
			speak("I'll check for you")
			url = 'https://api.openweathermap.org/data/2.5/forecast?id=938694&units=metric&appid=fb1fd2490f1a121fcb5c19575ca6e89f'
			res = requests.get(url)
			data = res.json()
			humidity = data['list'][time_stamp_corrected]['main']['humidity']
			weather = data['list'][time_stamp_corrected]['weather'][0]['description']
			clouds = data['list'][time_stamp_corrected]['clouds']['all']
			temp = data['list'][time_stamp_corrected]['main']['temp']
			real_feel = data['list'][time_stamp_corrected]['main']['feels_like']
			pres = data['list'][time_stamp_corrected]['main']['pressure']
			ts = data['list'][time_stamp_corrected]['dt']
			time = (datetime.utcfromtimestamp(ts).strftime('%H %M'))
			day_of_forcast = (datetime.utcfromtimestamp(ts).strftime('%A'))
			speak('The weather forecast for {} ...'.format(day_of_forcast))
			speak('At {}'.format(time))
			speak('Looks like  {} '.format(weather))
			speak('With {} percent cloud cover.'.format(clouds))
			speak('The temperature will be {} degrees'.format(temp))
			speak('But the real feel {} degrees'.format(real_feel))
			speak('Humidity will be sitting at {} percent'.format(humidity))
			speak('The air pressure will be {} hecto pascal'.format(pres))
			speak("Have a great day!")

		if obj == 'news':
			speak("For which category do you want the news?")
			news_category = recognize_request()
			NewsFromBBC(news_category)
			
		if obj == 'name' or obj == 'surname':
			speak("My name is Adolf Hitler")
		if obj == 'history' or obj == 'story':
			speak("I was born on the 20th of April 1889")
			speak("As an Austrian-born German politician They say I was the dictator of Germany from 1933 to 1945. I finaly got to power as the leader of the Nazi Party, I became Chancellor in 1933 and then got the title of Führer und Reichskanzler in 1934. During my aparent dictatorship, They say I initiated World War II in Europe by invading Poland on 1 September 1939... That was my land anyway?? haha. Aparantly I was closely involved in military operations throughout the war and was central to the perpetration of the Holocaust, the genocide of about six million Jews and millions of other victims.")
			speak("This is a Joke...")
			speak("You no the truth though... Thank you.")
	#ACTIONS
	if (action == "go" or action == "open" or action == 'activate' or action == 'show'):
		if obj == "desktop":
			speak("Showing the desktop")
			os.system("xdotool key super+d")
		if obj == 'documents':
			speak("Opening documents")
			os.system("nautilus /home/cj/Documents")
		if obj == 'music':
			speak("Opening music")
			os.system("nautilus /home/cj/Music")
		if obj == 'videos':
			speak("Opening videos")
			os.system("nautilus /home/cj/Videos")
		if obj == 'downloads':
			speak("Opening downloads")
			os.system("nautilus /home/cj/Downloads")
		if obj == 'pictures' or obj == 'picture':
			speak("Opening pictures")
			os.system("nautilus /home/cj/Pictures")
		if obj == 'calculator':
			speak("Opening calculator")
			os.system("gnome-calculator")
		if obj == 'firefox':
			speak("Opening Firefox")
			os.system("firefox")
		if obj == 'chrome' or obj == 'google':
			speak("Opening browser")
			os.system("xdotool key super+b")
		if obj == 'youtube':
			speak("Opening YouTube")
			os.system("xdotool key super+shift+y")
		if obj == 'whatsapp':
			speak("Opening WhatsApp")
			os.system("xdotool key super+w")
		if obj == 'netflix':
			speak("Opening NetFlix")
			os.system("xdotool key super+shift+n")
		if obj == 'email' or obj == 'mail' or obj == 'emails' or obj == 'mails':
			speak("Opening mails")
			os.system("xdotool key super+e")
		if obj == 'terminal' or obj == 'shell':
			speak("Opening terminal")
			os.system("xdotool key super+t")
		if obj == 'victron' or obj == 'connect':
			speak("Opening Vitron Connect")
			os.system("xdotool key super+9")
		if obj == 'camera':
			speak("Opening Camera, Say Cheese...")
			os.system("/usr/bin/flatpak run --branch=stable --arch=x86_64 --command=cheese org.gnome.Cheese")
		if obj == 'radio' or obj == 'vibes' or obj == 'live':
			webbrowser.open_new_tab('https://vibezlive.radioca.st/stream')
			speak("Sure thing.")
			sleep(1)
			os.system("xdotool key space")
			os.system("amixer -D pulse sset Master 30%")
			os.system("xdotool key super+h")
		

	#WINDOW CONTROLS
	if (action == 'close'):
		if obj == 'window' or obj == 'windows' or obj == 'app' or obj == 'application':
			os.system("xdotool key super+q")
		
	if (action == 'minimise' or action == 'minimize' or action == 'maximise' or action == 'maximize'):
		if obj == 'window' or obj == 'windows' or obj == 'app' or obj == 'application':
			os.system("xdotool key super+m")

	if (action == 'hide' or action == 'show'):
		if obj == 'window' or obj == 'windows' or obj == 'app' or obj == 'application':
			os.system("xdotool key super+h")

	#TOGGLE  FULLSCREEN

	if obj == 'f***' or obj == 'f******' or obj == 'c***':
		playsound('astonished.wav')
	if(action =='full' or action == 'leave' or action == 'normal'):
		if obj == 'screen':
			os.system("xdotool key F11")

	if(action =='play' or action == 'continue' or action == 'pause' or action == 'resume' or action == 'stop'):
		if obj == 'movie' or 'episode':
			os.system("xdotool key space")
		if obj == 'radio' or obj == 'vibes' or obj == 'live':
			webbrowser.open_new('https://vibezlive.radioca.st/stream')
			speak("Sure thing.")
			sleep(1)
			os.system("xdotool key space")
			os.system("amixer -D pulse sset Master 30%")
			os.system("xdotool key super+h")

	#TAKE REMINDERS & NOTES
	if (action == 'take' or action == 'remember' or action == 'add' or action == 'capture'):
		if obj == 'note' or obj == 'notes':
			speak("What do you want me to note down for you?")
			note_text = recognize_request()
			if note_text == '':
				speak("I did not understand. Please say that again.")
				note_text = recognize_request()
			# if "keyword" is not empty
			if note_text != '':
				speak("Sure, adding" + note_text)
				time = datetime.now().time().strftime("%H %M")
				note = (f"{time}. - {note_text}")
				f = open("note.txt", "a+")
				f.write("" + note + ".\n")
				f.close()
		if obj == 'reminder' or obj == 'reminders' or obj == 'task' or obj == 'tasks':
			speak("What do you want me to remember for you?")
			reminder_text = recognize_request()
			if reminder_text == '':
				speak("I did not understand that. Please say that again.")
				reminder_text = recognize_request()
			# if "keyword" is not empty
			if reminder_text != '':
				speak("Sure, I'll remember" + reminder_text)
				time = datetime.now().time().strftime("%H %M")
				reminder = (f"{time}. - {reminder_text}")
				f = open("reminder.txt", "a+")
				f.write("" + reminder + ".\n")
				f.close()
		if obj == 'picture' or obj == 'photo' or obj == 'image' or obj == 'video':
			speak("Opening Camera, Say Cheese...")
			os.system("/usr/bin/flatpak run --branch=stable --arch=x86_64 --command=cheese org.gnome.Cheese")

	#CHECK & READ
	#REMINDERS
	if (action == 'have' or action == 'check'):
		if obj == 'reminders' or obj == 'reminder' or obj == 'tasks' or obj == 'task':
			speak("I'll have a look")
			f = open("reminder.txt", "r")
			contents = f.read()
			if contents != '':
				speak("Your reminders are: " + contents)
			if contents == '':
				speak("You do not have any reminders")
				speak("Should I add a reminder for you?")
				response = recognize_request()
				if 'yes' in response or 'okay' in response:
					speak("What do you want me to remember for you?")
					reminder_text = recognize_request()
					if reminder_text == '':
						speak("I did not understand that. Please say that again.")
						reminder_text = recognize_request()
					# if "keyword" is not empty
					if reminder_text != '':
						speak("Sure, I'll remember" + reminder_text)
						time = datetime.now().time().strftime("%H %M")
						reminder = (f"{time}. - {reminder_text}")
						f = open("reminder.txt", "a+")
						f.write("" + reminder + ".\n")
						f.close()
				if 'no' in response:
					speak("Fine...")

		if obj == 'note' or obj == 'notes':
			speak("I'll have a look")
			f = open("note.txt", "r")
			contents = f.read()
			if contents != '':
				speak("Your notes are: " + contents)
			if contents == '':
				speak("You do not have any notes")
				speak("Should I add a note for you?")
				response = recognize_request()
				if 'yes' in response or 'okay' in response:
					speak("What do you want me to note down for you?")
					note_text = recognize_request()
					if note_text == '':
						speak("I did not understand that. Please say that again.")
						note_text = recognize_request()
					# if "keyword" is not empty
					if note_text != '':
						speak("Sure, I'll remember" + note_text)
						time = datetime.now().time().strftime("%H %M")
						note = (f"{time}. - {note_text}")
						f = open("note.txt", "a+")
						f.write("" + note + ".\n")
						f.close()
				if 'no' in response:
					speak("Fine...")
	#NOTES
	#if (action == 'notes'):
		

	#WEB SEARCH
	if (action == 'search'):
		if obj == 'google' or obj == 'web' or obj == 'online':
			speak("What do you want me to search for?")
			keyword = recognize_request()
			if keyword == '':
				speak("I did not understand")
				speak("Please say that again.")
				keyword = recognize_request()
			if keyword != '':
				url = (f"https://google.com/search?q=" + keyword)
				speak("Here are the search results for " + keyword)
				webbrowser.open(url)

	#LISTING FILES
	if(action =='list'):
		os.system("ls")

	#SOUND SETTINGS
	if (action == 'increase' or action == 'higher' or action == 'up'):
		if obj == 'volume' or obj == 'audio' or obj == 'sound':
			os.system("amixer -D pulse sset Master 10%+")

	if (action == 'decrease' or action == 'lower' or action == 'down' or action == 'reduce'):
		if obj == 'volume' or obj == 'audio' or obj == 'sound':
			os.system("amixer -D pulse sset Master 10%-")

	if (action == 'mute' or action == 'off' or action == 'none'):
		if obj == 'volume' or obj == 'audio' or obj == 'sound':
			os.system("amixer -D pulse sset Master mute")

	if (action == 'unmute' or action == 'on' or action == 'activate'):
		if obj == 'volume' or obj == 'audio' or obj == 'sound':
			os.system("amixer -D pulse sset Master unmute")

	if (action == 'max' or action == 'maximum' or action == 'full'):
		if obj == 'volume' or obj == 'audio' or obj == 'sound':
			os.system("amixer -D pulse sset Master unmute")
			os.system("amixer -D pulse sset Master 100%")

	if (action == 'middle' or action == 'half' or action == 'medium'):
		if obj == 'volume' or obj == 'audio' or obj == 'sound':
			os.system("amixer -D pulse sset Master unmute")
			os.system("amixer -D pulse sset Master 50%")

	#RESET VALUES
	action = ''
	obj = ''


#LOOP
while(True):
	wake_word = recognize_voice()
	if "hitler" in wake_word or "adolf" in wake_word:
		text_version = record_voice()
		reply(text_version)
