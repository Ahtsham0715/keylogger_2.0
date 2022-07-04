
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



cred = credentials.Certificate("core-builder-addon-e760e0910006.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def write_data(data):
    db.collection('users').document().set({
        'myname': data
    })


if __name__=="__main__":
	write_data(data='shami')