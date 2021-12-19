import sys, os
import json5
import numpy as np
import socket
import struct
from typing import Tuple, List
#import usb.core
import serial
#from sensors.utils import RF603 as utils

### CONSTANTS ###
UTILS_PATH = 'utils.json5'
SERIAL_PATH_DEFAULT = '/dev/ttyUSB0'

### LOAD UTILS ###
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, UTILS_PATH)
with open(filename) as f:
  content = f.read()
  utils = json5.loads(content)

### BASE FUNKTIONS ###

class Sensor(object):
  name = 'RF603'
  mRange = 0
  base = 0
  serial_no = 0
  firmware = 0
  device_type = 0

  def set_ident(self,device_type:int=0,firmware:int=0,serial_no:int=0,base:int=0,mRange:int=0):
    self.device_type = device_type
    self.firmware = firmware
    self.serial_no = serial_no
    self.base = base
    self.mRange = mRange

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

class Eth(Sensor): #Default
  """Default Mode of this module

  Returns:
      RF603.ETH: Instance of RF603 via ethernet
  """

  def __init__(self, ip:str=utils['ETH']['IP_SOURCE'], udp_port:int=utils['ETH']['UDP_PORT_DEST'], ip_dest:str=utils['ETH']['IP_DEST'], auto_connect=True):
    """Generates an Sensor object for RIFTEK RF603.
    You could find it by IP or serial number.
    Don't forget to connect after creating...

    Args:
        ip (str, optional): IP of the sensor. Defaults to IP_SOURCE.
        udp_port (int, optional): Target port of the sensor stream. Defaults to UDP_PORT_DEST.
        serial (int, optional): serial number. Defaults to None.
        ip_dest (str, optional): Target IP of the sensor (Not required). Defaults to IP_DEST.
    """
    self.ip_source = ip
    self.sensor_addr = (self.ip_source,utils['ETH']['UDP_PORT_SOURCE'])
    self.ip_dest = ip_dest
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
      self.socket.bind(('',udp_port))
    except PermissionError:
      print("no permissions to open this udp port... \ntry to start with sudo/admin!")
      return
    self.conneced = False
    if auto_connect:
      self.connect()

  def connect(self, ip:str=None, serial:int=None):
    """(re)connect to a sensor and override the object data...

    Args:
        ip (str, optional): IP of the sensor. Defaults to None.
        serial (int, optional): serial number. Defaults to None.

    Returns:
        bool: return True if connected
    """
    text='sensor '
    if ip:
      text += 'IP: '+ip
    if serial:
      text += 'serial: '+str(serial)
    print('Searching for',text)

    ip = ip or self.ip_source
    serial = serial or self.serial
    
    while True:
      _, found_serial, base, mRange, addr = self.receive(filter=False)
      if addr == (ip,utils['ETH']['UDP_PORT_SOURCE']) or found_serial == serial:
        print(f'Found {found_serial} on {addr[0]}:{addr[1]}')
        break
    self.ip_source = addr[0]
    self.udp_port = addr[1]
    self.set_ident(base=base, mRange=mRange,serial_no=serial)
    self.conneced = True
    return True

  def read(self):
    pass

  def listen(self,buffer:int=1024):
    """print live distance measurements

    Args:
        buffer (int, optional): buffer size of the listener. Defaults to 1024.
    """
    print('waiting for signal...\n')
    while True:
        distances = self.receive(buffer)[0]
        for d in distances:
          print(d)

  def receive(self,buffer:int=1024,filter:bool=True) -> Tuple[np.array, int, int, int, tuple[str, int]] or None:
    """Waiting for packets from connected sensor

    Args:
        buffer (int, optional): Size of the buffer - should be greater than 512. Defaults to 1024.

    Returns:
        np.array, int, int, int, tuple[str, int]: measure values, serial number, base distance, measurement range and address(IP, Port)
    """
    while True:
      data, addr = self.socket.recvfrom(buffer)
      if filter and (addr[0] != self.ip_source):
        continue
      dists, serial, base, mRange = self._unpack(data)
      if filter and (serial != self.serial):
        continue
      return dists, serial, base, mRange , addr

  def _unpack(self,data:bytes) -> Tuple[np.array, int, int, int]:
      measurements = np.array([self._struc_unpack(data,i) for i in range(0,504,3)])
      serial =  self._struc_unpack(data,utils['ETH']['POS']['serial'])
      base = self._struc_unpack(data,utils['ETH']['POS']['base'])
      mRange = self._struc_unpack(data,utils['ETH']['POS']['mRange'])
      dists = np.array([self._get_distance(m,mRange) for m in measurements])
      return dists, serial, base, mRange

