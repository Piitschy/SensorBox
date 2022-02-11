#!/usr/bin/python
import drivers.RF603.driver as RF603
import sys, os
from datetime import datetime
from time import sleep
import keyboard

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
  import fake_rpi
  sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
  sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
  sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)
  import RPi.GPIO as GPIO

clc = lambda: os.system('cls||clear')

### CONF
pins_in = {
    'start':2,   #pin 3
    'standby':3, #pin 5
    'request':4  #pin 7
  }
pins_out = {
  1   : 17, #pin 11
  2   : 27, #pin 13
  4   : 23, #pin 16 ex: 22/15
  8   : 10, #pin 19
  16  :  9, #pin 21
  32  : 11, #pin 23
  64  :  0, #pin 27
  128 :  5, #pin 29
  256 :  6, #pin 31
  512 : 13  #pin 33
}

### SETUP
GPIO.setmode(GPIO.BCM)

for func, pins in [(GPIO.IN, pins_in), (GPIO.OUT, pins_out)]:
  for name, p  in pins.items():
    GPIO.setup(p, func)

while True:
  s = RF603.Serial()
  if s.mRange == 500:  
    break
  

read_pin = lambda p: True if GPIO.input(pins_in[p]) == 0 else False

def set_pin(p:int, value=True, toggle:bool=False):
  if toggle:
    value = not read_pin(p)
  GPIO.output(p, value)

def nullGPIOs():
  for p in pins_out.values():
    GPIO.output(p, 0)

def encode(val:float, bins:int=10 , min:float=0, max:float=500) -> str:
  d_max = 2**bins
  d = int(round(((d_max-1)/(max-min))*(val-min)))
  if d>d_max or d<0:
    return '0'
  bits:str ='{0:b}'.format(d)
  return bits

def send(bits:str):
  nullGPIOs()
  b_list = reversed([int(b) for b in bits])
  for p,b in zip(pins_out.values(), b_list):
    set_pin(p, b)

def minimum(m:list):
  if all(v==0 for v in m):
    return 0
  if 0 not in m:
    return min(m)
  m_fil = [v for v in m if v>0]
  return min(m_fil)

read = lambda command, key: read_pin(command) or keyboard.read_key() == key

### RUN
meas = []
clc()
s.turn('off')
while True:
  if read('start', 's'):
    s.turn('on')
    break

while True:
  if read('start', 's'): #read_pin('start'):
    print('Messung')
    result = s.measure()
    meas.append(result)
  elif len(meas)>0:
    if read('start', 's'):#read_pin('start'):
      s.turn('on')
      continue
    elif read('request', 'r'): #read_pin('request'):
      s.turn('off')
      minim = minimum(meas)
      bins = encode(minim)
      clc()
      print(bins, minim)
      send(bins)
      with open("messungen.txt",'a') as f:
        f.write(' '.join([str(datetime.now()),str(meas)])+'\n')
      meas = []
      while True:
        if read('start', 's'):
          nullGPIOs()
          clc()
          s.turn('on')
          break
  continue