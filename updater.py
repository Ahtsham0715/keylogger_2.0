import os
import subprocess
from threading import Thread
import time
import requests
from tqdm import tqdm
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

cred = credentials.Certificate("core-builder-addon-e760e0910006.json")
firebase_admin.initialize_app(cred,{
    'storageBucket': 'core-builder-addon.appspot.com'
})
db = firestore.client()



# if(os.path.exists("core_builder_file.exe")): #TODO
#     os.remove("core_builder_file.exe")
    


def update_func(url):
    print('update function started... ')    
    def downloadThread():
        Thread(target=download).start()



    def download():
        
        filename = "corelog.exe" #TODO            
        r = requests.get(url, stream=True)
        f = open(filename, "wb")
        fileSize = int(r.headers["Content-Length"])
        chunk = 1
        downloaded = 0 # keep track of size downloaded so far
        chunkSize = 1024
        bars = int(fileSize/chunkSize)
        print(dict(num_bars=bars))
        with open(filename, "wb") as fp:
            for chunk in tqdm(r.iter_content(chunk_size=chunkSize), total=bars, unit="KB",
                            desc=filename, leave=True):
                fp.write(chunk)
                downloaded += chunkSize # increment the downloaded
        
    downloadThread()
    print('update function ended... ')    

def run_file():
    subprocess.run(["corelog.exe"]) #TODO
            
    

def update_checker():
    doc_ref = db.collection(u'version').document(u'version_doc')
    doc = doc_ref.get()
    if doc.exists:
        doc = doc.to_dict()
        app_version = doc['appversion']
        download_link = doc['update_link']
        print(f'app version is: {app_version}')
        print(f'update file link is: {download_link}')
        with open('version.txt', 'r+') as versionfile: #TODO
            localversion = versionfile.read()
            if(str(app_version) > str(localversion)):
                print('update found')
                if (download_link != ''):
                    print('update link available')
                    update_func(download_link)
                    run_file()
    else:
        print(u'No such document!')

update_checker()