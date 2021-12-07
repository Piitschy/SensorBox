from time import sleep, time

class Measurement(object):
  def __init__(self, sensor):
    self.sensor = sensor
  
  def start(self, rate:int, duration:float, name:str=None, db=None) -> list:
    start = time()
    meas = []
    self.sensor.open()
    while time() <= start + duration:
      meas.append(self.sensor.measure())
      sleep(1/rate)
    self.sensor.close()
    sleep(0.3)
    if name and db:
      db.write(name,meas)
    return meas