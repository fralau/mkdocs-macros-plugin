#!/usr/bin/env python3
# ------------------------------------------
# Utilities
# ------------------------------------------

from termcolor import colored
from copy import deepcopy

import os, sys, importlib.util

def import_module(project_dir, module_name):
    "Import a module from a pathname"
    # get the full path
    if not os.path.isdir(project_dir):
        raise FileNotFoundError("Project dir does not exist: %s" % project_dir) 
    # there are 2 possibilities: dir or file
    pathname_dir = os.path.join(project_dir, module_name)
    pathname_file = pathname_dir + '.py'
    if os.path.isfile(pathname_file):
        spec = importlib.util.spec_from_file_location(module_name, 
                                                pathname_file)
        module = importlib.util.module_from_spec(spec)
        # execute the module
        spec.loader.exec_module(module)
        return module
    elif os.path.isdir(pathname_dir):
        # directory
        sys.path.insert(0, project_dir)
        return importlib.import_module(module_name)
    else:
        return None




def trace(*args, **kwargs):
    "General purpose print function, with first item emphasized (color)"
    COLOR = 'green'
    first = args[0]
    rest = args[1:]
    emphasized = colored("[macros] " + first, COLOR)
    print(emphasized, *rest, **kwargs)


def update(d1, d2):
    """
    Update object d1, with object d2, recursively
    It has a simple behaviour:
    - if these are dictionaries, attempt to merge keys
      (recursively).
    - otherwise simply makes a deep copy.
    """
    BASIC_TYPES = (int, float, str, bool, complex)
    if isinstance(d1, dict) and isinstance(d2, dict):
        for key, value in d2.items():
            # print(key, value)
            if key in d1:
                # key exists
                if isinstance(d1[key], BASIC_TYPES):
                    d1[key] = value
                else:
                    update(d1[key], value)

            else:
                d1[key] = deepcopy(value)
    else:
        # if it is any kind of object
        d1 = deepcopy(d2)

class SuperDict(dict):
    """
    A dictionary accessible with the dot notation

    a['foo'] <=> a.foo

    except for standard methods
    """

    def __getattr__(self, name):
        "Allow dot notation on reading"
        try:
            return self[name]
        except KeyError:
            raise AttributeError("Cannot find attribute '%s" % name)

    def __setattr__(self, name, value):
        "Allow dot notation on writing"
        self[name] = value

if __name__ == '__main__':
    # test merging of dictionaries
    a = {'foo': 4, 'bar': 5}
    b = {'foo': 5, 'baz': 6}
    update(a, b)
    print(a)
    assert a['foo'] == 5
    assert a['baz'] == 6

    a = {'foo': 4, 'bar': 5}
    b = {'foo': 5, 'baz': ['hello', 'world']}
    update(a, b)
    print(a)
    assert a['baz'] == ['hello', 'world']


    a = {'foo': 4, 'bar': {'first': 1, 'second': 2}}
    b = {'foo': 5, 'bar': {'first': 2, 'third': 3}}
    update(a, b)
    print(a)
    assert a['bar'] == {'first': 2, 'second': 2, 'third': 3}
    NEW =  {'hello': 5}
    c = {'bar': {'third': NEW}}
    update(a, c)
    print(a)
    assert a['bar']['third'] == NEW


    NEW = {'first': 2, 'third': 3}
    a = {'foo': 4}
    b = {'bar': NEW}
    update(a, b)
    print(a)
    assert a['bar'] == NEW
