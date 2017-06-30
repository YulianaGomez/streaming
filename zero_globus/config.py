import threading
from singleton import Singleton
from Queue import Queue

class MyConfig(object):
    """
    Shared context between all programs. Everything that instantiates it will get the same object sharing same memory
    """
    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        """
        Load configuration and get the initial set of rules
        """
        self.q = Queue(0)

        pass
