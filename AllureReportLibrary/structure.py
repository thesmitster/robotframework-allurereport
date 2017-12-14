from allure.rules import xmlfied, Attribute, Element, WrappedMany, Nested, Many, \
    Ignored
from allure.constants import ALLURE_NAMESPACE, COMMON_NAMESPACE
from allure.structure import IterAttachmentsMixin

import os
import jprops
import collections
import subprocess

# overwriting the base class in allure.structure with an additional URL param.
class Environment(xmlfied('environment',
                          namespace=COMMON_NAMESPACE,
                          id=Element(),
                          name=Element(),
                          url=Element(), # Added
                          parameters=Many(Nested()))):
    pass

# Overwriting the base class in allure.structure with an additional SEVERITY attribute.
class TestCase(IterAttachmentsMixin,
               xmlfied('test-case',
                       id=Ignored(),  # internal field, see AllureTestListener
                       name=Element(),
                       title=Element().if_(lambda x: x),
                       description=Element().if_(lambda x: x),
#                        description=Element(),
                       failure=Nested().if_(lambda x: x),
                       steps=WrappedMany(Nested()),
                       attachments=WrappedMany(Nested()),
                       labels=WrappedMany(Nested()),
                       status=Attribute(),
                       severity=Attribute(), # Added
                       start=Attribute(),
                       stop=Attribute())):
    pass

class AllureProperties(object):
     
    def __init__(self, propertiesPath):
        self.path = propertiesPath
        if os.path.exists(self.path) is True: 
            with open(self.path) as fp:
                self.properties = jprops.load_properties(fp, collections.OrderedDict)
            fp.close()
        else:
            self.properties = {}
            self.set_property("allure.issues.id.pattern", "\\b([A-Z]{1,3}[-][0-9]{1,4})\\b")
            self.set_property("allure.issues.tracker.pattern", "http://jira.yourcompany.com/tests/%s")
            self.set_property("allure.tests.management.pattern", "http://tms.yourcompany.com/tests/%s")
            self.set_property("allure.cli.logs.xml", "./allure-report")
            self.set_property("allure.cli.logs.xml.clear", "True")
            
#             return False
         
#         return properties
         
    def save_properties(self, path=None):
    # store the Allure properties
    #
        if(path is None):
            output_path = self.get_property('allure.cli.logs.xml')+'\\allure.properties'
        else:
            output_path = path
         
        with open(output_path, 'w+') as fp:
            jprops.store_properties(fp, self.properties, timestamp=False)
        fp.close()
         
        return True
 
    def get_property(self, name):
        
        if name in list(self.properties.keys()):
            return self.properties[name]
        else:
            return None
 
    def get_properties(self):
         
        return self.properties
 
    def set_property(self, name, value):
         
        self.properties[name] = value
         
        return True