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
from playsound import playsound
#DECLARE GLOBAL VARIABLES
duration = 3
fs=16000
N=int(duration*fs)
r = sr.Recognizer()
engine = pyttsx3.init()
""" RATE """
engine.setProperty('rate', 125)
""" VOLUME """
engine.setProperty('volume', 0.8)


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
		r.adjust_for_ambient_noise(source, duration=0.2)

#CAPTURE AUDIO
		voice = r.listen(source)

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
	sd.wait()
	y = (np.iinfo(np.int32).max*(data/np.abs(data).max())).astype(np.int32)
	wavfile.write("input.wav", fs, y)
	AUDIO= ("input.wav")
	r= sr.Recognizer()
	with sr.AudioFile(AUDIO) as source:
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
		speak("Sorry, the I can't access the Google API...")

	return text

#MAIN FUNTION
def reply(text_version):
#Identifying action and object
	obj_lst=["desktop",'documents','netflix','music','sound','bastard','chrome','youtube','whatsapp','screen','max','increase','decrease','mute','down','up','reduce','unmute','calculator','brightness','time','date','calendar','file','folder','google','downloads','firefox','hey','hello','help','screen','time','date','maximize','minimize','minimise','maximise','hide','close','note','reminder','task','have','check','web','online','for','google','emai;','mail','emails','mails','terminal','shell','f***','f******']
	action_lst=['run','make','copy','go','list','to','open','move','jarvis','wizard','full','what','read','what is','window','application','volume','audio','take','remember','reminders','tasks','notes','add','search','windows']

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
	if (action == 'jarvis' or action == 'wizard'):
		if obj == 'hey':
			speak("Yes Sir!?")
		if obj == 'hello':
			speak("Hello Sir!")
		if obj == 'help':
			speak("How can I help you?")

#DATE & TIME
	if (action == 'what' or action == 'read' or action == 'what is'):
		if obj == 'time':
			time = datetime.now().time().strftime("%H %M")
			speak("The time is now" + time)
		if obj == 'date':
			speak("Todays date is")
			date = datetime.now().strftime("%-d %B %Y")
			speak(date)

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
		if obj == 'pictures':
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

#WINDOW CONTROLS
	if (action == 'application' or action == 'window'or action == 'windows'):
		if obj == 'maximize' or obj == 'minimize' or obj == 'maximise' or obj == 'minimise':
			os.system("xdotool key super+m")
		if obj == 'hide':
			os.system("xdotool key super+h")
		if obj == 'close':
			os.system("xdotool key super+q")

#TOGGLE  FULLSCREEN

	if obj == 'f***' or obj == 'f******':
		playsound('astonished.wav')
	if(action =='full'):
		if obj == 'screen':
			os.system("xdotool key F11")

#TAKE REMINDERS & NOTES
	if (action == 'take' or action == 'remember' or action == 'add'):
		if obj == 'note':
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
		if obj == 'reminder' or obj == 'task':
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
		if obj == 'google' or obj == 'web' or obj == 'online' or obj == 'for':
			speak("What do you want me to search for?")
			keyword = recognize_voice()
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
		if obj == 'increase' or obj == 'up':
			os.system("amixer -D pulse sset Master 10%+")
		if obj == 'max':
			os.system("amixer -D pulse sset Master 100%")
		if obj == 'decrease' or obj == 'reduce':
			os.system("amixer -D pulse sset Master 10%-")
		if obj == 'mute':
			os.system("amixer -D pulse sset Master mute")
		if obj == 'unmute':
			os.system("amixer -D pulse sset Master unmute")

#RESET VALUES
	action = ''
	obj = ''


#LOOP
while(True):
	wake_word = recognize_voice()
	if "jarvis" in wake_word or "wizard" in wake_word:
		speak("Yes Sir!?")
		playsound('start.wav')
		text_version = record_voice()
		reply(text_version)
