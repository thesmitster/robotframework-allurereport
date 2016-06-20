# -*- coding: utf-8 -*-

"""
Created on Feb 23, 2014

@author: qatoe1991
"""
from six import text_type, iteritems
from contextlib import contextmanager
from functools import wraps
import os
import uuid
from lxml import etree
import py
import re
from robot.libraries.BuiltIn import BuiltIn
from structure import Attach, TestSuite, TestCase, TestKeyword, Failure
from utils import now
from robot.libraries.Screenshot import Screenshot
from robot.running.userkeyword import UserLibrary
import shutil


class AllureListener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, logdir):
        self.logdir = os.path.normpath(os.path.abspath(os.path.expanduser(os.path.expandvars(logdir))))
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
        else:
            for f in os.listdir(self.logdir):
                f = os.path.join(self.logdir, f)
                if os.path.isfile(f):
                    os.unlink(f)

        self.stack = []

        self.testsuite = None
        self.environment = {}

    def attach(self, title, contents, attach_type):
        attach = Attach(source=self._save_attach(contents, attach_type=attach_type),
                        title=title,
                        type=attach_type)
        self.stack[-1].attachments.append(attach)

    def _save_attach(self, body, attach_type):
        with self._attachfile("%s-attachment.%s" % (uuid.uuid4(), attach_type)) as f:
            if isinstance(body, text_type):
                 f.write(body.encode('utf-8'))
            else:
                f.write(body)
        return os.path.basename(f.name)

    def start_test(self, name, attributes):
        test = TestCase(name=name,
                        description=name,
                        start=now(),
                        attachments=[],
                        labels=[],
                        steps=[])
        self.stack.append(test)

    def end_test(self, name, attributes):
        test = self.stack[-1]
        if attributes.get('status') == 'PASS':
            test.status = 'passed'
            test.description=attributes.get('message')
        elif attributes.get('status')=='FAIL':
            test.status = 'failed'
            test.failure = Failure(message=attributes.get('message'), trace='')
        test.stop = now()
        self.testsuite.tests.append(test)
        return test

    def start_suite(self, name, attributes):
        self.testsuite = TestSuite(name=name,
                                   title=name,
                                   description=name,
                                   tests=[],
                                   labels=[],
                                   start=now())

    def end_suite(self, name, attributes):
        self.testsuite.stop = now()

        with self._reportfile('%s-testsuite.xml' % uuid.uuid4()) as f:
            self._write_xml(f, self.testsuite)

    def start_keyword(self, name, attributes):
        keyword = TestKeyword(name=name,
                            title=name,
                            attachments=[],
                            steps=[],
                            start=now(),
                            )
        if self.stack[-1]:
            self.stack[-1].steps.append(keyword)
        return keyword

    def end_keyword(self, name, attributes):
        return

    def log_message(self, msg):
        if '.png' in msg['message']:
            self.attach('LOG', msg['message'], 'html')

    def _move_attachment(self):
        path = os.getcwd()
        new_path = os.path.join(self.logdir, 'allure-report/data/')
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        for file in os.listdir(path):
            if file.endswith(".png"):
                shutil.move(os.path.join(path, file), os.path.join(new_path, file))

    def close(self):
        self._move_attachment()
    
    @contextmanager
    def _attachfile(self, filename):
        reportpath = os.path.join(self.logdir, filename)

        with open(reportpath, 'wb') as f:
            yield f

    @contextmanager
    def _reportfile(self, filename):
        reportpath = os.path.join(self.logdir, filename)
        encoding = 'utf-8'

        logfile = py.std.codecs.open(reportpath, 'w', encoding=encoding)

        try:
            yield logfile
        finally:
            logfile.close()

    def _write_xml(self, logfile, xmlfied):
        logfile.write(etree.tostring(xmlfied.toxml(), pretty_print=True, xml_declaration=False, encoding=text_type))
