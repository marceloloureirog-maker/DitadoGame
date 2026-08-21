import pyttsx3
import time

voz = pyttsx3.init()

voz.setProperty("rate", 130)
voz.setProperty("volume", 1.0)

print("Falando primeira palavra...")
voz.say("cachorro")
voz.runAndWait()

time.sleep(2)

print("Falando segunda palavra...")
voz.say("borboleta")
voz.runAndWait()

print("Teste terminado.")