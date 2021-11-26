import shelve

DB_PATH = './utils/flask_db'

### DATABASE ###
class DB():
  def __init__(self,db_path:str=DB_PATH):
    self.db_path = db_path
    db = shelve.open(db_path)
    db.close()

  def write(self,key:str,payload):
    with shelve.open(self.db_path) as db:
      db[key]=payload
    return True

  def read(self,key:str):
    with shelve.open(self.db_path) as db:
      payload = db[key]
    return payload
  
  def delete(self,key:str):
    with shelve.open(self.db_path) as db:
      del db[key]
    return True