from time import gmtime, strftime, sleep
from datetime import datetime
import RPi.GPIO as GPIO
import os
import subprocess
import os.path
import httplib, urllib
import pysftp
import atexit
import traceback
import logging
import time

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def exit_handler():
    GPIO.output(22, False)
atexit.register(exit_handler)

# Logging
logger = logging.getLogger('doorbell')
hdlr = logging.FileHandler('/home/pi/Desktop/doorbell/web/doorbell.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Start
print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Doorbell started")
logger.info("Doorbell started")

# Volume
cmdVolume='amixer set PCM -- 1000'
subprocess.call(cmdVolume, shell=True)

# Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.output(15, False)
GPIO.output(22, True)
GPIO.setup(11, GPIO.IN)

# Loop
while 1:
    if not (GPIO.input(11)):
        try:
            time.sleep(0.01)
            if not (GPIO.input(11)):
            
                # Setup
                now=strftime("%Y-%m-%d %H:%M:%S", gmtime())
                filename=strftime("%Y-%m-%d_%H.%M.%S", gmtime())  + '.jpg'

                print(now + " Button pressed")
                logger.info("Button pressed")
                GPIO.output( 15, True)
        
                # Audio
                print("--> Audio")
                logger.info("--> Audio")
                subprocess.Popen(['aplay', '/home/pi/Desktop/doorbell/ringtone.wav'])
        
                # Camera
                print("--> Camera")
                logger.info("--> Camera")
                fullfilename = '/home/pi/Desktop/doorbell/web/photos/' +  filename
                cmdCam='raspistill -o ' + fullfilename
                subprocess.call(cmdCam, shell=True)
        
                # Pushover
                print("--> Pushover")
                logger.info("--> Pushover")
                conn = httplib.HTTPSConnection("api.pushover.net:443")
                conn.request("POST", "/1/messages.json",
                             urllib.urlencode({
                                              "token": "myToken",
                                              "user": "myUser",
                                              "title": "Doorbell",
                                              "message": "KNOCK KNOCK",
                                              "url": "http://example.com/photos/" + filename,
                                              "url_title": "Image",
                                              }),
                             { "Content-type": "application/x-www-form-urlencoded" })
                conn.getresponse()

                # Finished
                print("--> Finished")
                logger.info("--> Finished")
                time.sleep(2)
    
        except Exception, e:
            traceback.print_exc()
            logging.exception("!!!")
    else:
        GPIO.output( 15, False)
