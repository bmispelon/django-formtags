import sys


def split_fields(fields):
    """Normalize the given argument to return a list of field names.
    The supported formats are:
        * A list of str
        * A string of comma-separated fields
        * A string of whitespace-separated fields
    """
    if isinstance(fields, basestring):
        return fields.replace(',', ' ').split()
    return list(fields)


def python_2_unicode_compatible(klass):
    """Backported from django 1.5."""
    if sys.version_info[0] != 3:
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass
