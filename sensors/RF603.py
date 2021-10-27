import sys
import numpy as np
import socket
import struct
from typing import Tuple, List
#import usb.core
import serial
from sensors.utils import RF603 as utils

### BASE FUNKTIONS

class Sensor(object):

  ENDIAN = '<H'
  NORM = int(str(4000),16)

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
      return struct.unpack(self.ENDIAN, bytestr[pos:pos+2])[0]
    elif bits == 8:
      return int(bin(bytestr[pos]),2)
    else:
      print('Wrong bits')
      return 0

  def _get_distance(self,d,s:int=50):
      return (d*s)/self.NORM

### CONECTIONS ###

class Eth(Sensor): #Default
  """Default Mode of this module

  Returns:
      RF603.ETH: Instance of RF603 via ethernet
  """

  def __init__(self, ip:str=utils.ETH.IP_SOURCE, udp_port:int=utils.ETH.UDP_PORT_DEST, serial:int=None, ip_dest:str=utils.ETH.IP_DEST, auto_connect=True):
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
    self.sensor_addr = (self.ip_source,utils.ETH.UDP_PORT_SOURCE)
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
      if addr == (ip,utils.ETH.UDP_PORT_SOURCE) or found_serial == serial:
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
      serial =  self._struc_unpack(data,utils.ETH.STRUC['serial'])
      base = self._struc_unpack(data,utils.ETH.STRUC['base'])
      mRange = self._struc_unpack(data,self.STRUC['mRange'])
      dists = np.array([self._get_distance(m,mRange) for m in measurements])
      return dists, serial, base, mRange


class _Serial(Sensor):

  parity = {
    'odd' : serial.PARITY_ODD,
    'even' : serial.PARITY_EVEN,
  }

  def __init__(self,port='/dev/ttyUSB0',addr:int=0x01,timeout:int=0.03,parity:str='even'):
    self.ser = serial.Serial(port,timeout=timeout,parity=self.parity[parity])
    self.addr = addr
    if not self.ser.is_open:
      self._alert('Device not found')
      return 
    self.identify()
  
  def write(self,data:bytes):
    self.ser.write(data)
    return self.ser.read(64)

  def write_cmd(self,request:int,param:int=None,value:int=None):
    cmd = self._cmd(request=request,param=param,value=value)
    return self.write(cmd)

  def identify(self):
    result = self.request('ident')
    print(result)
    self.set_ident() # einsetzten
    return result
  
  def measure(self):
    result = self.request('measure')
    return self._get_distance(result['value'],self.mRange)

  def request(self,cmd:str,aws:str=None):
    aws = aws or cmd
    c:int = utils.SERIAL.CMDS[cmd]
    a:dict = utils.SERIAL.ANS[aws]
    r = self.write(self._cmd(c))
    return { k:self._answer(r,*v) for k,v in a.items()}

  def turn(self,state:str='on'): # on | off
    c = utils.SERIAL.CMDS['write']
    t = utils.SERIAL.PARAMS['turn']
    if state not in t:
      print('unknown state')
      return
    cmd = self._cmd(c,*t[state])
    self.write(cmd)
    print('turned',state)
    return True

  def close(self):
    self.ser.close()

  def _cmd(self,request:int,param:int=None,value:int=None):
    cmd = [self.addr]+request
    cmd += [param,0x80] if param is not None else []
    cmd += [value,0x80] if value is not None else []
    return serial.to_bytes(cmd)

  def _answer(self,bytestr:bytes,pos:int=0,length:int=1):
    start = pos*2
    end = start+length*2
    bits =[bin(b)[-4:] for b in bytestr]
    return int('0b'+''.join(bits[start:end][::-1]),2)

class _USB(Sensor):
  def __init__(self,idVendor=0x0403,idProduct=0x6001):
    import usb.core
    self.dev=usb.core.find(idVendor=idVendor, idProduct=idProduct)
    try:
      eps=self.dev[0].interfaces()[0].endpoints()
      self.ep_in=eps[0]
      self.ep_out=eps[1]
    except TypeError:
      self._alert('Device not found')
      exit(1)
    self.i=self.dev[0].interfaces()[0].bInterfaceNumber
    self.dev.reset()
    
    if self.dev.is_kernel_driver_active(self.i):
      self.dev.detach_kernel_driver(self.i)

    self.dev.set_configuration()
    self.eaddr_in=self.ep_in.bEndpointAddress
    self.eaddr_out=self.ep_out.bEndpointAddress

  def read(self,size_or_buffer:int=1024,timeout=1000):
    return self.dev.read(self.eaddr_in,size_or_buffer,timeout)
  
  def write(self,req_code:bytes=None,msg:bytes=b'',addr:bytes=b'0x01',timeout=1000):
    payload = addr+req_code+msg
    return self.dev.write(self.eaddr_out,payload,timeout)

class RS232(_Serial, _USB):
  def __init__(self,mode:str='serial',idVendor=0x0403, idProduct=0x6001): #mode: usb | serial
    if mode == "usb":
      _USB.__init__(self, idVendor=idVendor, idProduct=idProduct)
    if mode == "serial":
      _Serial.__init__(self)

class RS485(RS232):
  pass



#sys.modules[__name__] = Eth