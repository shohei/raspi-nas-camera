#!/usr/bin/env/ python
#-*- coding:utf-8 -*-

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

status,output = commands.getstatusoutput("ls -l  /dev/input/by-id/ | sed '1d'")
dev_number = 0
for o in output.split("\n"):
    if "Leonardo" in o:
        o = o.split("event")
        dev_number = o[-1]
dev = InputDevice('/dev/input/event'+dev_number) #Arduino leonardo
#dev = InputDevice('/dev/input/event12') #Keyboard (for debug)

#rpis = [{"name":"nozzle1","ip":"192.168.100.192","cameras":{"name":["webcam","fiberscope"],"port":["8080","8081"]}},
#{"name":"nozzle2","ip":"192.168.100.193","cameras":{"name":["webcam","fiberscope"],"port":["8080","8081"]}},
#{"name":"nozzle3","ip":"192.168.100.194","cameras":{"name":["webcam","fiberscope"],"port":["8080","8081"]}},
#{"name":"perspective","ip":"192.168.100.195","cameras":{"name":["webcam"],"port":["8080"]}},
#{"name":"topview","ip":"192.168.100.196","cameras":{"name":["webcam"],"port":["8080"]}}
#]

#id_nozzle1_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-4.1.4):'
#id_topview = 'USB 2.0 Camera: HD USB Camera (usb-0000:00:14.0-4.2.4):'
#id_nozzle1_fiberscope = 'USB2.0 PC CAMERA: USB2.0 PC CAM (usb-0000:00:14.0-4.3.4.4):'
#id_perspective_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-4.4.4):'
#id_nozzle1_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-1.4):'
#id_topview = 'USB 2.0 Camera: HD USB Camera (usb-0000:00:14.0-4.2.4):'
#id_nozzle1_fiberscope = 'USB2.0 PC CAMERA: USB2.0 PC CAM (usb-0000:00:14.0-4.3.4.4):'
#id_perspective_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-2.4):'
id_nozzle1_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-4.3.2.2):'
id_nozzle1_fiberscope = 'USB2.0 PC CAMERA: USB2.0 PC CAM (usb-0000:00:14.0-1.2.2.4):'
id_nozzle2_fiberscope = 'USB2.0 PC CAMERA: USB2.0 PC CAM (usb-0000:00:14.0-2.2.2.4):'
id_topview = 'USB 2.0 Camera: HD USB Camera (usb-0000:00:14.0-4.2.4):'
id_perspective_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-4.1.4):'

def find_cam(cam):
    cmd = ["sudo","/usr/bin/v4l2-ctl", "--list-devices"]
    out, err = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    out, err = out.strip(), err.strip()
    for l in [i.split("\n\t") for i in out.split("\n\n")]:
        if cam in l[0]:
            return l[1]
    return False

device_topview = find_cam(id_topview)
device_perspective_webcam = find_cam(id_perspective_webcam)
device_nozzle1_webcam = find_cam(id_nozzle1_webcam)
device_nozzle1_fiberscope = find_cam(id_nozzle1_fiberscope)
device_nozzle2_fiberscope = find_cam(id_nozzle2_fiberscope)

print(device_topview,
      device_nozzle1_webcam,
      device_nozzle1_fiberscope,
      device_nozzle2_fiberscope,
      device_perspective_webcam)

# rpis = [{"name":"nozzle1","ip":"192.168.100.192","cameras":{"name":["webcam","fiberscope"],"port":["8080","8081"]}},
# {"name":"perspective","ip":"192.168.100.195","cameras":{"name":["webcam"],"port":["8080"]}},
# {"name":"topview","ip":"192.168.100.196","cameras":{"name":["webcam"],"port":["8081"]}}
# ]

class MyClass():
  def __init__(self):
    self.threads = []

class Job():

  def __init__(self,device_name,camera_name,ip,port):
    self.stop_event = threading.Event() 
    self.thread = threading.Thread(target=self.record_thread,args=(device_name,camera_name,ip,port))
    self.thread.start()

  def stop(self):
    """スレッドを停止させる"""
    self.stop_event.set()
    self.thread.join() 

  def record_thread(self,device_name,camera_name,ip,port):
    filename = make_filename(device_name,camera_name)
    record_cmd = 'ffmpeg -f mjpeg -re -i "http://'+ip+':'+port+'/?action=stream" -q:v 10 '+ filename +' >/dev/null 2>&1 &'
    print(record_cmd)
    os.system(record_cmd)

    while not self.stop_event.is_set():
      pass # wait forever
  
