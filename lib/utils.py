import shelve, json
from multiprocessing import Manager, Process
from time import sleep


### DATABASE ###
class DB():
    def __init__(self, db_path: str):
        self.db_path = db_path
        db = shelve.open(db_path)
        db.close()

    def write(self, key: str, payload):
        with shelve.open(self.db_path) as db:
            db[key] = payload
        return True

    def read(self, key: str):
        with shelve.open(self.db_path) as db:
            payload = db[key]
        return payload

    def read_all(self) -> dict:
        with shelve.open(self.db_path) as db:
            payload = dict(db)
        return payload

    def delete(self, key: str):
        with shelve.open(self.db_path) as db:
            del db[key]
        return True

class conf(dict):
    def __init__(self, path: str = None, *args, **kwargs):
        super(conf, self).__init__(*args, **kwargs)
        self._path = path
        self.load()
    
    def load(self) -> dict:
        path = self._path
        with open(self._path, 'r') as file:
            self.__dict__ = dict(json.loads(file.read()))
        self._path = path

    def save(self) -> None:
        with open(self._path, 'w') as file:
            payload = dict(self.__dict__)
            del payload['_path']
            file.write(json.dumps(payload))

    def __setitem__(self, key, item):
        self.__dict__[key] = item
        self.save()

    def __getitem__(self, key):
        self.load()
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]
        self.save()

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        ret = self.__dict__.update(*args, **kwargs)
        self.save()
        return ret

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))
class MultiProc:
    def __init__(self, processes: list = []) -> None:
        """Hängt eine Liste von Funktionen an den Pool an:

        Args:
            processes (list): Liste an Funktionen oder FunktionsDicts:
                    [
                        function1, 

                        {
                            'id': ' ',
                            'func': function2,
                            'args': [...],
                            'kwargs': {...}
                        },
                        ...
                    ]
        """
        self.running = False
        self.manager = Manager()
        self.return_dict = self.manager.dict()
        self.jobs = []
        self.procs = []
        self.i = 0
        self.append_processes(processes)
        return

    def append_processes(self, processes: list):
        """Hängt eine Liste von Funktionen an den Pool an:

        Args:
            processes (list): Liste an Funktionen oder FunktionsDicts:
                    [
                        function1, 

                        {
                            'id': ' ',
                            'func': function2,
                            'args': [...],
                            'kwargs': {...}
                        },
                        ...
                    ]
        """
        if type(processes) is not list:
            processes = [processes]
        for proc in processes:
            if type(proc) != dict:
                proc = {'func': proc}
            if 'id' not in proc or not proc['id']:
                proc.update({'id': self.i})
            if 'args' not in proc:
                proc.update({'args': []})
            if 'kwargs' not in proc or not proc['kwargs']:
                proc.update({'kwargs': {}})
            self.procs.append(proc)
            self.i += 1

    def add_process(self, function, *args, **kwargs):
        """Fügt einen Prozess zum Pool hinzu

        Args:
            function (func,dict(func)): Funktion oder Dict von Funktionen
        """
        id = None
        if type(function) is dict:
            (id, function) = list(function.items())[0]
        p = {
            'id': id,
            'func': function,
            'args': args,
            'kwargs': kwargs
        }
        self.append_processes([p])

    def _worker(self, id, proc, *args, **kwargs):
        self.return_dict.update({id: proc(*args, **kwargs)})
        return

    def start(self) -> None:
        """Startet den Pool, unterbricht die Laufzeit jedoch nicht
        """
        for proc in self.procs:
            p = Process(target=self._worker, args=(
                proc['id'], proc['func'], *proc['args'], ), kwargs=proc['kwargs'])
            self.jobs.append(p)
            p.start()
        return

    def join(self) -> list:
        """Fängt alle Prozesse aus dem Pool ein und lässt die Laufzeit erst nach dem Fangen des letzten Prozesses weiterlaufen

        Returns:
            list: Liste aller Prozess-returns
        """
        for p in self.jobs:
            p.join()
        return dict(self.return_dict)

    def execute(self) -> list:
        """Lässt den Pool laufen und fängt ihn wieder.
        Gut geeignet vom Parallelisieren von Prozessen.

        Returns:
            list: Liste aller Prozess-returns
        """
        while self.running:
            sleep(0.1)
        self.running = True
        self.start()
        result =self.join()
        self.running = False
        return result
