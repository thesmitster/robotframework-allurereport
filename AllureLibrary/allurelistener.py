from six import text_type, iteritems
from contextlib import contextmanager
from functools import wraps
import os
import uuid
import re
from lxml import etree
import py
import re
import io
from robot.libraries.BuiltIn import BuiltIn
from structure import Attach, TestSuite, TestCase, TestKeyword, Failure, TestLabel
from utils import now
from robot.libraries.Screenshot import Screenshot
from robot.running.userkeyword import UserLibrary
import shutil
from rules import *
from constant import ROBOT_OUTPUT_FILES, Status, Robot, SEVERITIES, Label


class AllureListener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.issuetracker = BuiltIn().get_variable_value("${ISSUE_TRACKER}")
        self.logdir = BuiltIn().get_variable_value("${OUTPUT_DIR}")
        self.stack = []
        self.testsuite = None
        self.environment = {}
        """
        The lines above clean the entire directory form previous tests,
        expect the robotframework files.
        """
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
        else:
            for f in os.listdir(self.logdir):
                if f not in ROBOT_OUTPUT_FILES:
                    f = os.path.join(self.logdir, f)
                    if os.path.isfile(f):
                        os.unlink(f)

# Listener functions

    def start_test(self, name, attributes):
        test = TestCase(name=name,
                description=name,
                start=now(),
                attachments=[],
                labels=[],
                parameters=[],
                steps=[])
        self.stack.append(test)
        return
    
    def end_test(self, name, attributes):
        test = self.stack[-1]

        if attributes.get('status') == Robot.PASS:
            test.status = Status.PASSED
            test.description=attributes.get('message')
        elif attributes.get('status')==Robot.FAIL:
            test.status = Status.FAILED
            test.failure = Failure(message=attributes.get('message'), trace='')
        
        test.stop = now()

        if attributes['tags']:
            for tag in attributes['tags']:
                if tag.startswith('DIM'):
                    test.labels.append(TestLabel(
                        name=Label.ISSUE,
                        value=tag))
                elif tag in SEVERITIES:
                    test.severity = tag

        self.testsuite.tests.append(test)
        return test

    def start_suite(self, name, attributes):
        self.testsuite = TestSuite(name=name,
                title=name,
                description=name,
                tests=[],
                labels=[],
                start=now())
        return

    def end_suite(self, name, attributes):
        self.testsuite.stop = now()

        with self._reportfile('%s-testsuite.xml' % uuid.uuid4()) as f:
            self._write_xml(f, self.testsuite)
        return

    def start_keyword(self, name, attributes):
        keyword = TestKeyword(name=name,
                title=name,
                attachments=[],
                steps=[],
                start=now(),)
        if self.stack:
            self.stack[-1].steps.append(keyword)
        return keyword

    def end_keyword(self, name, attributes):
        return

    def log_message(self, msg):
        if msg['level']=='INFO':
            screenshot = re.search('[a-z]+-[a-z]+-[0-9]+.png',msg['message'])
            if screenshot:
                self.attach('{}'.format(screenshot.group(0)) , screenshot.group(0), 'png')
        
        return

    def close(self): 
        with self._attachfile('allure.properties') as f:
            if self.issuetracker:
                 f.write('allure.issues.tracker.pattern='+self.issuetracker+'%s')
        f.close()
        return


# Helper functions

    def attach(self, title, contents, attach_type):
        """
        This functions created the attachments and append it to the test.
        """
        contents = os.path.join(self.logdir, contents)

        with open(contents, 'rb') as f:
            file_contents = f.read()

        attach = Attach(source=self._save_attach(file_contents, attach_type=attach_type),
                        title=title,
                        type='image/'+attach_type)
        self.stack[-1].attachments.append(attach)
        return

    def _save_attach(self, body, attach_type):
        with self._attachfile("%s-attachment.%s" % (uuid.uuid4(), attach_type)) as f:
            if isinstance(body, text_type):
                f.write(body.encode('utf-8'))
            else:
                f.write(body)
        return os.path.basename(f.name)

    @contextmanager
    def _attachfile(self, filename):
        reportpath = os.path.join(self.logdir, filename)

        with open(reportpath, 'wb') as f:
            yield f

    @contextmanager
    def _reportfile(self, filename):
        """
        This creates the final xml file for every suite
        """
        reportpath = os.path.join(self.logdir, filename)
        encoding = 'utf-8'

        logfile = py.std.codecs.open(reportpath, 'w', encoding=encoding)

        try:
            yield logfile
        finally:
            logfile.close()

    def _write_xml(self, logfile, xmlfied):
        logfile.write(etree.tostring(xmlfied.toxml(), pretty_print=True, xml_declaration=False, encoding=text_type))


class AllureLibrary(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.1'

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = AllureListener()
