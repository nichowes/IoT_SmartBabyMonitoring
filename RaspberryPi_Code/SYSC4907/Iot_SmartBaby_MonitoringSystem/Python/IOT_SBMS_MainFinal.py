import serial
from io import StringIO
import csv
from time import sleep
from picamera import PiCamera
from pyrebase import pyrebase
import datetime
import time
import pygame
from random import randrange
import speech_recognition as sr
import pygame
import time
from pprint import pformat as pf
from pyHS100 import Discover, SmartPlug
from datetime import datetime

# Database Configuration Code Will Never Change
config = {
    "apiKey": "AIzaSyBLwvIEA9__jCTxCKBXJaeHjztbFtyTrfk",
    "authDomain": "iotsmartbabymonitoringcloud.firebaseapp.com",
    "databaseURL": "https://iotsmartbabymonitoringcloud.firebaseio.com",
    "storageBucket": "iotsmartbabymonitoringcloud.appspot.com",
    "projectId": "iotsmartbabymonitoringcloud",
    "messagingSenderId": "390483925787",
    "serviceAccount": "./iotsmartbabymonitoringcloud-0421414daa1d.json"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("samyibrahim661@gmail.com", "iotTestUser")
db = firebase.database()

# Arduino Serial Port Configuration
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 4)

# Camera Configuration: (set to true once working)
useCamera = False

def insertTest(name, age, height, weight):
  data = {"name": name, "age": age, "height": height, "weight": weight}
  db.child("users").child(name).set(data, user['idToken'])
  print("Insert Successfull")

def insertSensor(cameraTriggered, microphoneTriggered, temperature, timestamp):
  data = {"cameraTriggered": cameraTriggered, "microphoneTriggered": microphoneTriggered,
          "temperature": temperature, "timestamp": timestamp}
  db.child("SensorData").child(timestamp).set(data, user['idToken'])
  print("Insert to Sensor Table Successfull")
  
def getTemperatureLimit():
    temp = db.child("Settings").child("temperatureLimit").get(user['idToken'])
    return temp.val()

def incrementTotalCries():
    total = db.child("Statistics").child("numberOfCries").get(user['idToken'])
    value = total.val()
    value = value + 1
    data = {"numberOfCries": value}
    db.child("Statistics").update(data, user['idToken'])

def triggerBabyCrying(trigger):
  data = {"trigger": trigger}
  db.child("BabyCrying/trigger").update(data, user['idToken'])
  
def updateLatestCrying(latest):
  data = {"latestWakeup": latest}
  db.child("Statistics").update(data, user['idToken'])

def updateLatestWorking(latest):
  data = {"latestWorkingMethod": latest}
  db.child("Statistics").update(data, user['idToken'])

def updateTempCausingCry(latest):
  data = {"tempCausingCry": latest}
  db.child("Statistics").update(data, user['idToken'])

def triggerMicrophone(trigger):
  data = {"trigger": trigger}
  db.child("SensorTrigger/microphone").update(data, user['idToken'])
  
def triggerTemp(trigger):
  data = {"trigger": trigger}
  db.child("SensorTrigger/temperature").update(data, user['idToken'])
  
def triggerCamera(trigger):
  data = {"trigger": trigger}
  db.child("SensorTrigger/camera").update(data, user['idToken'])
  
