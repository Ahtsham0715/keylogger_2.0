import pyautogui
import os
import time
from datetime import datetime
from threading import Timer
import dbfile
import getpass

comname = getpass.getuser()

count = 0
def ss_taker():
    global count
    if not os.path.exists(f'{comname}'):
        os.mkdir(comname)
    print('function called')
    try:
        # date = datetime.now().strftime("%H:%M:%S")
        pyautogui.screenshot(f'{comname}/log{count}.png')
        print(f'ss saved to {comname}/log{count}')
        count += 1
        dbfile.upload_images(imgpath=f'{comname}/log{count-1}.png')
        os.remove(f'{comname}/log{count-1}.png')
    except:
        print('some exception occured')
        time.sleep(2)
        ss_taker() 
    timer = Timer(interval=5, function = ss_taker)
    timer.daemon = True
    timer.start()
    timer.join()

    

if __name__ == "__main__":
    ss_taker()