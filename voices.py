import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[12].id)
engine.setProperty('rate', 160)
engine.say("Hello, this is a test of my voice to see if you will like it or not. Please let me know. Is there anything I can help with? ")
engine.runAndWait()
engine.stop()
