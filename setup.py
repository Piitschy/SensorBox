import subprocess

def install_requirements():
  cmd = ['sudo','pip','install','-r','requirements.txt']
  result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  return result.stdout

if __name__ == '__main__':
  install_requirements()