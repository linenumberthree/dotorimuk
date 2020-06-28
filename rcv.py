#!/usr/bin/env python

from picamera import *
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from multiprocessing import Process, Queue
import time
import datetime
import socket
import smtplib
import subprocess
import os.path
import RPi.GPIO as GPIO
import threading
import serial
import shlex

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

ser=serial.Serial('/dev/ttyACM0', 9600)

camera = PiCamera()
camera.resolution=(640, 480)


me='dotorimuk4@naver.com'
you='dotorimuk4@naver.com'
user='dotorimuk4'
passwd='rlatlsdlwkd123'
smtp_server='smtp.naver.com'
smtp_port=465


def time_thread_run():
    while True:
        GPIO.output(17, False)
        print("On")
        time.sleep(1)
        GPIO.output(17, True)
        print("Off")
        time.sleep(30)


def rp_camera():
    while True:
        msg=ser.readline().decode()
        print("received msg : {}".format(msg))
        if 'Soil' in msg:
            watermsg=ser.readline().decode()
            print("Soil humidity : {}".format(watermsg))
        elif 'Warning' in msg:
            if 'S' in msg:
                print("54321")
                errormsg='Please check that the sprinkler is broken.'
                message=MIMEText(errormsg)
                message['Subject']='Water Please! Sprinkler error'
                message['from']=me
                message['to']=you
            elif 'T' in msg:
                print("12345")
                temp=ser.readline().decode()
                errormsg=temp
                message=MIMEText(errormsg)
                message['Subject']='Hot or Cold! Temperature error'
                message['from']=me
                message['to']=you
            s=smtplib.SMTP_SSL(smtp_server, smtp_port)
            s.login(user, passwd)
            s.send_message(message)
            s.quit()
        elif 'Temp' in msg:
            tempmsg=ser.readline().decode()
            print("Temperature : {}".format(tempmsg))
        """
        elif 'Motion' in msg:
            now=datetime.datetime.now()
            filename=now.strftime('%Y-%m-%d-%H:%M:%S')
            dirname='/home/pi/Test/'
            recordname=dirname+filename
            h264name='record'
            mp4name=recordname+'.mp4'
            print(recordname + "    " + h264name + "    " + mp4name)
            command=shlex.split("MP4Box -add {}.h264 {}.mp4".format(h264name, filename))
            print(command)
            message=MIMEMultipart()
            message['Subject']='Motion Detected!'
            message['from']=me
            message['to']=you
            camera.start_recording(h264name+'.h264')
            camera.wait_recording(3)
            camera.stop_recording()
            subprocess.call(command)
            time.sleep(5)
            img_file=open(filename+'.mp4', 'rb').read()
            data=MIMEBase("application", "octet-stream")
            data.set_payload(img_file)
            encoders.encode_base64(data)
            data.add_header('Content-Disposition', 'attachment', filename=mp4name)
            message.attach(data)
            s=smtplib.SMTP_SSL(smtp_server, smtp_port)
            s.login(user, passwd)
            s.sendmail(me, you, message.as_string())
            s.quit()
            message['Contents']=None
            subprocess.Popen("rm "+h264name+".h264", shell=True)
"""

if __name__ == '__main__':
    GPIO.output(17, False)
    time.sleep(1)
    GPIO.output(17, True)
    p1 = threading.Thread(target = time_thread_run)
    p2 = threading.Thread(target = rp_camera)
    p1.start()
    p2.start()