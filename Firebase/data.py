import pyrebase
import logging
import logging.handlers
import datetime
import os
import pathlib

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

timestampStr = datetime.datetime.now().strftime("%d-%b-%Y(%H:%M:%S)")


def insertSensorData(temperature, isMicrophoneTriggered, isCameraTriggered, timestamp):
    info = {"temperature": temperature, "microphoneTriggered": isMicrophoneTriggered,
            "cameraTriggered": isCameraTriggered, "timestamp":timestamp}
    db.child("SensorData").child(timestampStr).set(info, user['idToken'])
    logging.info("Successfully Inserted Sensor Data into Database")


def insertTest(name, age, height, weight):
    data = {"name": name, "age": age, "height": height, "weight": weight}
    db.child("users").child(name).set(data, user['idToken'])
    print("Insert Successfull")


def initializeLog():
    fileName = "iotSmartBaby_" + timestampStr + ".log"
    pathlib.Path('./logs').mkdir(exist_ok=True)
    filename = "logs\log_{}".format(fileName).replace(':', '.')
    should_roll_over = os.path.isfile(filename)
    handler = logging.handlers.RotatingFileHandler(filename, mode='w', backupCount=5)
    if should_roll_over:  #skip if the log already exists (it shouldn't - error handling)
        handler.doRollover()
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.info("LOG Iot Smart Baby Monitoring System - " + timestampStr)


if __name__ == '__main__':
    initializeLog()
    #insertSensorData("20", "1", "0", timestampStr)
