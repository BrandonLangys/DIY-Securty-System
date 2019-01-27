import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from time import sleep
from datetime import datetime
import os
import sys
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import smtplib
import glob

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

servo_1 = 16
servo_2 = 18
motion_1 = 11  # left side dc=12.5
motion_2 = 13  # middle dc = 7.5
motion_3 = 15  # right dc= 2.5

GPIO.setup(motion_1, GPIO.IN)  # motion sensor
GPIO.setup(motion_2, GPIO.IN)  # motion sensor
GPIO.setup(motion_3, GPIO.IN)  # motion sensor

camera = PiCamera()


def whereToMove(turnTo):
    GPIO.setup(servo_1, GPIO.OUT)  # servo begins
    defPWM = GPIO.PWM(servo_1, 50)
    defPWM.start(0)
    time.sleep(.01)
    defPWM.ChangeDutyCycle(7.5)
    print('set')
    time.sleep(.2)

    if (turnTo == 0):
        defPWM.ChangeDutyCycle(2.5)
        print('right')
        time.sleep(5)
    if (turnTo == 1):  # middle
        print('middle')
        time.sleep(5)
    if (turnTo == 2):
        defPWM.ChangeDutyCycle(12.5)
        print('left')
        time.sleep(5)


def Camera():
    h264_Vid = '.h264'
    mp4_video = '.mp4'
    vid_Name = datetime.now().strftime('%m-%d-%Y_%H.%M.%S')

    camera.start_preview()

    camera.start_recording('/home/pi/PiFiles/' + vid_Name + h264_Vid)
    sleep(5)
    camera.stop_recording()

    camera.stop_preview()
    os.system('MP4Box -add ' + vid_Name + h264_Vid + ' ' + vid_Name + mp4_video)
    os.system('rm ' + vid_Name + h264_Vid)


def moveBack():
    GPIO.setup(servo_1, GPIO.OUT)  # servo begins
    defPWM = GPIO.PWM(servo_1, 50)
    defPWM.ChangeDutyCycle(7.5)
    time.sleep(1)


def sendEmail():
    server = smtplib.SMTP('smtp.gmail.com', 587)

    i = 0
    mp4files = []
    for file in glob.glob("*.mp4"):
        mp4files.append(file)
    # loginInfo
    user = 'tk.compsci10@gmail.com'
    passWord = 'toEasy11'

    # message
    fromAdd = user
    toAdd = "tk.compsci10@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromAdd
    msg['To'] = toAdd
    msg['Subject'] = "Alarm Triggered"

    body = "test"
    msg.attach(MIMEText(body, 'plain'))

    # fileAttachment

    attachment = open(mp4files[i], "rb")

    part = MIMEBase('application', "octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; fileName= %s" % os.path.basename(mp4files[i]))
    msg.attach(part)
    i += 1

    # sendingEmail
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, passWord)
    text = msg.as_string()
    server.sendmail(fromAdd, toAdd, text)

    server.quit()


while True:

    num = 0
    whereToMove(1)

    if GPIO.input(motion_1):
        motion_1On = 0
        print("motion has been detected")
        whereToMove(motion_1On)
        Camera()
        sendEmail()
        moveBack()
        num += 1
        time.sleep(0.5)

    if GPIO.input(motion_2):
        motion_1On = 1
        print("motion has been detected")
        whereToMove(motion_1On)
        Camera()
        sendEmail()
        num += 1
        time.sleep(0.5)

    if GPIO.input(motion_3):
        motion_1On = 2
        print("motion has been detected")
        whereToMove(motion_1On)
        Camera()
        sendEmail()
        moveBack()
        num += 1
        time.sleep(0.5)