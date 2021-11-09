from flask import Flask
import subprocess
import os
import os.path as path
from dotenv import load_dotenv

ENV_KEYS = [
  'GIT_USER',
  'GIT_PASSWORD',
  'GIT_SERVER'
]

GIT_PATH = path.abspath(path.join(path.dirname(path.realpath(__file__)),'..'))
GIT_DIR = GIT_PATH.split(path.sep)[-1]

load_dotenv(GIT_PATH)
env = { k:os.getenv(k) for k in ENV_KEYS }
env.update({'GIT_DIR':GIT_DIR})

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
  return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/update', methods=['GET'])
def update():
  cmd = ['git','pull',f'https://{env["GIT_USER"]}:{env["GIT_PASSWORD"]}@{env["GIT_SERVER"]}/{env["GIT_USER"]}/{env["GIT_DIR"]}']
  print(cmd)
  result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  return result.stdout



app.run()