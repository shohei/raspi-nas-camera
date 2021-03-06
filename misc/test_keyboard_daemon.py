from evdev import InputDevice, categorize, ecodes
#dev = InputDevice('/dev/input/event12') #Keyboard (for debug)
#dev = InputDevice('/dev/input/event6') #Arduino leonardo
dev = InputDevice('/dev/input/event11') #Arduino leonardo

last = 0
current = 0

for event in dev.read_loop():
  if event.type == ecodes.EV_KEY:
    print(current)
    current = event.code
    if((last==0 or last==48) and current==30): # a is pushed
      print('on')
    elif((last==0 or last==30) and current==48): # b is pushed
      print('off')
    last = current
  
