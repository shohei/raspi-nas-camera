#!/usr/bin/env/ python
#-*- coding:utf-8 -*-
import sys
import termios
import contextlib

import time
import os
import commands
from time import gmtime, strftime, localtime
import pdb
import threading

WAIT_TIME_SEC=20


class MyClass():
  def __init__(self):
    self.threads = []

class Job():
  def __init__(self,device_name,camera_name,ip,port):
    self.stop_event = threading.Event() #停止させるかのフラグ
    self.thread = threading.Thread(target=self.record_thread,args=(device_name,camera_name,ip,port))
    self.thread.start()
  def stop(self):
    """スレッドを停止させる"""
    self.stop_event.set()
    self.thread.join()    #スレッドが停止するのを待つ

  def record_thread(self,device_name,camera_name,ip,port):
    while not self.stop_event.is_set():
      filename = make_filename(device_name,camera_name)
      record_cmd = 'ffmpeg -f mjpeg -re -i "http://'+ip+':'+port+'/?action=stream" -q:v 10 '+ filename +' >/dev/null 2>&1 &'
      print(record_cmd)
      os.system(record_cmd)
      print("start recording:",device_name,camera_name,ip,port)

      time.sleep(WAIT_TIME_SEC)

      print("end recording")

#rpis = [{"name":"nozzle1","ip":"192.168.100.192","cameras":{"name":["webcam","fiberscope"],"port":["8080","8081"]}},
#{"name":"nozzle2","ip":"192.168.100.193","cameras":{"name":["webcam","fiberscope"],"port":["8080","8081"]}},
#{"name":"nozzle3","ip":"192.168.100.194","cameras":{"name":["webcam","fiberscope"],"port":["8080","8081"]}},
#{"name":"perspective","ip":"192.168.100.195","cameras":{"name":["webcam"],"port":["8080"]}},
#{"name":"topview","ip":"192.168.100.196","cameras":{"name":["webcam"],"port":["8080"]}}
#]

rpis = [{"name":"perspective","ip":"192.168.100.195","cameras":{"name":["webcam"],"port":["8080"]}},
{"name":"topview","ip":"192.168.100.196","cameras":{"name":["webcam"],"port":["8080"]}}
]

def make_filename(device_name,camera_name):
    save_folder = "/mnt/nas/"
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
      #thread = threading.Thread(target=record_thread,args=(device_name,camera_name,ip,port))
      job = Job(device_name,camera_name,ip,port)
      mClass.threads.append(job)

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

if __name__ == '__main__':
  mClass = MyClass()
  start_server(mClass)
