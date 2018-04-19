#!/usr/bin/env/ python

import time
import os
import commands
from time import gmtime, strftime, localtime
import pdb
import threading

_, HOSTNAME = commands.getstatusoutput("cat /etc/hostname")
_, output = commands.getstatusoutput("ls /dev/video*")
if output[0:2]=="ls":
    print("No cameras are connected. Abort program.")
    exit()

status,output=  commands.getstatusoutput("v4l2-ctl --list-devices")
video_array = output.split('\n')
webcam_device = ""
fiberscope_device = ""
if len(video_array)==6:
    if "046d" in video_array[0]: #logicool webcam
        webcam_device = video_array[1].strip() #/dev/video0 or /dev/video1
        fiberscope_device = video_array[4].strip() #/dev/video0 or /dev/video1
elif len(video_array)==3:
    if "046d" in video_array[0]: #logicool webcam
        webcam_device = video_array[1].strip() #/dev/video0 
    else:
        fiberscope_device = video_array[1].strip() #/dev/video0 
else:
    print("Invalid numbers of camera. Abort program.")
    exit()

#WAIT_TIME_SEC = 1*60*60 #1 hour
WAIT_TIME_SEC = 10*60 #10 min.
#WAIT_TIME_SEC = 10 #10sec (for debug)

# start streaming 
stream_cmd_webcam = '/usr/local/bin/mjpg_streamer -i "input_uvc.so -r 1280x720 -d '+ webcam_device +' -f 30 -q 80" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www" &'
stream_cmd_fiberscope = '/usr/local/bin/mjpg_streamer -i "input_uvc.so -r 1280x720 -d '+ fiberscope_device +' -f 30 -q 80" -o "output_http.so -p 8081 -w /usr/local/share/mjpg-streamer/www" &'

if webcam_device: 
    os.system(stream_cmd_webcam)
if fiberscope_device:
    os.system(stream_cmd_fiberscope)
    
for i in range(2):
    print(2-i)
    time.sleep(1)

def make_webcam_filename():
    save_folder = "/mnt/nas/"
    webcam_filename =  (HOSTNAME + '_webcam_'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + ".mpeg").replace(" ","_").replace(":","-")
    return save_folder + webcam_filename

def make_fiberscope_filename():
    save_folder = "/mnt/nas/"
    fiberscope_filename = (HOSTNAME + '_fiberscope_'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + ".mpeg").replace(" ","_").replace(":","-")
    return save_folder + fiberscope_filename

def webcam_func():
    while True:
        webcam_filename = make_webcam_filename()
        record_cmd_webcam = 'ffmpeg -f mjpeg -re -i "http://localhost:8080/?action=stream" -q:v 10 '+ webcam_filename +' >/dev/null 2>&1 &'
        print(record_cmd_webcam)
	os.system(record_cmd_webcam)
	_, output = commands.getstatusoutput("ps aux | grep -E 'ffmpeg.*8080' | awk '{print $2}'")
	pid1 = output.split('\n')[0]
        print("start webcam recording")

        time.sleep(WAIT_TIME_SEC) 

        print("end webcam recording")
        kill_cmd1 = "kill -9 " + str(pid1)
        os.system(kill_cmd1)

def fiberscope_func():
    while True:
        fiberscope_filename = make_fiberscope_filename()
        record_cmd_fiberscope = 'ffmpeg -f mjpeg -re -i "http://localhost:8081/?action=stream" -q:v 10 '+ fiberscope_filename +' >/dev/null 2>&1 &'
        print(record_cmd_fiberscope)
    	os.system(record_cmd_fiberscope)
	_, output = commands.getstatusoutput("ps aux | grep -E 'ffmpeg.*8081' | awk '{print $2}'")
	pid2 = output.split('\n')[0]
        print("start fiberscope recording")

        time.sleep(WAIT_TIME_SEC) 

        print("end fiberscope recording")
        kill_cmd2 = "kill -9 " + str(pid2)
        os.system(kill_cmd2)

if webcam_device:
    thread_1 = threading.Thread(target=webcam_func)
    thread_1.start()
if fiberscope_device:
    thread_2 = threading.Thread(target=fiberscope_func)
    thread_2.start()

