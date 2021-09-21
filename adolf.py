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
#DECLARE GLOBAL VARIABLES
duration = 5
fs=16000
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

#VOICE RECOGNITION FOR SUB_ROUTINES
def recognize_voice():
    text = ''

    #PULL IN MICROPHONE
    with sr.Microphone() as source:
    #ADJUST FOR AMBIENT NOISE LEVELS
        r.energy_threshold=50
        r.dynamic_energy_threshold = False

    #CAPTURE AUDIO
        voice = r.listen(source, phrase_time_limit=3)

    #RECOGNIZE WORDS
    try:
        text = r.recognize_google(voice)
        print(text)
    except sr.RequestError:
        playsound('error.wav')
        print("Sorry, the I can't access the Google API...")
    except sr.UnknownValueError:
        print("Unrecognized...")
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
        print("The audio file contains: "+ r.recognize_google(audio))
        text =r.recognize_google(audio)
    except sr.UnknownValueError:
        playsound('error.wav')
        print("Couldn't recognize")
    except sr.RequestError:
        playsound('error.wav')
        speak("I can't access the Google API...")
    return text

def weather_data():
	url = 'https://api.openweathermap.org/data/2.5/weather?id=938694&appid=7a4e25d9875abca76452bd084f8c1ce7&units=metric'
	res = requests.get(url)

	data = res.json()

	temp = data['main']['temp']
	humidity = data['main']['humidity']
	weather = data['weather'][0]['description']

