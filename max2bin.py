#!/usr/bin/python
import drivers.RF603.driver as RF603
import sys
try:
    import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
  import fake_rpi
  sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
  sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
  sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

import RPi.GPIO as GPIO

### CONF
pins_in = {'start':1}
pins_out = {i:2**i for i in range(0,10)}

### SETUP
GPIO.setmode(GPIO.BCM)

for func, pins in [(GPIO.IN, pins_in), (GPIO.OUT, pins_out)]:
  for name, p  in pins.items():
    GPIO.setup(func, p)

while True:
  s = RF603.Serial()
  if s.mRange == 500:  
    break
  

### RUN
start = lambda: True if GPIO.input(pins_in['start']) else False

while True:
  meas = []
  i=5
  while i>0: #start():
    result = s.measure()
    meas.append(result)
    i=i-1
  minim = min(meas)