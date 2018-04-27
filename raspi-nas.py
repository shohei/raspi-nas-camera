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
print(video_array)
print(len(video_array))
if len(video_array)==6:
    if "046d" in video_array[0]: #logicool webcam
        webcam_device = video_array[1].strip() #/dev/video0 or /dev/video1
        print("webcam detected")
        fiberscope_device = video_array[4].strip() #/dev/video0 or /dev/video1
        print("fiberscope detected")
    else:
        webcam_device = video_array[4].strip() #/dev/video0 or /dev/video1
        print("webcam detected")
        fiberscope_device = video_array[1].strip() #/dev/video0 or /dev/video1
        print("fiberscope detected")
elif len(video_array)==3:
    if "046d" in video_array[0]: #logicool webcam
        webcam_device = video_array[1].strip() #/dev/video0 
        print("webcam detected")
    else:
        fiberscope_device = video_array[1].strip() #/dev/video0 
        print("fiberscope detected")
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
    
