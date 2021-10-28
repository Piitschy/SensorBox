
class RF603:
  class ETH:
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


  class SERIAL:
    REQ = {
      'ident': [0x81],
      'write': [0x83],
      'measure':[0x86]
    }

    PARAMS = {
      'turn' : {
        'on' : [0x80,0x81],
        'off': [0x80,0x80]
      }
    }

    ANS = {
      'ident': {
        'type': [0],
        'firmware':[1],
        'serial':[2,2],
        'base': [4,2],
        'mRange':[6,2]
      },
      'measure':{
        'value':[0,2]
      }
    }