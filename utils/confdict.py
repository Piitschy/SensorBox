import json


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
