from flask import Flask
import sensors.RF603.driver as RF603
import subprocess
from time import sleep
import os
import os.path as path
from dotenv import load_dotenv

### CONST ###

GIT_PATH = path.abspath(path.join(path.dirname(path.realpath(__file__)),'..'))
GIT_DIR = GIT_PATH.split(path.sep)[-1]


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

@app.route('/measure', methods=['GET'])
def measure():
  s = RF603.Serial()
  m = s.measure()
  print(m)
  return m

if __name__ =='__main__':
    app.run(host="0.0.0.0", debug=True)