def playMusic():
    print("Playing Music")
    pygame.mixer.init()
    pygame.mixer.music.load("babyLulaby20sec.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
def isBabyCrying():
    #Method
    sample_rate = 48000
    chunk_size = 2048
    result = False
    #Initialize the recognizer 
    r = sr.Recognizer()

    with sr.Microphone(device_index = 2, sample_rate = sample_rate,  
                            chunk_size = chunk_size) as source: 
        #wait for a second to let the recognizer adjust the  
        #energy threshold based on the surrounding noise level 
        r.adjust_for_ambient_noise(source) 
        print("Say Something")
        #listens for the user's input 
        audio = r.record(source, duration=2) 
          
        try: 
            text = r.recognize_google(audio) 
            print ("you said: " + text)
    
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio")
            result = True
          
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return result
    
def babyCriesAgain():
    print("BABY CRIES AGAIN METHOD")
    result = False
    line = arduino.readline()  
    f = StringIO(line.decode("utf-8") )
    hold = f.getvalue()
    exitInd=False
    
    print("BABY CRYING LOOP")
    line = arduino.readline()
    f = StringIO(line.decode("utf-8") )
    hold = f.getvalue()
    exitInd=True
    if "HIGH" in hold:
        result = True
    return result            

def getCurrentTimeStamp():
    babyCryTime = datetime.now()
    timeStamp = babyCryTime.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    print("Timestamp is: " + timeStamp)
    return timeStamp

def parseIP(output):
    pluglocalIP = output.partition("192.168.")[1] + output.partition("192.168.")[2].partition(" ")[0]
    print(pluglocalIP)
    return pluglocalIP

def parseName(output):
    plugName = output.partition("(")[2].partition(")")[0]
    print(plugName)
    return plugName

def plugInfo(name):
    plug = SmartPlug(deviceList[name])
    print("Hardware: %s" % pf(plug.hw_info))
    print("Full sysinfo: %s" % pf(plug.get_sysinfo()))

    print("Current state: %s" % plug.state)
    
def plugTurnOn(name):
    plug = SmartPlug(deviceList[name])
    plug.turn_on()

def plugTurnOff(name):
    plug = SmartPlug(deviceList[name])
    plug.turn_off()

def isPlugOn(name):
    plug = SmartPlug(deviceList[name])
    if (plug.state == "ON"):
        return True
    return False

def discoverDevices():
    deviceList = {
        }
    for dev in Discover.discover().values():
        print(dev)
        output = str(dev)
        deviceList[parseName(output)] = parseIP(output)
    
    return deviceList

soundTriggered = False
attemptedLullaby = False
attemptedToy = False
temperatureLowTrigger = False
temperatureHighTrigger = False
babyPersistedCrying = False

deviceList = discoverDevices()

while(1):
    if(arduino.in_waiting > 0):
        microphoneTrigger = False
        tempLimit = getTemperatureLimit()
        line = arduino.readline()
        
        readData = []
        
        f = StringIO(line.decode("utf-8") )
        hold = f.getvalue()
        s = line.decode("utf-8")
        sString = ""
           
        if "HIGH" in hold:
            microphoneTrigger = True
        
            
        text1 = s.split(',')
        print(text1)
        
        avg = 0;
        index = 0;
        for i in range(16):
            if (("HIGH" in text1[i]) or ("LOW" in text1[i]) or ("\r\n" in text1[i]) or ("Invalid" in text1[i])):
                break;
            else:
                index += 1
                avg += float(text1[i])

        if avg>0:
            if index>0:
                avg = avg/index
                
        print("Average: " + str(avg))
        print("Temperature limit: " + str(tempLimit))
        cameraTrigger = False
        if(useCamera==True):
            camera = PiCamera()
            camera.resolution = (1024,768)
            camera.start_preview()
            sleep(5)
            camera.capture('testing.jpg')
            # Use Open CV and Analyse the image (Add Logic below and set cameraTrigger to true
        
        currIndex = 0
        
        
        
        if (float(avg) > float(tempLimit)):
            temperatureHighTrigger = True
            triggerTemp(1)
            print("TEMPERATURE HIGH TRIGGER")
        elif (temperatureHighTrigger == True and not avg == 0):
            temperatureHighTrigger = False
            print("RESET EMPERATURE HIGH TRIGGER")
        
        #if (float(avg) < float(tempLimit)):
            #temperatureLowTrigger = True
            #triggerTemp(1)
            #print("TEMPERATURE LOW TRIGGER")
        #elif (temperatureLowTrigger):
            #temperatureLowTrigger = False
            #print("RESET TEMPERATURE LOW TRIGGER")
            
            
        if(microphoneTrigger==True):
            triggerMicrophone(1)
            soundTriggered = isBabyCrying()
            print("MIC TRIGGER")
            
            
        if(cameraTrigger==True):
            triggerCamera(1)
            print("CAMERA TRIGGER")
            
        tellParents = False
        
        if((soundTriggered == True) and (microphoneTrigger == True)):
           # Play Lulaby
           
           if (attemptedLullaby == False):
               playMusic()
               currIndex = currIndex +1
               attemptedLullaby = True
               incrementTotalCries()
               updateLatestCrying(getCurrentTimeStamp())
               if(float(avg)>0):
                   updateTempCausingCry(float(avg))
               if(babyCriesAgain() == False):
                   print("Baby didnt cry again after Lulaby")
                   updateLatestWorking("Lulaby")
                   attemptedLullaby = False
               
           elif(attemptedToy == False):
               # Play Toy
               attemptAgain = babyCriesAgain()
               if(attemptAgain):
                   print("Toy Attempted")
                   plugTurnOn("Toy")
                   atemptedToy = True
               if(babyCriesAgain()==True):
                   tellParents = True
                   
               else:
                   print("Baby didnt cry again after Lullaby")
                   updateLatestWorking("Toy")
                   attemptedLullaby = False
                   attemptedToy = False
               
        if(tellParents == True):
           currIndex = 0
           attemptedLullaby = False
           attemptedToy = False
           triggerBabyCrying(1)
           print("TRIGGER DB")
        
        
        if (temperatureHighTrigger and not isPlugOn("Fan")):
            print("Attempt to turn fan on")
            plugTurnOn("Fan")
            
        elif (temperatureHighTrigger == False and isPlugOn("Fan")):
            print ("Attempt to turn fan off")
            plugTurnOff("Fan")
         

        print("\n")
        #if (temperatureLowTrigger and not isPlugOn("Heater")):
            #print("Attempt to turn heater on")
            #plugTurnOn("Heater")
        #elif (temperatureLowTrigger and isPlugOn("Heater")):
            #print ("Attempt to turn heater off)
            #plugTurnOff("Heater")