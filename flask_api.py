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

DB_SENS_PATH = './var/db_sensors'
DB_MEAS_PATH = './var/db_measurements'

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

  # ROUTE FUNCTS
  
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
      return jsonify({
        'massage':f'u need 2 PUT like the default',
        'default': default
      }),200

    sensors = {}
    for name, sensor in db_sens.read_all().items():
      sensors.update({name:{k:v for k, v in dict(sensor.__dict__).items() if isinstance(v,(int, str))}})
    return jsonify(sensors)
  
  if request.method == 'DELETE':
    if 'delete' in request.args and 'name' in kwargs:
      name = kwargs['name']
      db_sens.delete(name)
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
      db_sens.write(params['name'],s)
      return jsonify(ident),200
  return jsonify(kwargs),200 

@app.route('/drivers', methods=['GET'])
def show_drivers():
  kwargs = get_kwargs_from_request(request,"device")
  drivers = get_driver_list(kwargs["device"])
  return drivers

@app.route('/measure/<name>', methods=['GET'])
def get_measure(name):
  s = db_sens.read(name)
  s.open()
  result = s.measure()
  s.close()
  return jsonify({
    'data' : result
  }), 200

@app.route('/schedule', methods=['GET','PUT','DELETE'])
def schedule():
  default = {
    "name" : "measurement",
    "senor_name"  : "sensor",
    "rate": 1,
    "duration": 10.0,
    "start_time" : None,
    "delay" : 0,
    "demo": True
  }
  kwargs = dict(request.get_json() or {})
  schedule_keys = ['id']+list(default.keys())
  schedules = [{ k: p['kwargs'][k] for k in schedule_keys if k in p['kwargs'] } for p in pool.procs]
  schedule_ids = [p['id'] for p in pool.procs]
  
  # GET
  if request.method == 'GET':
    if 'info' in request.args:
      return jsonify({
        'massage':f'u need 2 PUT like the default',
        'default': default
      }),200
    return jsonify({'data':schedules}), 200
  
  # PUT
  if request.method == 'PUT':
    if not all(e in kwargs for e in default):
      return jsonify({'error':f'you need all of these params: {default}'}),400
    
    params = default | kwargs
    
    sName = params['senor_name']
    if sName in schedule_ids:
      pool.delete_process(sName)
    if sName not in db_sens.read_all():
      return jsonify({'error':'sensor not found'})
    
    s = db_sens.read(params['senor_name'])
    messung = Measurement(s)

    pool.add_process(
      function=messung.start,
      #id=sName,
      rate=params['rate'],
      duration=params['duration'],
      name=params['name'],
      db=db_meas,
      demo=params['demo']
    )
    
    return jsonify({
      'massage':f'scheduled "{params["name"]}" successfull',
      'data': params
    }), 200

@app.route('/schedule/start', methods=['GET'])
def start_schedule():
  result = pool.execute()
  return jsonify({'data':result}), 200

@app.route('/measurements', methods=['GET'])
def load_measurements():
  result = db_meas.read_all()
  return jsonify({
    'data' : result
  }), 200

@app.route('/measurements/<name>', methods=['GET'])
def load_measurement(name):
  try:
    result = db_meas.read(name)
  except KeyError:
    return jsonify({'error': 'unknown measurement'}), 404
  return jsonify({
    'data' : result
  }), 200

if __name__ =='__main__':
  db_sens = DB(DB_SENS_PATH)
  db_meas = DB(DB_MEAS_PATH)
  pool = MultiProc()
  app.run(host="0.0.0.0", debug=True)