def make_filename(device_name,camera_name):
    save_folder = "/mnt/nas/" + device_name + '/'
    filename =  (device_name+ '_'+camera_name+'_'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + ".mpeg").replace(" ","_").replace(":","-")
    return save_folder + filename

def start_record(mClass):
  for rpi in rpis:
    print(rpi)
    device_name = rpi['name']
    ip = rpi['ip']
    cameras = rpi['cameras']
    camera_names = cameras['name']
    camera_ports = cameras['port']
    for idx,camera_name in enumerate(camera_names):
      port = camera_ports[idx]
      job = Job(device_name,camera_name,ip,port)
      mClass.threads.append(job)

def start_record_standalone():
    if device_topview:
        filename = make_filename("topview","webcam")
        cmd = "sudo ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -input_format mjpeg -i "+device_topview+" -q:v 3 "+filename+" >/dev/null 2>&1 &"
        print(cmd)
        os.system(cmd)
        time.sleep(2) 

    if device_nozzle1_webcam:
        filename = make_filename("nozzle1","webcam")
        cmd = "sudo ffmpeg  -i "+device_nozzle1_webcam+" -q:v 3 "+filename+" >/dev/null 2>&1 &"
        print(cmd)
        os.system(cmd)
        time.sleep(2) 

    if device_nozzle1_fiberscope:
        filename = make_filename("nozzle1","fiberscope")
        cmd = "sudo ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -i "+device_nozzle1_fiberscope+" -q:v 3 "+filename+" >/dev/null 2>&1 &"
        print(cmd)
        os.system(cmd)
        time.sleep(2) 
   
    if device_perspective_webcam:
        filename = make_filename("perspective","webcam")
        cmd = "sudo ffmpeg -i "+device_perspective_webcam+" -q:v 3 "+filename+" >/dev/null 2>&1 &"
        print(cmd)
        os.system(cmd)
        time.sleep(2) 

    if device_nozzle2_fiberscope:
        filename = make_filename("nozzle2","fiberscope")
        cmd = "sudo ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -i "+device_nozzle2_fiberscope+" -q:v 3 "+filename+" >/dev/null 2>&1 &"
        print(cmd)
        os.system(cmd)
        time.sleep(2) 

def kill_threads(mClass):
  jobs = mClass.threads
  for job in jobs:
    job.stop()
  mClass.threads = []
  kill_ffmpeg()

def kill_ffmpeg():
  _, output = commands.getstatusoutput("ps aux | grep -E 'ffmpeg' | awk '{print $2}'")
  pids = output.split('\n')
  for pid in pids: 
    cmd = "sudo kill -9 "+pid
    print(cmd)
    os.system(cmd)

@contextlib.contextmanager
def raw_mode(file):
  old_attrs = termios.tcgetattr(file.fileno())
  new_attrs = old_attrs[:]
  new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
  try:
    termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
    yield
  finally:
    termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

def start_server(mClass):
  print('exit with ^C or ^D')
  with raw_mode(sys.stdin):
    try:
      while True:
        ch = sys.stdin.read(1)
        if(ch=='a'):
          start_record(mClass)
        elif(ch=='b'):
          print("kill threads")
          kill_threads(mClass)

    except (KeyboardInterrupt, EOFError):
      pass

def start_daemon(mClass):
  mClass.last = 0
  mClass.current = 0
  for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
      mClass.current = event.code
      if((mClass.last==0 or mClass.last==48) and mClass.current==30): # a is pushed
        print('on')
        start_record_standalone()
      elif((mClass.last==0 or mClass.last==30) and mClass.current==48): # b is pushed
        print('off')
        kill_ffmpeg()
      mClass.last = mClass.current

if __name__ == '__main__':
  mClass = MyClass()
  #start_server(mClass) # non-daemon program 
  start_daemon(mClass)

