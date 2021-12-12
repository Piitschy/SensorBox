from time import sleep, time
from datetime import datetime
import hashlib
import random

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

def hasher(s:str):  # this is not a good hashing function
    return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**6
  
def time_str(time:float, format:str = DATE_FORMAT, ms:bool = False) -> str:
  t = time if ms else int(time)
  return datetime.fromtimestamp(t).strftime(format)
  
class Measurement(object):
  def __init__(self, sensor):
    self.sensor = sensor
  
  def start(self, rate:int, duration:float, name:str=None, sensor:str=None, db=None, demo:bool=False) -> list:
    start = time()
    startDate = time_str(start, DATE_FORMAT)
    startTime = time_str(start, TIME_FORMAT)
    meas = []
    id = hasher(' '.join([startDate,startTime,name]))
    
    if demo:
      while time() <= start + duration:
        meas.append(random.randrange(12.5,500,0,1))
        sleep(1/rate)
    else:
      self.sensor.open()
      while time() <= start + duration:
        meas.append(self.sensor.measure())
        sleep(1/rate)
      self.sensor.close()
      sleep(0.1)
    
    dataset = {
      'name': name,
      'sensor': sensor,
      'rate': rate,
      'start_date': startDate,
      'start_time': startTime,
      'start': start,
      'duration': duration,
      'data': meas
    }
    if name and db:
      db.write(id,dataset)
    return dataset
  
