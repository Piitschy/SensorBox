import sys, os
import json5
import numpy as np
import socket
import struct
from typing import Tuple, List
#import usb.core
import serial

### CONSTANTS ###
UTILS_PATH = 'utils.json5'
SERIAL_PATH = '/dev/ttyUSB0'

### LOAD UTILS ###
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, UTILS_PATH)
with open(filename) as f:
  content = f.read()
  utils = json5.loads(content)

### BASE FUNKTIONS ###

class Sensor(object):
  serial_no = 0

  def set_ident(self,device_type:int=0,firmware:int=0,serial_no:int=0,base:int=0,mRange:int=0):
    self.serial_no = serial_no

  def _alert(self,text):
    print(text)

  def _struc_unpack(self,bytestr:bytes,pos:int=0,bits:int=16):
    if bits == 16:
      return struct.unpack(utils['ENDIAN'], bytestr[pos:pos+2])[0]
    elif bits == 8:
      return int(bin(bytestr[pos]),2)
    else:
      print('Wrong bits')
      return 0

  def _get_distance(self,d,s:int=50):
      return (d*s)/utils['NORM']

### CONECTIONS ###

class Serial(Sensor):
  def __init__(self,port=SERIAL_PATH,addr:int=0x01,timeout:int=1):
    self.ser = serial.Serial(port,timeout=timeout,parity=serial.PARITY_NONE)
    self.addr = addr
    if not self.ser.is_open:
      self._alert('Device not found')
      return 
    #self.identify()
  
  def _write(self,data:bytes) -> bytes:
    self.ser.write(data)
    return self.ser.read(64)

  def write_cmd(self,*args) -> bytes:
    cmd = self._cmd(*args)
    print(cmd)
    return self._write(cmd)

  def identify(self) -> dict:
    result = self.request('ident')
    self.set_ident(
      device_type=result['type'],
      firmware=result['firmware'],
      serial_no=result['serial'],
      base=result['base'],
      mRange=result['mRange']
    )
    return result
  
  def measure(self) -> float:
    result = self.request('measure')
    return self._get_distance(result['value'],self.mRange)

  def request(self,req:str,aws:str=None)->dict:
    aws = aws or req
    c:int = utils['SERIAL']['REQ'][req]
    a:dict = utils['SERIAL']['ANS'][aws]
    r = self._write(self._cmd(c))
    return { k:self._answer(r,*v) for k,v in a.items()}

  def turn(self,state:str='on') -> bool: # on | off
    c = utils['SERIAL']['REQ']['write']
    t = utils['SERIAL']['PARAMS']['turn']
    if state not in t:
      print('unknown state')
      return
    cmd = self._cmd(c,*t[state])
    self._write(cmd)
    print('turned',state)
    return True

  def close(self):
    """close the open serial port
    """    
    self.ser.close()

  def _cmd(self,*args:list) -> bytes:
    cmd = args
    print(cmd)
    return serial.to_bytes(cmd)

  def _answer(self,bytestr:bytes,pos:int=0,length:int=1) -> int:
    start = pos*2
    end = start+length*2
    bits =[bin(b)[-4:] for b in bytestr]
    try:
      value = int('0b'+''.join(bits[start:end][::-1]),2)
    except:
      return 0
    return value

#sys.modules[__name__] = Eth