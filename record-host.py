#!/usr/bin/env/ python

import time
import os
import commands
from time import gmtime, strftime, localtime
import pdb
import threading

WAIT_TIME_SEC=20


def make_webcam_filename():
    save_folder = "/mnt/nas/"
    webcam_filename =  ("nozzle1"+ '_webcam_'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + ".mpeg").replace(" ","_").replace(":","-")
    return save_folder + webcam_filename

def make_webcam_filename2():
    save_folder = "/mnt/nas/"
    webcam_filename =  ("perspective" + '_webcam_'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + ".mpeg").replace(" ","_").replace(":","-")
    return save_folder + webcam_filename

def make_fiberscope_filename():
    save_folder = "/mnt/nas/"
    fiberscope_filename = ("nozzle1"+ '_fiberscope_'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + ".mpeg").replace(" ","_").replace(":","-")
    return save_folder + fiberscope_filename


def webcam_func():
    while True:
        webcam_filename = make_webcam_filename()
        record_cmd_webcam = 'ffmpeg -f mjpeg -re -i "http://192.168.100.8:8080/?action=stream" -q:v 10 '+ webcam_filename +' >/dev/null 2>&1 &'
        print(record_cmd_webcam)
        os.system(record_cmd_webcam)
        print("start webcam recording")

        time.sleep(WAIT_TIME_SEC)

        print("end webcam recording")

def webcam2_func():
    while True:
        webcam_filename = make_webcam_filename2()
        record_cmd_webcam = 'ffmpeg -f mjpeg -re -i "http://192.168.100.212:8080/?action=stream" -q:v 10 '+ webcam_filename +' >/dev/null 2>&1 &'
        print(record_cmd_webcam)
        os.system(record_cmd_webcam)
        print("start webcam recording")

        time.sleep(WAIT_TIME_SEC)

        print("end webcam recording")

def fiberscope_func():
    while True:
        fiberscope_filename = make_fiberscope_filename()
        record_cmd_fiberscope = 'ffmpeg -f mjpeg -re -i "http://192.168.100.8:8081/?action=stream" -q:v 10 '+ fiberscope_filename +' >/dev/null 2>&1 &'
        print(record_cmd_fiberscope)
        os.system(record_cmd_fiberscope)
        print("start fiberscope recording")

        time.sleep(WAIT_TIME_SEC)

        print("end fiberscope recording")

thread_1 = threading.Thread(target=webcam_func)
thread_1.start()
thread_2 = threading.Thread(target=fiberscope_func)
thread_2.start()
thread_3 = threading.Thread(target=webcam2_func)
thread_3.start()

