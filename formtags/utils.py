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
