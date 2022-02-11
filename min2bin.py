#!/usr/bin/python

def main():
  import drivers.RF603.driver as RF603
  import sys, os
  from datetime import datetime
  from time import sleep, time
  import keyboard
  from lib.utils import DB

  try:
      import RPi.GPIO as GPIO
      key_input = False
  except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
    sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)
    key_input = True
    import RPi.GPIO as GPIO

  clc = lambda: os.system('cls||clear')

  ### CONF
  pins_in = {
      's':2,   #pin 3 start
      'o':3, #pin 5 standby
      'r':4  #pin 7 request
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

  db = DB('./var/db_measurements')

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

  def read(command):
    if key_input:
      return keyboard.read_key() == command
    else:
      return read_pin(command)

  def write2db(meas:list):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    def time_str(time:float, format:str = DATE_FORMAT, ms:bool = False) -> str:
      t = time if ms else int(time)
      return datetime.fromtimestamp(t).strftime(format)
    
    start = time()
    
    dataset = {
      'name': 'Messung',
      'sensor': 'RF603',
      'rate': 0,
      'start_date': time_str(start, DATE_FORMAT),
      'start_time': time_str(start, TIME_FORMAT),
      'start': start,
      'duration': 0,
      'data': meas
    }
    
    db.write(str(start),dataset)

  ### RUN
  meas = []
  clc()
  s.turn('off')
  while True:
    if read('s'):
      s.turn('on')
      break

  while True:
    if read('s'): #read_pin('start'):
      print('Messung')
      try:
        result = s.measure()
      except:
        result = 0
      meas.append(result)
    elif len(meas)>0:
      if read('s'):#read_pin('start'):
        s.turn('on')
        continue
      elif read('r'): #read_pin('request'):
        s.turn('off')
        minim = minimum(meas)
        bins = encode(minim)
        clc()
        print(bins, minim)
        send(bins)
        write2db(meas)
        with open("messungen_"+str(datetime.now())+".csv",'w') as f:
          f.write('\n'.join([str(e) for e in meas]))
        meas = []
        while True:
          if read('s'):
            nullGPIOs()
            clc()
            s.turn('on')
            break
    continue

if __name__ == "__main__":
  main()