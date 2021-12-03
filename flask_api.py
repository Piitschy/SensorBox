from flask import Flask, request, jsonify
import drivers.RF603.driver as RF603
import subprocess
from time import sleep
import os, json5
import os.path as path
from dotenv import load_dotenv
import importlib.util
from utils.db import DB
from utils.confdict import conf

### CONST ###

GIT_PATH = path.abspath(path.join(path.dirname(path.realpath(__file__)),''))
GIT_DIR = GIT_PATH.split(path.sep)[-1]

DRIVER_LOCATIONS_PATH = './utils/driver_locations.json5'
CONFIG_PATH = './utils/config.json5'

### ENV ###

ENV_KEYS = [
  'GIT_USER',
  'GIT_PASSWORD',
  'GIT_SERVER'
]

load_dotenv(GIT_PATH)
env = { k:os.getenv(k) for k in ENV_KEYS }
env.update({'GIT_DIR':GIT_DIR})


### CMDs ###

CMD = {
  'update': ['git','pull',f'https://{env["GIT_USER"]}:{env["GIT_PASSWORD"]}@{env["GIT_SERVER"]}/{env["GIT_USER"]}/{env["GIT_DIR"]}'],
  'requirements': ['sudo','pip','install','-r',GIT_PATH+'/requirements.txt'],
  'reboot': ['sudo','reboot']
}

### FUNCTIONS ###

def exec_command(name:str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text:bool=True, **kwargs):
  if name not in CMD:
    return None
  return subprocess.run(CMD[name], stdout=stdout, stderr=stderr, text=text, **kwargs).stdout

def get_kwargs_from_request(request,*args) -> dict:
  kwargs = {}
  for arg in args:
    if arg in request.args:
      kwargs.update({arg:request.args[arg]})
    else:
      kwargs.update({arg:None})
  return kwargs

def get_driver_list(filter_list:list=None):
  with open(DRIVER_LOCATIONS_PATH) as f:
    sources = json5.load(f)
  if not filter_list:
    return sources
  return {k:v for k, v in sources.items() if k in filter_list}

def load_drivers(mode:str, devices:list=None,*args,**kwargs) -> list:
  '''
  Lädt sensoreninstanzen in eine Liste.
  '''
  def import_from_path(name:str,path:str):
    spec = importlib.util.spec_from_file_location(name, path)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    return driver

  def multi_import(sources:dict,mode:str=mode):
    drivers = [import_from_path(name,source['path']) for name, source in sources.items()]
    return [getattr(driver, mode) for driver in drivers]
  
  sources = get_driver_list(devices)
  drivers = multi_import(sources, mode)
  #sensors = [driver(*args,**kwargs) for driver in drivers]
  return drivers

### FLASK ###

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
  return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/update', methods=['GET'])
def update():
  print("Updating...",env['GIT_SERVER'])
  result = exec_command('update')
  # print(exec_command('requirements'))
  return result

@app.route('/reboot', methods=['GET'])
def reboot():
  return exec_command('reboot')

@app.route('/sensores/add', methods=['GET'])
def detect_sensors():
  kwargs = get_kwargs_from_request(request,"device")
  new_sensors = load_drivers('/dev/ttyUSB0')
  db.write('s1',new_sensors)
  return 

@app.route('/sensores/drivers', methods=['GET'])
def show_drivers():
  kwargs = get_kwargs_from_request(request,"device")
  drivers = get_driver_list(kwargs["device"])
  return drivers

@app.route('/sensores/measure', methods=['GET'])
def get_measure():
  ms = {s.device:s.measure() for s in sensors}
  return ms

if __name__ =='__main__':
  db = DB()
  s = RF603.Serial()#load_drivers('Serial',['RF603'])[0]('/dev/ttyUSB0')
  s.close()
  db.write('s',s)
  ss:RF603.Serial = db.read('s')
  ss.open()
  print(ss.identify())
  #app.run(host="0.0.0.0", debug=True)