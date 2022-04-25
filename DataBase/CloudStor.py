import json
import threading
import pyrebase
import os

import dotenv 

dotenv.load_dotenv()



config = {
    'databaseURL': os.getenv("FIREBASE_API_URL"),
    'apiKey': os.getenv("FIREBASE_API_KEY"),
    'authDomain': "itappproject-2208c.firebaseapp.com",
    'projectId': "itappproject-2208c",
    'storageBucket': "itappproject-2208c.appspot.com",
    'messagingSenderId': "913980335360",
    'appId': "1:913980335360:web:b1911f51bff8e7118d3fe5",
    'measurementId': "G-842BBGMSGQ"
}


class CloudStore:

    def __init__(self):

        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()
        self.user = self.auth.sign_in_with_email_and_password(
            os.getenv("FIREBASE_EMAIL"), os.getenv("FIREBASE_PASSWORD"))
        self.token = self. user['idToken']
        self.storage = self.firebase.storage()

    def uploadFile(self, pathtouploadlocation: str, pathtofile: str):
        threading.Thread(target=(lambda p1, p2: self.storage.child(
            pathtouploadlocation).put(p2)), args=(pathtouploadlocation, pathtofile,)).start()

    def getFileUrl(self, pathtouploadlocation: str):
        return self.storage.child(pathtouploadlocation).get_url(self.token)
