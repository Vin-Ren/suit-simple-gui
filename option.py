

class Option:
    """Option With case-insensitivity"""
    OPTIONS = {}
    
    def __setattr__(self, name, value):
        if name not in super().__getattribute__('ON_INSTANCE_ATTRS'):
            return self.extras.__setitem__(name, value)
        return super().__setattr__(name, value)
    
    def __setitem__(self, name, value):
        return self.extras.__setitem__(name, value)
    
    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return super().__getattribute__('extras').__getitem__(name)
    
    def __getitem__(self, name):
        return self.extras.__getitem__(name)
    
    def __init__(self, name: str, BeatsList: list=[], **extra_attributes):
        super().__setattr__('_name', name)
        super().__setattr__('BeatsList', [str(option).lower() for option in BeatsList])
        super().__setattr__('extras', extra_attributes)

        self.__class__.OPTIONS[name] = self
        
        d = dict(self.__class__.__dict__)
        d.update(self.__dict__)
        super().__setattr__('ON_INSTANCE_ATTRS', d)

    def __repr__(self):
        return "<Option Object Name={} BeatsList={}>".format(self.name, "[%s]" % ",".join(self.BeatsList))

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self.OPTIONS[new_name] = self.OPTIONS.pop(self.name)
        self._name = new_name

    def add_beats(self, option):
        self.BeatsList.append(str(option).lower())

    def beats(self, other):
        if str(other).lower() == str(self).lower():
            return -1
        return str(other).lower() in self.BeatsList


Batu = Option('Batu', ['Gunting'], display_char="✊")
Kertas = Option('Kertas', ['Batu'], display_char="🖐️")
Gunting = Option('Gunting', ['Kertas'], display_char="✌️")
