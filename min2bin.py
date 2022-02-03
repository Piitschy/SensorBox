#!/usr/bin/python
import drivers.RF603.driver as RF603
import sys, os
try:
    import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
  import fake_rpi
  sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
  sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
  sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

import RPi.GPIO as GPIO

### CONF
pins_in = {
    'start':1,
    'laser':2
  }
pins_out = {
  1   : 23,
  2   : 24,
  4   : 25,
  8   : 26,
  16  : 27,
  32  : 28,
  64  : 29,
  128 : 30,
  256 : 31,
  512 : 32
}

### SETUP
GPIO.setmode(GPIO.BCM)

for func, pins in [(GPIO.IN, pins_in), (GPIO.OUT, pins_out)]:
  for name, p  in pins.items():
    GPIO.setup(func, p)

while True:
  s = RF603.Serial()
  if s.mRange == 500:  
    break
  

def nullGPIOs():
  for p in pins_out.values():
    GPIO.output(p, GPIO.LOW)

def encode(val:float, bins:int=10 , min:float=0, max:float=500) -> str:
  d_max = 2**bins
  d = int(round(((d_max-1)/(max-min))*(val-min)))
  if d>d_max or d<0:
    return '0'
  bits:str ='{0:b}'.format(d)
  return bits

def send(bits:str):
  #nullGPIOs()
  b_list = reversed([b for b in bits])
  for p,b in zip(pins_out.values(), b_list):
    #print(p,b)
    pass

def minimum(m:list):
  if all(v==0 for v in m):
    return 0
  if 0 not in m:
    return min(m)
  m_fil = [v for v in m if v>0]
  return min(m_fil)

### RUN
start = lambda: True if GPIO.input(pins_in['start']) else False
i=200
meas = []
os.system('cls||clear')
while True:
  if i>0:
    result = s.measure()
    meas.append(result)
    i=i-1
  elif len(meas)>0:
    minim = minimum(meas)
    bins = encode(minim)
    print(bins, minim)
    send(bins)
    meas = []
    i=200