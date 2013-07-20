import sys

def format_exception(etype, value, tb, limit=None):
    return sys._get_traceback_list(value, tb, limit=limit)

def print_exc():
    print sys._get_traceback_list(value, tb, None)

def format_exc(limit=None):
    """Like print_exc() but return a string."""
    try:
        etype, value, tb = sys.exc_info()
        return ''.join(format_exception(etype, value, tb, limit))
    finally:
        etype = value = tb = None