#MAIN FUNTION
def reply(text_version):
	#Identifying action and object
	obj_lst=["desktop",'documents','netflix','music','sound','bastard','chrome','youtube','whatsapp','screen','half','middle','higher','lower','max','increase','decrease','mute','down','up','reduce','unmute','calculator','brightness','time','date','calendar','file','folder','google','downloads','firefox','hey','hello','help','screen','time','date','maximize','minimize','minimise','maximise','hide','close','note','notes','reminder','reminders','task','tasks','have','check','web','online','google','email;','mail','emails','mails','terminal','shell','f***','f******','c***','temperature','humidity','weather','forecast','temp','victron','connect','camera','image','video','videos','picture','photo','pictures','radio','vibes','live','movie','episode','name','surname','history','story']
	action_lst=['run','make','copy','go','list','to','open','move','jarvis','wizard','full','what','read','what is','window','application','volume','audio','take','remember','reminders','tasks','notes','add','search','windows','current','leave','normal','current','play','continue','pause','resume','stop']

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
	if (action == 'what' or action == 'read' or action == 'what is' or action == 'current'):
		if obj == 'time':
			time = datetime.now().time().strftime("%H %M")
			speak("It is now" + time)
		if obj == 'date':
			speak("Todays date is")
			date = datetime.now().strftime("%-d %B %Y")
			speak(date)
		if obj == 'temperature' or obj == 'weather' or obj == 'humidity':
			speak("I'll check for you.")
			url = 'https://api.openweathermap.org/data/2.5/weather?id=938694&appid=7a4e25d9875abca76452bd084f8c1ce7&units=metric'
			res = requests.get(url)
			data = res.json()
			temp = data['main']['temp']
			speak('The temperature is {} degrees celsius'.format(temp))
			
		if obj == 'forecast':
			speak("I'll have a look at the weather for today")
			url = 'https://api.openweathermap.org/data/2.5/weather?id=938694&appid=7a4e25d9875abca76452bd084f8c1ce7&units=metric'
			res = requests.get(url)
			data = res.json()
			humidity = data['main']['humidity']
			weather = data['weather'][0]['description']
			clouds = data['clouds']['all']
			temp_max = data['main']['temp_max']
			temp_min = data['main']['temp_min']
			temp = data['main']['temp']
			real_feel = data['main']['feels_like']
			speak('It looks like there is {} right now'.format(weather))
			speak('With {} percent cloud cover.'.format(clouds))
			speak('The minimum temperature for today is {} degrees'.format(temp_min))
			speak('Currently the temperature is at {} degrees'.format(temp))
			speak('But the real feel is {} degrees'.format(real_feel))
			speak('The maximum temperature for is {} degrees'.format(temp_max))
			speak('Humidity is sitting at {} percent'.format(humidity))
			speak("That is it for now.")

		if obj == 'name' or obj == 'surname':
			speak("My name is Adolf Hitler")
		if obj == 'history' or obj == 'story':
			speak("I was born on the 20th of April 1889")
			speak("As an Austrian-born German politician They say I was the dictator of Germany from 1933 to 1945. I finaly got to power as the leader of the Nazi Party, I became Chancellor in 1933 and then got the title of Führer und Reichskanzler in 1934. During my aparent dictatorship, They say I initiated World War II in Europe by invading Poland on 1 September 1939... That was my land anyway?? haha. Aparantly I was closely involved in military operations throughout the war and was central to the perpetration of the Holocaust, the genocide of about six million Jews and millions of other victims.")
			speak("This is a Joke...")
			speak("You no the truth though... Thank you.")
	#ACTIONS
	if (action == "go" or action == "open" or action == 'to'):
		if obj == "desktop":
			speak("Opening dektop files")
			os.system("nautilus /home/cj/Desktop")
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
	if (action == 'application' or action == 'window'or action == 'windows'):
		if obj == 'maximize' or obj == 'minimize' or obj == 'maximise' or obj == 'minimise':
			os.system("xdotool key super+m")
		if obj == 'hide':
			os.system("xdotool key super+h")
		if obj == 'close':
			os.system("xdotool key super+q")

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
	if (action == 'take' or action == 'remember' or action == 'add'):
		if obj == 'note' or obj == 'notes':
			speak("What do you want me to note down for you?")
			playsound('start.wav')
			note_text = recognize_voice()
			playsound('stop.wav')
			if note_text == '':
				speak("I did not understand. Please say that again.")
				playsound('start.wav')
				note_text = recognize_voice()
				playsound('stop.wav')
			# if "keyword" is not empty
			if note_text != '':
				speak("Sure, adding" + note_text)
				time = datetime.now().time().strftime("%H %M")
				note = (f"{time}. - {note_text}")
				f = open("note.txt", "a+")
				f.write("" + note + ".\n")
				f.close()
		if obj == 'reminder' or obj == 'task' or obj == 'reminders' or obj == 'tasks':
			speak("What do you want me to remember for you?")
			playsound('start.wav')
			reminder_text = recognize_voice()
			playsound('stop.wav')
			if reminder_text == '':
				speak("I did not understand that. Please say that again.")
				playsound('start.wav')
				reminder_text = recognize_voice()
				playsound('stop.wav')
			# if "keyword" is not empty
			if reminder_text != '':
				speak("Sure, I'll remember." + reminder_text)
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
	if (action == 'reminders' or action == 'tasks'):
		if obj == 'have' or obj == 'check':
			speak("I'll have a look")
			f = open("reminder.txt", "r")
			contents = f.read()
			if contents != '':
				speak("Your reminders are: " + contents)
			if contents == '':
				speak("You do not have any reminders")
				speak("Should I add a reminder for you?")
				playsound('start.wav')
				response = recognize_voice()
				playsound('stop.wav')
				if 'yes' in response or 'okay' in response:
					speak("What do you want me to remember for you?")
					playsound('start.wav')
					reminder_text = recognize_voice()
					playsound('stop.wav')
					if reminder_text == '':
						speak("I did not understand that. Please say that again.")
						playsound('start.wav')
						reminder_text = recognize_voice()
						playsound('stop.wav')
					# if "keyword" is not empty
					if reminder_text != '':
						speak("Sure, I'll remember." + reminder_text)
						time = datetime.now().time().strftime("%H %M")
						reminder = (f"{time}. - {reminder_text}")
						f = open("reminder.txt", "a+")
						f.write("" + reminder + ".\n")
						f.close()
				if 'no' in response:
					speak("Fine...")
	#NOTES
	if (action == 'notes'):
		if obj == 'have' or obj == 'check':
			speak("I'll have a look")
			f = open("note.txt", "r")
			contents = f.read()
			if contents != '':
				speak("Your notes are: " + contents)
			if contents == '':
				speak("You do not have any notes")
				speak("Should I add a reminder for you?")
				playsound('start.wav')
				response = recognize_voice()
				playsound('stop.wav')
				if 'yes' in response or 'okay' in response:
					speak("What do you want me to note down for you?")
					note_text = recognize_voice()
					if note_text == '':
						speak("I did not understand that. Please say that again.")
						playsound('start.wav')
						note_text = recognize_voice()
						playsound('stop.wav')
					# if "keyword" is not empty
					if note_text != '':
						speak("Sure, I'll remember." + note_text)
						time = datetime.now().time().strftime("%H %M")
						note = (f"{time}. - {note_text}")
						f = open("note.txt", "a+")
						f.write("" + note + ".\n")
						f.close()
				if 'no' in response:
					speak("Fine...")

	#WEB SEARCH
	if (action == 'search'):
		if obj == 'google' or obj == 'web' or obj == 'online':
			speak("What do you want me to search for?")
			playsound('start.wav')
			keyword = recognize_voice()
			playsound('stop.wav')
			if keyword == '':
				speak("I did not understand")
				speak("Please say that again.")
				playsound('start.wav')
				keyword = recognize_voice()
				playsound('stop.wav')
			if keyword != '':
				url = (f"https://google.com/search?q=" + keyword)
				speak("Here are the search results for " + keyword)
				webbrowser.open(url)

	#LISTING FILES
	if(action =='list'):
		os.system("ls")

	#SOUND SETTINGS
	if (action == 'volume' or action == 'audio'):
		if obj == 'increase' or obj == 'up' or obj == 'higher':
			os.system("amixer -D pulse sset Master 10%+")
		if obj == 'max':
			os.system("amixer -D pulse sset Master unmute")
			os.system("amixer -D pulse sset Master 100%")
		if obj == 'middle' or obj == 'half':
			os.system("amixer -D pulse sset Master unmute")
			os.system("amixer -D pulse sset Master 50%")
		if obj == 'decrease' or obj == 'reduce' or obj == 'lower':
			os.system("amixer -D pulse sset Master 10%-")
		if obj == 'mute' or obj == 'off':
			os.system("amixer -D pulse sset Master mute")
		if obj == 'unmute' or obj == 'on':
			os.system("amixer -D pulse sset Master unmute")

	#RESET VALUES
	action = ''
	obj = ''


#LOOP
while(True):
	wake_word = recognize_voice()
	if "hitler" in wake_word or "adolf" in wake_word:
		speak("What can I do for you?")
		text_version = record_voice()
		reply(text_version)
