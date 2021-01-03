# Writing pluglets

!!! Note
    New, as of version 0.4.20.

## Introduction

### Definition

A **pluglet** is a preinstalled module for mkdocs-macros, which is
installed thanks to Pythons [standard packaging process](https://packaging.python.org/tutorials/packaging-projects/).

The only
thing needed (as a bare minimum), is to implement a single function,
`define_env()`:

```python

def define_env(env):
    ....

```

!!! Question "What makes a pluglet different from a plain module?"
    The only difference between a **pluglet** and an ordinary
    mkdocs-macros [**module**](macros) (typically `main.py` or `main` directory),
    is that the pluglet is preinstalled. In this way, you can
    benefit from pluglets written by others, and you could share the
    pluglets that you wrote.

    A pluglet can do two things that any mkdocs-macro module can do:

    1. Define macros.
    2. Perform changes on the architecture of the website.


!!! Question "What makes a pluglet different from a plugin?"
    A **pluglet** is distinct from an **[MkDocs plugin](https://www.mkdocs.org/user-guide/plugins/)**. A **pluglet** is a more lightweight tool that sits
    over the mkdocs-macros plugin and uses the framework provided by it.

    There is no need to implement a subclass of the `BasePlugin` class,
    only to declare a `define_env(env)` function.
   
!!! Question "Could a pluglet do everything a plugin can do?"

    The answer is, *quite a lot, but not everything*. 
    MkDocs plugins are able to rely on [a wide range of 
    events](https://www.mkdocs.org/user-guide/plugins/#events),
    which are hooks for acting on the website at various stages of the config/build process.

    A mkdocs-macros pluglet operates mostly on the [on_config](https://www.mkdocs.org/user-guide/plugins/#on_config) event of MkDocs thanks to
    `define_env(env)`hook; but [its use can be extended thanks to other hooks](macros/#list-of-hook-functions-within-a-module).



## Using existing pluglets

### Declaring a pluglet for an MkDocs project

For your specific documentation project, you may call already
installed pluglets (which would appear with `pip list`):

```bash
pip list | grep mkdocs-macros
```

Use the `modules` argument.  
It is a list, so that you can declare one or more:

e.g. :

``` {.yaml}
plugins:
  ...
  - macros:
      modules: [mkdocs_macros_test]
```

or: 

``` {.yaml}
plugins:
  ...
  - macros:
      modules: [mkdocs_macros_foo, mkdocs_macros_bar]
```

** Every module specified must be available, or this will 
raise an error.**

When you type the `mkdocs serve` or `mkdocs build` command, everything
should fall into place.

## Implementing a new pluglet

### General Principles

**You can develop pluglets for mkdocs-macros-plugin
and publish them on [github](https://github.com/) and 
[pypi](https://pypi.org/)**.

### How to name a pluglet

The names for pluglets are not constrained. As a **naming convention**, we
strongly recommend:

- a package name starting with `mkdocs-macros-`
- an import name starting `mkdocs_macros_`, i.e. replacing the hyphen (`-`) symbol by underscore (`_`).



### Typical structure of a pluglet

!!! Note
    You will find a simple example with the [`mkdocs-test` pluglet, available on gihub](https://github.com/fralau/mkdocs-macros-test).


The `setup.py` file will typically have this form:

```python

from setuptools import setup

setup(
    name='mkdocs-macros-foo',
    version='0.0.1',
    description="Foo library for macros plugin",
    packages=['mkdocs_macros_foo'],
    license='<YOUR CHOICE>',
    author='Joe Bloe'
)

```

The structure will be typically like so:

    ├── LICENSE.md
    ├── README.md
    ├── mkdocs_macros_test.py
    └── setup.py

or like so (if it is more complex):


    ├── LICENSE.md
    ├── README.md
    ├── mkdocs_macros_test
    │   └── __init__.py
    |   └── util.py
    └── setup.py

!!! Note
    The subdirectory containing
    the code will have to be called `mkdocs_macros_foo` (underscores).



### How to write the code
For the code itself, proceed as for a [usual module](../macros):

```python
"""
Code of the pluglet
"""

def test_fn(x:float):
    "Test function"
    return x * 4 / 3

def say_hello(s:str):
    "Test procedure"
    return "<i>Hello %s</i>" % s

def define_env(env):
    "Declare environment for jinja2 templates for markdown"

    for fn in [test_fn, say_hello]:
        env.macro(fn)


    # you could, of course, also define a macro here:
    @env.macro
    def test_fn2(s:str):
        return "I am displaying this: %s" % s

```