class Serial(Sensor):
  """Parent class for alle Types of serial connections

  Args:
      Sensor: used sensor

  Returns:
      Sensor: Tools to communicate with given sensor
  """
  def __init__(self,port=SERIAL_PATH_DEFAULT,addr:int=0x01,timeout:int=0.03,name:str=None):
    self.ser = serial.Serial(port,timeout=timeout,parity=serial.PARITY_EVEN)
    self.addr = addr
    self.name = name or self.name
    if not self.ser.is_open:
      self._alert('Device not found')
      return 
    self.identify()
  
  def _write(self,data:bytes) -> bytes:
    """write a given bytestring on device and return the answer

    Args:
        data (bytes): command or request as bytes

    Returns:
        response (bytes): response of the device as bytestring
    """    
    self.ser.write(data)
    return self.ser.read(64)

  def write_cmd(self,request:int,param:int=None,value:int=None) -> bytes:
    """write a given command in (hex-)integers on device.
    The integer values can be found n the datasheet.

    Args:
        request (int): Number of the kind of request
        param (int, optional): request parameter. Defaults to None.
        value (int, optional): value of the request parameter. Defaults to None.

    Returns:
        bytes: response of the device as bytestring
    """    
    cmd = self._cmd(request=request,param=param,value=value)
    return self._write(cmd)

  def identify(self) -> dict:
    """send a identify request at device and set the response as sensor parameters

    Returns:
        dict: sensor parameters
    """    
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
    """get the currently measure value in mm

    Returns:
        float: distance in mm
    """    
    result = self.request('measure')
    return self._get_distance(result['value'],self.mRange)

  def request(self,req:str,aws:str=None)->dict:
    """encode and write the given command in hexaintegers at the sensor and decode the response.

    Args:
        req (str): kind of request. 'ident' | 'write' | 'measure' | ... (look at utils)
        aws (str, optional): expected format answer structure from utils. Defaults to equal to req.

    Returns:
        dict: formated answare of the device
    """    
    aws = aws or req
    c:int = utils['SERIAL']['REQ'][req]
    a:dict = utils['SERIAL']['ANS'][aws]
    r = self._write(self._cmd(c))
    return { k:self._answer(r,*v) for k,v in a.items()}

  def turn(self,state:str='on') -> bool: # on | off
    """turn the laser of the sensor on or off to get into power saving mode.

    Args:
        state (str, optional): 'on' | 'off'. Defaults to 'on'.

    Returns:
        bool: True if transmission successfull
    """    
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
  
  def open(self):
    """Reopen a port
    """
    self.ser.open()

  def _cmd(self,request:int,param:int=None,value:int=None) -> bytes:
    """concat he elements of a command (look at datasheet for details)

    Args:
        request (int): integer of request
        param (int, optional): integer of parameter. Defaults to None.
        value (int, optional): integer of values. Defaults to None.

    Returns:
        bytes: command as bytestring
    """    
    cmd = [self.addr]+request
    cmd += [param,0x80] if param is not None else []
    cmd += [value,0x80] if value is not None else []
    return serial.to_bytes(cmd)

  def _answer(self,bytestr:bytes,pos:int=0,length:int=1) -> int:
    """slice the given position (16bit) out of given bytestream.
    WARNING: IT'S IN 16bit!!!!!!

    Args:
        bytestr (bytes): for example: response of the sensor.
        pos (int, optional): startposition of the slice 16bit. Defaults to 0.
        length (int, optional): length of the slice in 16bit. Defaults to 1.

    Returns:
        int: byteslice
    """    
    start = pos*2
    end = start+length*2
    bits =[bin(b)[-4:] for b in bytestr]
    try:
      value = int('0b'+''.join(bits[start:end][::-1]),2)
    except:
      return 0
    return value

#sys.modules[__name__] = Serial()