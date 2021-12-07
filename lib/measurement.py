from time import sleep, time

class Measurement(object):
  def __init__(self, sensor):
    self.sensor = sensor
  
  def start(self, rate:int=1, duration:float= 10.0) -> list:
    start = time()
    meas = []
    self.sensor.open()
    while time() <= start + duration:
      meas.append(self.sensor.measure())
      sleep(1/rate)
    self.sensor.close()
    return meas