

import random


class Option:
    """Option With case-insensitivity"""
    DIRECT_MODIFIABLE_INSTANCE_ATTRS = ['name']
    OPTIONS = {}
    
    @classmethod
    def random(cls):
        return random.choice(list(cls.OPTIONS.values()))

    def __setattr__(self, name, value):
        return self.__setitem__(name, value)

    def __setitem__(self, name, value):
        if name not in super().__getattribute__('DIRECT_MODIFIABLE_INSTANCE_ATTRS'):
            return self._data.__setitem__(name, value)
        return super().__setattr__(name, value)

    def __getattribute__(self, name):
        try:
            # FOR DEBUGGING
            # print('__getattribute__: %s.%s' % (super().__getattribute__('_data').get('name'), name))
            return super().__getattribute__(name)
        except AttributeError:
            return self._data.__getitem__(name)

    def __getitem__(self, name):
        return self._data.__getitem__(name)

    def __init__(self, name: str, beatsList: list=[], **extra_attributes):
        # DO NOT USE DUNDER VARIABLES. IT WOULD PREPEND "_<CLASSNAME>" TO THE FRONT OF THE GIVEN ATTRIBUTE NAME
        super().__setattr__('_data', {'name':name, 'beatsList':beatsList})
        self._data.update(extra_attributes)
        
        self.OPTIONS[name] = self

    def __repr__(self):
        return "<Option Object Name={} BeatsList={}>".format(self.name, "[%s]" % ",".join(self.beatsList))

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self._data.get('name')

    @name.setter
    def name(self, new_name):
        self.OPTIONS[new_name] = self.OPTIONS.pop(self.name)
        self._data['name'] = new_name

    def add_beats(self, option):
        self.beatsList.append(str(option).lower())

    def beats(self, other):
        if str(other).lower() == str(self).lower():
            return -1
        return str(other).lower() in self.beatsList


Batu = Option('Batu', ['Gunting'], display_char="✊")
Kertas = Option('Kertas', ['Batu'], display_char="🖐️")
Gunting = Option('Gunting', ['Kertas'], display_char="✌️")
