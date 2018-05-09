#!/usr/bin/env/ python

import time
import os
import commands
from time import gmtime, strftime, localtime
import pdb
import threading

WAIT_TIME_SEC=20

rpis = [{"name":"nozzle1","ip":"192.168.100.192","cameras":[{"name":["webcam","fiberscope"]},{"port":["8080","8081"]}]},
{"name":"nozzle2","ip":"192.168.100.193","cameras":{"name":["webcam","fiberscope"],"port":["8080","8081"]}},
{"name":"nozzle3","ip":"192.168.100.194","cameras":[{"name":["webcam","fiberscope"]},{"port":["8080","8081"]}]},
{"name":"perspective","ip":"192.168.100.195","cameras":[{"name":["webcam"]},{"port":["8080"]}]},
{"name":"topview","ip":"192.168.100.196","cameras":[{"name":["webcam"]},{"port":["8080"]}]}
]

def make_filename(device_name,camera_name):
    save_folder = "/mnt/nas/"
    filename =  (device_name+ '_'+camera_name+'_'+ strftime("%Y-%m-%d %H:%M:%S", localtime()) + ".mpeg").replace(" ","_").replace(":","-")
    return save_folder + filename

def record_thread(device_name,camera_name,ip,port):
    while True:
        filename = make_filename(device_name,camera_name)
        record_cmd = 'ffmpeg -f mjpeg -re -i "http://'+ip+':'+port+'/?action=stream" -q:v 10 '+ filename +' >/dev/null 2>&1 &'
        print(record_cmd)
        os.system(record_cmd)
        print("start recording:",device_name,camera_name,ip,port)

        time.sleep(WAIT_TIME_SEC)

        print("end recording")

for rpi in rpis:
  device_name = rpi['name']
  ip = rpi['ip']
  cameras = rpi['cameras']
  camera_names = cameras['name']
  camera_ports = cameras['port']
  for idx,camera_name in enumerate(camera_names):
    port = camera_ports[idx]
    thread = threading.Thread(target=record_thread(device_name,camera_name,ip,port)
    thread.start()

