from flask import Flask, request, jsonify
import sensors.RF603.driver as RF603
import subprocess
from time import sleep
import os, json5
import os.path as path
from dotenv import load_dotenv
import importlib.util

### CONST ###

GIT_PATH = path.abspath(path.join(path.dirname(path.realpath(__file__)),''))
GIT_DIR = GIT_PATH.split(path.sep)[-1]

DRIVER_LOCATIONS_PATH = './utils/driver_locations.json5'

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

def load_sensors(mode:str, devices:list=None):
  def import_from_path(name:str,path:str):
    spec = importlib.util.spec_from_file_location(name, path)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    return driver

  def multi_import(sources:dict,mode:str=mode):
    drivers = [import_from_path(source['name'],source['path']) for source in sources]
    return [getattr(driver, mode) for driver in drivers]
  
  sources = get_driver_list(devices)
  drivers = multi_import(sources, mode)
  sensors = [driver() for driver in drivers]
  return sensors

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
  
  app.run(host="0.0.0.0", debug=True)