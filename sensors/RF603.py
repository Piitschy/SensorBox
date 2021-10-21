import sys
import numpy as np
import socket
import struct
from typing import Tuple, List
import usb.core

### DUMMY ###

DATA = b'\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xd9\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xdb\x15\x03\xda\x15\x03\xdb\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xdb\x15\x03\xda\x15\x03\xdb\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xd9\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xdb\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xd9\x15\x03\xda\x15\x03\xda\x15\x03\xdb\x15\x03\xda\x15\x03\xda\x15\x03\xdb\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xdb\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xda\x15\x03\xa2s}\x00\xf4\x01\x97\x00'

### BASE FUNKTIONS

class Sensor(object):
  def turn_on(self):
    pass

### CONECTIONS ###

class Eth(Sensor): #Default
  """Default Mode of this module

  Returns:
      RF603.ETH: Instance of RF603 via ethernet
  """
  NORM = int(str(4000),16)
  ENDIAN = '<H'
  IP_DEST = '255.255.255.255'
  IP_SOURCE = '192.168.0.3'
  UDP_PORT_DEST = 603
  UDP_PORT_SOURCE = 6003
  STRUC = { #position in bytestring
    'no_of_measurements': 168,
    'len_of_measurements': 3,
    'serial': 504,
    'base': 506,
    'mRange': 508
  }

  def __init__(self, ip:str=IP_SOURCE, udp_port:int=UDP_PORT_DEST, serial:int=None, ip_dest:str=IP_DEST, auto_connect=True):
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
    self.sensor_addr = (self.ip_source,self.UDP_PORT_SOURCE)
    self.ip_dest = ip_dest
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
      self.socket.bind(('',udp_port))
    except PermissionError:
      print("no permissions to open this udp port... \ntry to start with sudo/admin!")
      return
    self.serial = serial
    self.base = self.mRange = None
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
      if addr == (ip,self.UDP_PORT_SOURCE) or found_serial == serial:
        print(f'Found {found_serial} on {addr[0]}:{addr[1]}')
        break
    self.ip_source = addr[0]
    self.udp_port = addr[1]
    self.base = base
    self.mRange = mRange
    self.serial = serial
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
      serial =  self._struc_unpack(data,self.STRUC['serial'])
      base = self._struc_unpack(data,self.STRUC['base'])
      mRange = self._struc_unpack(data,self.STRUC['mRange'])
      dists = np.array([self._get_distance(m,mRange) for m in measurements])
      return dists, serial, base, mRange

  def _struc_unpack(self,bytestr:bytes,pos:int=0,bits:int=16):
    if bits == 16:
      return struct.unpack(self.ENDIAN, bytestr[pos:pos+2])[0]
    else:
      return int(bin(bytestr[pos]),2)

  def _get_distance(self,d,s:int=50):
    return (d*s)/self.NORM
  
  def _alert(self,text):
    print(text)

class _Serial(Sensor):
  def __init__(self):
    pass

class _USB(Sensor):
  def __init__(self,idVendor=0x0403,idProduct=0x6001):
    self.dev=usb.core.find(idVendor=idVendor, idProduct=idProduct)
    self.ep=self.dev[0].interfaces()[0].endpoints()[0]
    self.i=self.dev[0].interfaces()[0].bInterfaceNumber
    self.dev.reset()
    
    if self.dev.is_kernel_driver_active(self.i):
      self.dev.detach_kernel_driver(self.i)

    self.dev.set_configuration()
    self.eaddr=self.ep.bEndpointAddress

  def read(self):
    return self.dev.read(self.eaddr,1024)

class RS232(_Serial, _USB):
  def __init__(self,mode:str='usb',idVendor=0x0403, idProduct=0x6001): #mode: usb | serial
    if mode == "usb":
      _USB.__init__(self, idVendor=idVendor, idProduct=idProduct)
    if mode == "serial":
      _Serial.__init__(self)

class RS485(RS232):
  pass

#sys.modules[__name__] = Eth