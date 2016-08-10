from rules import xmlfied, Attribute, Element, WrappedMany, Nested, Many, \
    Ignored
from constant import ALLURE_NAMESPACE

class Attach(xmlfied('attachment',
                     source=Attribute(),
                     title=Attribute(),
                     type=Attribute())):
    """
    Attached file
    """

class Failure(xmlfied('failure',
                      message=Element(),
                      trace=Element('stack-trace'))):
    """
    trace
    """

class IterAttachmentsMixin(object):

    def iter_attachments(self):
        for a in self.attachments:
            yield a

        for s in self.steps:
            for a in s.iter_attachments():
                yield a


class TestCase(IterAttachmentsMixin,
               xmlfied('test-case',
                       id=Ignored(),  # internal field, see AllureTestListener
                       name=Element(),
                       title=Element().if_(lambda x: x),
                       description=Element().if_(lambda x: x),
                       failure=Nested().if_(lambda x: x),
                       steps=WrappedMany(Nested()),
                       attachments=WrappedMany(Nested()),
                       labels=WrappedMany(Nested()),
                       parameters=WrappedMany(Nested()),
                       status=Attribute(),
                       severity=Attribute(),
                       start=Attribute(),
                       stop=Attribute())):
    pass


class TestSuite(xmlfied('test-suite',
                        namespace=ALLURE_NAMESPACE,
                        name=Element(),
                        title=Element().if_(lambda x: x),
                        description=Element().if_(lambda x: x),
                        tests=WrappedMany(Nested(), name='test-cases'),
                        labels=WrappedMany(Nested()),
                        start=Attribute(),
                        stop=Attribute())):
    pass


class TestKeyword(IterAttachmentsMixin,
                  xmlfied('step',
                       name=Element(),
                       title=Element().if_(lambda x: x),
                       attachments=WrappedMany(Nested()),
                       steps=WrappedMany(Nested()),
                       start=Attribute(),
                       status=Attribute())):
    pass


class TestLabel(xmlfied('label',
                       name=Attribute(),
                       value=Attribute())):
    pass


class EnvParameter(xmlfied('parameter',
                   name=Element(),
                   key=Element(),
                   value=Element())):
    pass
