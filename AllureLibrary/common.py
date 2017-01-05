from six import text_type, iteritems
from contextlib import contextmanager
from functools import wraps
import os
import uuid

from lxml import etree
import py

import allure
from allure.constants import AttachmentType, Status
from allure.structure import Attach, TestStep, TestCase, TestSuite, Failure, EnvParameter
from structure import Environment
from allure.utils import now


class AllureImpl(allure.common.AllureImpl):
    '''
    AllureImpl extends and overwrites allure.common.AllureImpl.
    
    store_environment() has been extended to support the URL parameter/attribute. 
    
    All other Parent methods and attributes accessible.
    '''
    def __init__(self, logdir):
        super(AllureImpl, self).__init__(logdir)
        self.environment = {}
    
    def store_environment(self, environmentlist):
        '''Extension of allure.AllureImpl.store_environment due to lacking URL parameter'''
        
        if not self.environment:
            return

        id = environmentlist['id']
        name = environmentlist['name']
        url = environmentlist['url']

        environment = Environment(id=id, name=name, url=url, parameters=[])
        for key, value in iteritems(self.environment):
            environment.parameters.append(EnvParameter(name=key, key=key, value=value))

        with self._reportfile('environment.xml') as f:
            self._write_xml(f, environment)
