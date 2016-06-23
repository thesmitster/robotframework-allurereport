import re
import sys

from six import u, unichr
from lxml import objectify
from namedlist import namedlist

from utils import unicodify


def element_maker(name, namespace):
    return getattr(objectify.ElementMaker(annotate=False, namespace=namespace,), name)


class Rule(object):
    _check = None

    def value(self, name, what):
        raise NotImplemented()

    def if_(self, check):
        self._check = check
        return self

    def check(self, what):
        if self._check:
            return self._check(what)
        else:
            return True


class Ignored(Rule):
    def if_(self, check):
        return False


class Element(Rule):

    def __init__(self, name='', namespace=''):
        self.name = name
        self.namespace = namespace

    def value(self, name, what):
        return element_maker(self.name or name, self.namespace)(unicodify(what))


class Attribute(Rule):

    def value(self, name, what):
        return unicodify(what)


class Nested(Rule):

    def value(self, name, what):
        return what.toxml()


class Many(Rule):

    def __init__(self, rule, name='', namespace=''):
        self.rule = rule
        self.name = name
        self.namespace = namespace

    def value(self, name, what):
        return [self.rule.value(name, x) for x in what]


class WrappedMany(Many):

    def value(self, name, what):
        values = super(WrappedMany, self).value(name, what)
        return element_maker(self.name or name, self.namespace)(*values)


def xmlfied(el_name, namespace='', fields=[], **kw):
    items = fields + list(kw.items())

    class MyImpl(namedlist('XMLFied', [(item[0], None) for item in items])):

        def toxml(self):
            el = element_maker(el_name, namespace)

            def entries(clazz):
                return [(name, rule.value(name, getattr(self, name)))
                        for (name, rule) in items
                        if isinstance(rule, clazz) and rule.check(getattr(self, name))]

            elements = entries(Element)
            attributes = entries(Attribute)
            nested = entries(Nested)
            manys = sum([[(m[0], v) for v in m[1]] for m in entries(Many)], [])

            return el(*([element for (_, element) in elements + nested + manys]),
                      **dict(attributes))

    return MyImpl
