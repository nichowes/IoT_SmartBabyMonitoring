import speech_recognition as sr
  
#use the microphone as source for input. Here, we also specify  
#which device ID to specifically look for incase the microphone  
#is not working, an error will pop up saying "device_id undefined"
sample_rate = 48000
chunk_size = 2048

#Initialize the recognizer 
r = sr.Recognizer()

with sr.Microphone(device_index = 2, sample_rate = sample_rate,  
                        chunk_size = chunk_size) as source: 
    #wait for a second to let the recognizer adjust the  
    #energy threshold based on the surrounding noise level 
    r.adjust_for_ambient_noise(source) 
    print("Listen Started")
    #listens for the user's input
    
    audio = r.record(source, duration=4) 
    print("Listen Done")
    try:
        print("Recognition started")
        text = r.recognize_google(audio) 
        print ("you said: " + text)
      
    #error occurs when google could not understand what was said 
      
    except sr.UnknownValueError: 
        print("Google Speech Recognition could not understand audio") 
      
    except sr.RequestError as e: 
        print("Could not request results from Google Speech Recognition service; {0}".format(e)) 