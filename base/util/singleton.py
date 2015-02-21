# -*- coding: utf-8 -*-


class Singleton(object):
    def __new__(cls, new_instance_func=None):
        key = hash(cls)
        if not hasattr(cls, '_Singleton__instance_dict'):
            instance = new_instance_func(cls) if new_instance_func else super(Singleton, cls).__new__(cls)
            cls._Singleton__instance_dict = {key: instance}
            cls._initialized = False
            return instance
        elif key not in cls._Singleton__instance_dict:
            instance = new_instance_func(cls) if new_instance_func else super(Singleton, cls).__new__(cls)
            cls._Singleton__instance_dict[key] = instance
            return instance
        else:
            return cls._Singleton__instance_dict[key]
