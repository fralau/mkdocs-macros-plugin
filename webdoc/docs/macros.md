Writing modules
===============

Introduction
------------

**Modules** are libraries of macros, filters and variables, which
can be used by your MkDocs project.

Every module MUST contain a
[`define_env()` function](#the-define_env-function), 
which contains the declarations.

Location of the modules
-----------------------

### Local module

By default, the Python code must go into **one** `main.py` file in the main
website's project directory (generally beside the `mkdocs.yml` file).


**If no `main` module is available, this is ignored.**

If you wish, you can change the name of that module by adding a
`module_name` entry to the `mkdocs.yml` file (no need to add the `.py`
suffix):

``` {.yaml}
plugins:
  ...
  - macros:
        module_name: source_code
```

** If you specify a module name, it must be available, or this will 
raise an error.**

!!! Note
    If you wish, you can implement your module as a [package (subdirectory)](index.md/#implementing-the-module-as-a-package-module-subdirectory)
    instead of a single file. 


### Preinstalled modules (pluglets)

If you wish to reuse modules across several documentation projects,
you may want to pre-install them, turning them into [**pluglets**](pluglets.md).


The `define_env()` function
---------------------------

!!! Note
    New, as of version 0.3.0

As a first step, you need declare a hook function called `define_env`,
with one argument: `env` (object).
This object contains the environment (variables, filters, etc.) of the
templating tool (Jinja2). 

This is the information that will be used to generate the 
pure Markdown pages, which will then be translated into HTML 
(and displayed in a browser).

### Registration of variables, macros and filters
The example should be self-explanatory:

``` {.python}
"""
Basic example of a Mkdocs-macros module
"""

import math

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """

    # add to the dictionary of variables available to markdown pages:
    env.variables['baz'] = "John Doe"

    # NOTE: you may also treat env.variables as a namespace,
    #       with the dot notation:
    env.variables.baz = "John Doe"

    @env.macro
    def bar(x):
        return (2.3 * x) + 7

    # If you wish, you can  declare a macro with a different name:
    def f(x):
        return x * x
    env.macro(f, 'barbaz')

    # or to export some predefined function
    env.macro(math.floor) # will be exported as 'floor'


    # create a jinja2 filter
    @env.filter
    def reverse(x):
        "Reverse a string (and uppercase)"
        return x.upper()[::-1]
```
No special imports are required besides those you would need to write
your functions (the `env` object does all the 'magic').

!!! Tip
    You can export (as variables, macros or filters)
    a wide range of objects, and their attributes
    will remain accessible to the jinja2 template via the standard Python
    convention, e.g. `{{ foo.bar }}` (see [more
    information](https://jinja.palletsprojects.com/en/latest/templates#variables))

### Definition of variables/macros/filters

1. You register a **variable** for MkDocs-macros 
   by adding a key/value pair
   to the `env.variables` dictionary (or namespace).
   Variables are loaded with each page being rendered.
2. You register a **macro** by **decorating** a function
   with the expression `@env.macro` 
   (or by adding it to the `env.macros` dictionary).  
   Macros are loaded in the [global namespace](https://jinja.palletsprojects.com/en/2.11.x/api/#global-namespace)
of the Jinja2 environment.[^2].
3. You register a **filter** by **decorating** a function
   with the expression `@env.filter`
   (or by adding it to the `env.filters` dictionary).

This must be done *within* that `define_env()` function.
You may, however, place any imports or other declarations
outside of the function.


[^2]: _From version 0.5.10._ Before that, macros were inserted in `env.variables`.

### Priority of variables
!!! Warning
    In case of conflict, **variables** declared in the Python
    module will override
    those created by users in YAML files (`extra`). 
    This is a safety feature, to ensure that the maintainers of that file 
    will not accidentally break the setup defined
    by programmers in the module.

    Conversely, keep that fact in mind, 
    if users start complaining that an `extra` 
    value has a different value than the one which they expected!





## Content of the env object

### Description

The `env` object is used for _introspection_, i.e. is to get information
on the project or page. 



Here is a list of commonly needed attributes (constants)
or functions of that object:

Item|Type|Description
---|---|---
`variables`|_attribute_|The namespace that contains the variables and macros that will be available in markdown pages with `{{ ... }}` notation. This dictionary is initialized with the values contained in the `extra` section of the configuration file (and optionally, with external yaml files). This object is also accessible with the dot notation; e.g. `env.variables['foo']` is equivalent to `env.variables.foo`.
`macro`|_function_|A decorator function that you can use to declare a Python function as a Jinja2 callable ('macro' for MkDocs).
`filters`|_attribute_|A list list of jinja2 filters (default None)
`filter`|_function_|A decorator for declaring a Python function as a jinja2 custom filter
`project_dir`|_attribute_|The source directory of the MkDocs project (useful for finding or including other files)
`conf`|_attribute_|The content of the [config file](https://www.mkdocs.org/user-guide/custom-themes/#config) (`mkdocs.yaml`).
`config`|_attribute_|This can be a useful object; it contains the global context for MkDocs][^1].
`page`|_attribute_|The information on the page being served (such as the title, etc.). For more information on its content, see [MkDoc's description of the page object](https://www.mkdocs.org/user-guide/custom-themes/#page).


[^1]: `env.config` versus `env.conf`: it is unhappy that `env.config` represents MkDocs whole context, whereas `env.conf` represents only the `config` (YAML) file (a subset). This ambiguity was born from the fact that MkDoc itself used `config` to represent the context, as a property of the `BasePlugin` object.

!!! Note "Technical Note"
    `env` is essentially an instance of a subclass of the 
    MkDocs' [`BasePlugin` class](https://www.mkdocs.org/user-guide/plugins/#baseplugin), with some additional properties.
    Whatever you find in the `BasePlugin` class, you will find in the
    the `env` object.



### Accessing the whole config file (`mkdocs.yaml`)


Sometimes, you might need information from the [whole config file 
(`mkdocs.yaml`)](https://mkdocs.readthedocs.io/en/stable/user-guide/configuration/), e.g. `site_description`, `theme`, `copyright`, etc.

The property `conf` of the `env` object contains that information.

For example you could define such a function:

``` {.python}
@env.macro
def site_info():
    "Return general info on the website (name, description and theme)"
    info = (env.conf['site_name'], env.conf['site_description'],
            env.conf['theme'].name)
    return "%s/%s (theme: %s)" % info
```

!!! Warning "Beware the change of name"
    Beware that the what is usually called `config` is allied `env.conf`
    in the module. That is is because there is already `env.config`
    property as part of the `BasePlugin` class.

    Indeed, you will also find the same object under `env.variables.config`;
    in other words, it will be thus be accessible as `{{ config }}` 
    within the markdown pages.


!!!Tip
    In order obtain the documents directory (`docs`), you can
    use, within the Python module, the value: `env.conf['docs_dir']`.





### Manipulating the MkDocs configuration information

`env.config` is the object containing the **global context** for mkdocs,
i.e. the data structures that are being manipulated to create the final
HTML web site.


You would have to explore it
(using the [MkDocs documentation on the global context](https://www.mkdocs.org/user-guide/custom-themes/#global-context)),
but it contains the navigation (`env.conf['nav']`), as well
as all objects that could be manipulated.

!!! Note
    `env.config` is thus a superset of the `env.conf` object
    (which is `env.config['config']`).

!!! Caution
    This object is **not** accessible as a variable from the markdown pages.
    Exposing it might encourage black magic.


### Validating environment variables in Python code

By design, the call to `define_env()` is the last stage of the config
process, to create the jinja2 environment that will interpret the jinja2
directives inserted in the markdown code.

It means in particular, that you can test the variables dictionary to
validate its key/values, and to take appropriate action.

For example, to check that root branches are present in the variables
tree:

``` {.python}
MINIMAL_BRANCHES = ('foo', 'bar', 'baz')
def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    ...
    """

    # initial checks
    for branch in MINIMAL_BRANCHES:
        if branch not in env.variables:
            raise KeyError("Branch '%s' is not in environment variables! ")
```

!!! Tip
    This is a place where you could check that you code will not conflict
    with variables defined in the configuration files.

    You may also verify other aspects of the configuration file
    (`env.conf`). Note that the attributes of the `pluging->macro` branch
    are automatically checked by mkdocs (type and default value).


## List of hook functions within a module

`define_env()` is not the only possible hook within a module.

There are other functions available. Each is triggered by a [MkDocs event](https://www.mkdocs.org/user-guide/plugins/#events).

Function | Description | Typical Use | Triggered by MkDoc's event 
---  | ------ | ---- | ---
`define_env(env)` | Main function | [Create macros, filters, etc.](#the-define_env-function) | on_config 
`on_pre_page_macros(env)`| Executed just before the Jinja2 directives (markdown page) have been rendered | [Directly modify a markdown page](advanced.md/#adding-post-build-files-to-the-html-website) | on_page 
`on_post_page_macros(env)`| Executed just after the Jinja2 code (markdown page) have been rendered | [Directly modify a markdown page](advanced.md/#adding-post-build-files-to-the-html-website) | on_page
`on_post_build(env)` | Executed after the html pages have been produced | [Add files to the website](advanced.md/#adding-post-build-files-to-the-html-website) | on_post_build
`declare_variables(variables, macro)`| _Main function_ | [_Deprecated (< version 0.3.0)_](#the-declare_variables-function-deprecated) | *on_config*


## Implementing the module as a package (module subdirectory)

Instead of implementing the Python module as a file (typically `main.py`), 
you can create a *package* (i.e. a `main` subdirectory). 

The Python rules for defining a package apply: particularly
the dot (`.`) prefix for relative imports inside the package.

The `define_env()` function should be accessible
through the `__init__.py` file.

A typical directory file could look like this:

```
main
├── __init__.py
├── util.py
├── ...
└── ...
```

The `__init__.py` file could look like this:

```python
from .util import foo, bar

def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """

    @env.macro
    def make_foo():
        .......
        return foo(s)

    @env.macro
    def get_bar(s):
        s = bar(s, ...)
        return s

    ...

```



## A caution about security


!!! Warning

    It is true that you are generating static pages.

    Nevertheless, think about potential side effects of macros
    (in case of error or
    abuse) or about the risks of exposing sensitive information,
    **if the writers of markdown pages are different persons than
    the maintainers of the webserver**.


Depending on your use case, you may want to give **access to the shell**
(e.g. for a development team). Or else, may you **want to "sandbox" your
web pages** (for business applications). 





## What you can and can't do with `define_env()`

The fact is that you **cannot** actually access page information
in the `define_env()` function, since
it operates at the configuration stage of the page building process 
(during the [`on_config()` event of MkDocs](https://www.mkdocs.org/user-guide/plugins/#on_config)). 
At that point, **you don't have access to specific pages**


!!! Warning "Vital Note on mkdocs-macros" 
    Of course, you **can** declare **macros**, which **appear** to act on pages. 
    But realize that these are only **declarations** and that their
    execution is **deferred**. 
    The macros will actually be run ** later** 
    (by MkDocs' [`on_page_markdown()` event](https://www.mkdocs.org/user-guide/plugins/#on_page_markdown)),
    just before the markdown is rendered. The framework is so organized
    that, in macros, you are actually "talking" about objects that don't exist yet.

    So you **cannot** influence the rendering process other than by
    adding macros, variables and filters to `mkdocs_macros`.





!!! Danger "Do not modify system entities in `env.variables`"

    Also, the system information in `env.variables`
    is for **reading** purposes.
    You could modify it in your Python code, of course (at your own peril).
    But **by design**, it may have no effect on the mechanics
    of `mkdocs` (these are shallow copies). 

    Whatever you do in that way, is likely to be branded **black magic**.

