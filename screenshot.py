import pyautogui
import os
import time
from datetime import datetime
from threading import Timer, Thread
import dbfile
import getpass

comname = getpass.getuser()

def remaining_images_checker():
    files = os.listdir(comname)
    print(len(files))
    if len(files) != 0:
        for file in files:
            try:
                print(file)
                dbfile.upload_images(imgpath=f'{comname}/{file}')
                os.remove(f'{comname}/{file}')
            except:
                print('exception occured')        
remaining = Thread(daemon=True,target=remaining_images_checker)
remaining.start()
remaining.join()

def ss_taker():
    if not os.path.exists(f'{comname}'):
        os.mkdir(comname)
    print('function called')
    try:
        date = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        pyautogui.screenshot(f'{comname}/{date}.png')
        print(f'ss saved to {comname}/{date}')
        dbfile.upload_images(imgpath=f'{comname}/{date}.png')
        os.remove(f'{comname}/{date}.png')
    except:
        print('some exception occured')
        time.sleep(2)
        ss_taker() 
    timer = Timer(interval=50, function = ss_taker)
    timer.daemon = True
    timer.start()
    timer.join()

    

# if __name__ == "__main__":
#     ss_taker()