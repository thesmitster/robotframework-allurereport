from AllureListener import AllureListener
import os

class AllureLibrary(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self, logdir='reports/'):
        self.ROBOT_LIBRARY_LISTENER = AllureListener(logdir)
