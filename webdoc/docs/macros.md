Defining Macros and Filters (as well as Variables) 
======================================================

Introduction
------------

Modules are libraries of macros, filters and variables, which
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


!!! Tip
    Instead of a module file, could also be a *package* (i.e. a `main`
    subdirectory), as long as the `define_env()` function is accessible
    through the `__init__.py` file.

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

### Adding pre-installed modules

!!! Note
    New, as of version 0.4.20.

You may use pre-installed modules (which would appear with `pip list`).

In that case, you must use a different argument (`modules`).  
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

!!! Tip

    ** It means that you can develop modules for mkdocs-macros-plugin
    and publish them on [github](https://github.com/) and 
    [pypi](https://pypi.org/)**.

    The names of modules are not constrained. 
    
    As a **naming convention**, we recommend names starting with
    `mkdocs_macros_`.

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
    You can export a wide range of objects, and their attributes
    will remain accessible to the jinja2 template via the standard Python
    convention, e.g. `{{ foo.bar }}` (see [more
    information](http://jinja.pocoo.org/docs/2.10/templates/#variables))


### Definition of variables/macros/filters

!!! Important 

    1. You register a **variable** for MkDocs-macros 
       by adding a key/value pair
       to the `env.variables` dictionary (or namespace).
    2. You register a **macro** by **decorating** a function
       with the expression `@env.macro` 
       (or by adding it to the `env.variables` dictionary).
    3. You register a **filter** by **decorating** a function
       with the expression `@env.filter`
       (or by adding it to the `env.filters` dictionary).

    This must be done *within* that `define_env()` function.
    You may, however, place any imports or other declarations
    outside of the function.

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

The `env` object is used for _introspection_, i.e. is to get information
on the project or page.

Here is a list of commonly needed attributes (constants)
or functions of that object:

Item|Type|Description
---|---|---
`variables`|_attribute_|The namespace that contains the variables and macros that will be available in mardkown pages with `{{ ... }}` notation. This dictionary is initialized with the values contained in the `extra` section of the configuration file (and optionally, with external yaml files). This object is also accessible with the dot notation; e.g. `env.variables['foo']` is equivalent to `env.variables.foo`.
`macro`|_function_|A decorator function that you can use to declare a Python function as a Jinja2 callable ('macro' for MkDocs).
`filters`|_attribute_|A list list of jinja2 filters (default None)
`filter`|_function_|A decorator for declaring a Python function as a jinja2 custom filter
`project_dir`|_attribute_|The source directory of the MkDocs project (useful for finding or including other files)
`conf`|_attribute_|This is a very useful object; it contains the [configuration information for mkdocs](https://mkdocs.readthedocs.io/en/stable/user-guide/configuration).


!!!Tip
    In order obtain the documents directory (`docs`), you can
    use, within the Python module, the value: `env.conf['docs_dir']`.


Accessing the whole config file
-------------------------------

Sometimes, you might need information from the whole config file,
e.g. `site_description`, `theme`, `copyright`, etc.

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



Validating environment variables in Python code
-----------------------------------------------

By design, the call to define\_env() is the last stage of the build
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


A caution about security
------------------------

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



The `declare_variables()` function (DEPRECATED)
----------------------------------------

!!! Warning
    `declare_variables()` is the old paradigm, before 0.3.0
    and it is DEPRECATED. 
    Support for this call will be discontinued in a future version.
    
    Use instead the `define_env()` function.

As a first step, you need declare a hook function called
`declare_variables`, with two arguments:

-   `variables`: the dictionary that contains the variables. It is
    initialized with the values contained in the `extra` section of the
    `mkdocs.yml` file.
-   `macro`: a decorator function that you can use to declare a Python
    function as a Jinja2 callable ('macro' for MkDocs).

The example should be self-explanatory:

``` {.python}
def declare_variables(variables, macro):
    """
    This is the hook for the functions

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """

    variables['baz'] = "John Doe"

    @macro
    def bar(x):
        return (2.3 * x) + 7



    # If you wish, you can  declare a macro with a different name:
    def f(x):
        return x * x

    macro(f, 'barbaz')

    # or to export some predefined function
    import math
    macro(math.floor) # will be exported as 'floor'
```

Your **registration** of variables or macros for MkDocs should be done
inside that hook function. On the other hand, nothing prevents you from
making imports or declarations **outside** of this function.

> **Note:** You can export a wide range of objects, and their attributes
> remain accessible (see [more
> information](http://jinja.pocoo.org/docs/2.10/templates/#variables))

### Accessing variables

In case you need to access some variables defined in the config file
(under `extra`), use the `variables` dictionary:

Suppose you have:

``` {.yaml}
extra:
    price: 12.50
```

You could write a macro:

``` {.python}
@macro
def compare_price(my_price):
    "Compare the price to the price in config file"
    if my_price > env.variables['price']:
        return("Price is higher than standard")
    else:
        return("Price is lower than standard")
```

For your convenience, you may also use the dot notation:
``` {.python}
@macro
def compare_price(my_price):
    "Compare the price to the price in config file"
    if my_price > env.variables.price:
        return("Price is higher than standard")
    else:
        return("Price is lower than standard")
```

### Accessing macros
> Note that since a macro is also a variable (function), you can also "import"
it in a module. 
For example, `fix_url` is a predefined macro that fixes relative
urls (when applicable) so that they point to the root of the site:


```
fix_url = env.variables.fix_url
my_url = fix_url(url)
```