import numpy as np
import socket
import struct

# CLASSES #

class RF603:
  NORM = int(str(4000),16)
  ENDIAN = '<H'
  IP_DEST = '255.255.255.0'
  IP_SOURCE = '192.168.0.3'
  UDP_PORT_DEST = 603
  UDP_PORT_SOURCE = 6003
  STRUC = {
    'no_of_measurements': 168,
    'len_of_measurements': 3,
    'serial': 504,
    'base': 506,
    'mRange': 508
  }

  def __init__(self, ip_source=IP_SOURCE, ip_dest=IP_DEST, udp_port=UDP_PORT_DEST):
    self.ip_source = ip_source
    self.ip_dest = ip_dest
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    self.socket.bind(('',udp_port))

  def listen(self,buffer:int=1024):
    while True:
        data, addr = self.socket.recvfrom(buffer)
        dists,_ = self._unpack(data)

  def _unpack(self,data:bytes):
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