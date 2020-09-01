import pyrebase
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

config = {
    "apiKey": "AIzaSyCGvYVyE9M9FrWGZQ9-9cdCYnE7e6WTb98",
  "authDomain": "webel-dashboad.firebaseapp.com",
  "databaseURL": "https://webel-dashboad.firebaseio.com",
  "projectId": "webel-dashboad",
  "storageBucket": "webel-dashboad.appspot.com",
  "messagingSenderId": "57021749904",
  "appId": "1:57021749904:web:5812ff5b3ee5817e045615",
  "measurementId": "G-9Q2P9QYDH1"
}

cred = credentials.Certificate("webel-dashboad-firebase-adminsdk-39ope-cec400e142.json")
# firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

firebase_admin.initialize_app(cred, {
    'storageBucket': 'webel-dashboad.appspot.com'
})

# bucket = storage.bucket()
# storage.child("/home/omni/liveapp-24-02/LineCrossing/2020-03-12/cam2/Warning_alert_10-41-33.jpg").put("/home/omni/liveapp-24-02/LineCrossing/2020-03-12/cam2/Warning_alert_10-41-33.jpg")
# imageBlob = bucket.blob("/")
