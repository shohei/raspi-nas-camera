from subprocess import Popen,PIPE

id_nozzle1_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-4.1.4):'
id_topview = 'USB 2.0 Camera: HD USB Camera (usb-0000:00:14.0-4.2.4):'
id_nozzle1_fiberscope = 'USB2.0 PC CAMERA: USB2.0 PC CAM (usb-0000:00:14.0-4.3.4.4):'
id_perspective_webcam = 'UVC Camera (046d:0825) (usb-0000:00:14.0-4.4.4):'

def find_cam(cam):
    cmd = ["sudo","/usr/bin/v4l2-ctl", "--list-devices"]
    out, err = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    out, err = out.strip(), err.strip()
    for l in [i.split("\n\t") for i in out.split("\n\n")]:
        if cam in l[0]:
            return l[1]
    return False

device_nozzle1_webcam = find_cam(id_nozzle1_webcam)
device_topview = find_cam(id_topview)
device_nozzle1_fiberscope = find_cam(id_nozzle1_fiberscope)
device_perspective_webcam = find_cam(id_perspective_webcam)


print(device_nozzle1_webcam,device_topview,device_nozzle1_fiberscope,device_perspective_webcam)

 

