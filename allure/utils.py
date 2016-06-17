"""
@author: qatoe1991
"""
import time
import hashlib

from six import text_type, binary_type


def uid(name):
    """
    Generates fancy UID uniquely for ``name`` by the means of hash function
    """
    return hashlib.sha256(name).hexdigest()


def sec2ms(sec):
    return int(round(sec * 1000.0))

def now():
    """
    Return current time in the allure-way representation. No further conversion required.
    """
    return sec2ms(time.time())

def unicodify(something):
    if isinstance(something, text_type):
        return something
    elif isinstance(something, binary_type):
        return something.decode('utf-8', 'replace')
    else:
        try:
            return text_type(something)  # @UndefinedVariable
        except (UnicodeEncodeError, UnicodeDecodeError):
            return u'<nonpresentable %s>' % type(something)  # @UndefinedVariable

