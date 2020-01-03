import pyrebase

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

# auth = firebase.auth()
# authenticate a user
# user = auth.sign_in_with_email_and_password("samyibrahim661@gmail.com", "iotTestUser")

auth = firebase.auth()
user = auth.sign_in_with_email_and_password("samyibrahim661@gmail.com", "iotTestUser")

db = firebase.database()
# print(db.child().get().val())

def insertTest(name, age, height, weight):
  data = {"name": name, "age": age, "height": height, "weight": weight}
  db.child("users").child(name).set(data, user['idToken'])
  print("Insert Successfull")


if __name__ == '__main__':
  insertTest("Tri", "21", "170 cm", "80 kg")
