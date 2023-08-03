import pyttsx3
import speech_recognition as sr
from pvrecorder import PvRecorder

engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate
engine.setProperty('rate', 150)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

#engine.say("Hello World!")
#engine.say('My current speaking rate is ' + str(rate))
#engine.runAndWait()
#engine.stop()

voices = engine.getProperty('voices')
#print(f'Voices: {voices}' )

for voice in voices:
    print(voice.name)

engine.setProperty('voice', voices[2].id)
#engine.say('What was your problem then?')
engine.runAndWait()

engine.setProperty('voice', voices[3].id)
engine.say('Én vagyok Szabolcs!')
engine.runAndWait()


"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
# engine.save_to_file('Hello World', 'test.mp3')
# engine.runAndWait()



print("RECORDING NOW")

for index, device in enumerate(PvRecorder.get_audio_devices()):
    print(f"[{index}] {device}")


recorder = PvRecorder(device_index=-1, frame_length=512)
r = sr.Recognizer()

mehet = True
while (mehet):

    # Exception handling to handle
    # exceptions at the runtime
    try:


        # audio = []

        try:
            recorder.start()

            while True:
                audio2 = r.listen(recorder)
        except KeyboardInterrupt:
            print("NOW STOP")
            recorder.stop()

            print("REC")
            MyText = r.recognize_google(audio2)
            print("RECOK")
            MyText = MyText.lower()
 
            print("Did you say ", MyText)
            engine.say(MyText)
            engine.runAndWait()

        finally:
            recorder.delete()




    # except sr.UnknownValueError as ext:
    except Exception as ext:
        print(f'unknown error occurred: {ext}')
        mehet = False








# while(1):   
     
#     # Exception handling to handle
#     # exceptions at the runtime
#     try:
         
#         # use the microphone as source for input.
#         with sr.Microphone() as source2:
#             print(source2.__dict__)
             
#             # wait for a second to let the recognizer
#             # adjust the energy threshold based on
#             # the surrounding noise level
#             r.adjust_for_ambient_noise(source2, duration=0.2)
             
#             #listens for the user's input
#             audio2 = r.listen(source2)

#             print("AUDIO")
#             print(audio2)

             
#             # Using google to recognize audio
#             print("REC")
#             MyText = r.recognize_google(audio2)
#             print("RECOK")
#             MyText = MyText.lower()
 
#             print("Did you say ",MyText)
#             engine.say(MyText)
#             engine.runAndWait()

             
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
         
#     # except sr.UnknownValueError as ext:
#     except Exception as ext:
#         print(f'unknown error occurred: {ext}')