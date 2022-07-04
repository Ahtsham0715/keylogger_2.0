
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

def write_data(data):
    db.collection('users').document('mHi4Kcg4DP3iLHKrU3kO').set({
        'name': data,
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