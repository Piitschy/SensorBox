from flask import Flask, request, jsonify
import drivers.RF603.driver as RF603
import subprocess
from time import sleep
import os, json5
import os.path as path
import sys
from dotenv import load_dotenv
import importlib.util
from lib.utils import DB, MultiProc, conf
from lib.measurement import Measurement

### CONST ###

GIT_PATH = path.abspath(path.join(path.dirname(path.realpath(__file__)),''))
GIT_DIR = GIT_PATH.split(path.sep)[-1]

DRIVER_LOCATIONS_PATH = './utils/driver_locations.json5'
CONFIG_PATH = './utils/config.json5'

DB_PATH = './var/flask_db'

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

def import_from_path(name:str,path:str):
  spec = importlib.util.spec_from_file_location(name, path)
  driver = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(driver)
  return driver

def load_drivers(mode:str, devices:list=None,*args,**kwargs) -> list:
  '''
  Lädt sensoreninstanzen in eine Liste.
  '''
  def multi_import(sources:dict,mode:str=mode):
    drivers = [import_from_path(name,source['path']) for name, source in sources.items()]
    return [getattr(driver, mode) for driver in drivers]
  
  sources = get_driver_list(devices)
  drivers = multi_import(sources, mode)
  #sensors = [driver(*args,**kwargs) for driver in drivers]
  return drivers

def load_driver(device:str, mode:str, *args,**kwargs):
  source = get_driver_list([device])[device]
  print(source)
  driver = import_from_path(device, source['path'])
  print(driver)
  return getattr(driver, mode)

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

@app.route('/sensors', methods=['GET','PUT','DELETE'])
def sensors():
  default = {
    "name"  : "sensor",
    "device": [
      "RF603",
      "OPT3"
    ],
    "port"  : "/dev/ttyUSB0",
    "addr"  : 1
  }
  kwargs = dict(request.get_json())
  
  # GET
  if request.method == 'GET':
    if 'info' in request.args:
      return jsonify({'massage':f'u need 2 PUT like this: {default}'}),200
  
    sensors = {}
    for name, sensor in db.read_all().items():
      sensors.update({name:{k:v for k, v in dict(sensor.__dict__).items() if isinstance(v,(int, str))}})
    return jsonify(sensors)
  
  if request.method == 'DELETE':
    if 'delete' in request.args and 'name' in kwargs:
      name = kwargs['name']
      db.delete(name)
      return jsonify({'massage':f'{name} deleted'}), 200
    return jsonify({'error':'send {name: ... } in body and "delete" as arg to delete something'}), 400
  
  # PUT
  if request.method == 'PUT':    
    if not all(e in kwargs for e in default):
      return jsonify({'error':f'you need all of these params: {default}'}),400
    
    params = default | kwargs
    if params['device'] == 'RF603':
      s = RF603.Serial(params['port'])
      ident = s.identify()
      s.close()
      db.write(params['name'],s)
      return jsonify(ident),200
  return jsonify(kwargs),200 

@app.route('/drivers', methods=['GET'])
def show_drivers():
  kwargs = get_kwargs_from_request(request,"device")
  drivers = get_driver_list(kwargs["device"])
  return drivers

@app.route('/measure/<name>', methods=['GET'])
def get_measure(name):
  s = db.read(name)
  s.open()
  result = s.measure()
  s.close()
  return jsonify(result), 200

@app.route('/start_measure/<senor_name>', methods=['GET'])
def start_measure(senor_name):
  rate = int(request.args.get('rate') or 1)
  duration = float(request.args.get('duration') or 10.0)
  meas_name = str(request.args.get('name') or senor_name+'_meas')
 
  #pool = MultiProc()
  #pool.add_process(
  #  function=messung.start,
  #  rate=rate,
  #  duration=duration,
  #  name=meas_name,
  #  db=db
  #)
  #pool.start()
  
  s = db.read(senor_name)
  messung = Measurement(s)
  result = messung.start(
    rate=rate,
    duration=duration,
    name=meas_name,
    db=db
  )
  return jsonify({
    'massage':f'measure "{meas_name}" successfull',
    'data': result
  }), 200

@app.route('/measurement/<name>', methods=['GET'])
def load_measurement(name):
  try:
    result = db.read(name)
  except KeyError:
    return jsonify({'message': 'unknown measurement'}), 404
  return jsonify(result), 200


if __name__ =='__main__':
  db = DB(DB_PATH)
  app.run(host="0.0.0.0", debug=True)