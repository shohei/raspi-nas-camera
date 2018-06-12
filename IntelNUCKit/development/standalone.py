import commands
import os
from evdev import InputDevice, categorize, ecodes
import sys
import termios
import contextlib
import time
import os
import commands
from time import gmtime, strftime, localtime
import pdb
import threading

from subprocess import Popen,PIPE

#id_nozzle1_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-4.1.4):'
#id_topview = 'USB 2.0 Camera: HD USB Camera (usb-0000:00:14.0-4.2.4):'
#id_nozzle1_fiberscope = 'USB2.0 PC CAMERA: USB2.0 PC CAM (usb-0000:00:14.0-4.3.4.4):'
#id_perspective_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-4.4.4):'
id_nozzle1_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-1.4):'
id_topview = 'USB 2.0 Camera: HD USB Camera (usb-0000:00:14.0-4.2.4):'
id_nozzle1_fiberscope = 'USB2.0 PC CAMERA: USB2.0 PC CAM (usb-0000:00:14.0-4    .3.4.4):'
id_perspective_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-2.4):'


def find_cam(cam):
    cmd = ["sudo","/usr/bin/v4l2-ctl", "--list-devices"]
    out, err = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    out, err = out.strip(), err.strip()
    print(out)
    for l in [i.split("\n\t") for i in out.split("\n\n")]:
        if cam in l[0]:
            return l[1]
    return False

def make_filename(device_name,camera_name):
    save_folder = "/mnt/nas/" + device_name + '/'
    filename =  (device_name+ '_'+camera_name+'_'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + ".mpeg").replace(" ","_").replace(":","-")
    return save_folder + filename

def kill_ffmpeg():
    _, output = commands.getstatusoutput("ps aux | grep -E 'ffmpeg' | awk '{print $2}'")
    pids = output.split('\n')
    for pid in pids: 
        cmd = "sudo kill -9 "+pid
        print(cmd)
        os.system(cmd)

device_nozzle1_webcam = find_cam(id_nozzle1_webcam)
device_topview = find_cam(id_topview)
device_nozzle1_fiberscope = find_cam(id_nozzle1_fiberscope)
device_perspective_webcam = find_cam(id_perspective_webcam)
print(device_nozzle1_webcam,device_topview,device_nozzle1_fiberscope,device_perspective_webcam)

filename = make_filename("nozzle1","webcam")
cmd = "sudo ffmpeg -i "+device_nozzle1_webcam+" -q:v 3 "+filename+" >/dev/null 2>&1 &"
print(cmd)
os.system(cmd)

filename = make_filename("nozzle1","fiberscope")
cmd = "sudo ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -i "+device_nozzle1_fiberscope+" -q:v 3 "+filename+" >/dev/null 2>&1 &"
print(cmd)
os.system(cmd)

filename = make_filename("topview","webcam")
cmd = "sudo ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -input_format mjpeg -i "+device_topview+" -q:v 3 "+filename+" >/dev/null 2>&1 &"
print(cmd)
os.system(cmd)

filename = make_filename("perspective","webcam")
cmd = "sudo ffmpeg -i "+device_perspective_webcam+" -q:v 3 "+filename+" >/dev/null 2>&1 &"
print(cmd)
os.system(cmd)


#try:
#    while True:
#        pass
#except KeyboardInterrupt:
#    kill_ffmpeg()



