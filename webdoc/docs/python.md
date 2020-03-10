Defining variables, macros, and filters in Python code
======================================================

Location of the module
----------------------

By default, the Python code must go into a `main.py` file in the main
website's directory (beside the `mkdocs.yml` file).

> Instead of a module file, it also be a *package* (i.e. a `main`
> subdirectory), as long as the `declare_env` function is accessible
> through the **init**.py file.

If you wish, you can change the name of that module by adding a
`module_name` entry to the `mkdocs.yml` file (no need to add the `.py`
suffix):

``` {.yaml}
module_name: source_code
```

The `define_env()` function
---------------------------

> New as of version 0.3.0

As a first step, you need declare a hook function called `define_env`,
with one argument: `env` (object).

This object contains the following attributes:

-   `variables`: the dictionary that contains the variables and macros
    It is initialized with the values contained in the `extra` section
    of the configuration file (and optionally, with external yaml
    files). This object is also accessible with the dot notation;
    e.g. `env.variables['foo']` is equivalent to `env.variables.foo`.
-   `macro`: a decorator function that you can use to declare a Python
    function as a Jinja2 callable ('macro' for MkDocs).
-   `filters`: a list list of jinja2 filters (default None)
-   `filter`: a decorator for declaring a Python function as a jinja2
    custom filter.

> In case of conflict, jinja2 variables declared in Python will override
> those created by users in yaml files. This is a safety feature, to
> ensure that contributors will not accidentally break the setup defined
> by programmers.

The example should be self-explanatory:

``` {.python}
def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """

    env.variables['baz'] = "John Doe"
    # NOTE: you may also write:
    #       env.variables.baz = "John Doe"

    @env.macro
    def bar(x):
        return (2.3 * x) + 7

    # If you wish, you can  declare a macro with a different name:
    def f(x):
        return x * x

    env.macro(f, 'barbaz')

    # or to export some predefined function
    import math
    env.macro(math.floor) # will be exported as 'floor'


    # create a jinja2 filter
    @env.filter
    def reverse(x):
        "Reverse a string (and uppercase)"
        return x.upper()[::-1]
```

> For the pre 0.3.0 version (`define_variables()`), use `variables`
> directly, without prefixing with `env`.

Your **registration** of variables or macros for MkDocs should be done
*within* that hook function.

No special imports are required (the `env` object does all the 'magic').
On the other hand, nothing prevents you from making imports or
declarations **outside** of the `declare_env` function.

> **Note:** You can export a wide range of objects, and their attributes
> will remain accessible to the jinja2 template via the standard Python
> convention, e.g. `{{ foo.bar }}`. Jinja2 will even (see [more
> information](http://jinja.pocoo.org/docs/2.10/templates/#variables))

The `declare_variables()` function (old)
----------------------------------------

> This is the old paradigm, before 0.3.0 (still supported). Prefer the
> `define_env` function.

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

Example: Creating a Button Macro
--------------------------------

In the python module, add to the `define_env()` function:

```python
def define_env(env):

    # import the predefined macro
    fix_url = env.variables.fix_url # make relative urls point to root

    @env.macro
    def button(label, url):
        "Add a button"
        url = fix_url(url)
        HTML = """<a class='button' href="%s">%s</a>"""
        return HTML % (url, label)
```

In your markdown page:


    {{ button('Try this', 'http:your.website.com/page') }}

> The `fix_url` function is optional. Its purpose is to capture relative urls
and make them point to the root of the website,
rather than to the `docs` directory.
Supposing you had an `attachment` directory just under the root,
then a pdf could be accessed e.g. with `attachment/foo.pdf`, rather
than `../attachment/foo.pdf` (error prone).

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

> This is a place where you could check that you code will not conflict
> with variables defined in the configuration files.

> You may also verify other aspects of the configuration file
> (`env.conf`). Note that the attributes of the `pluging->macro` branch
> are automatically checked by mkdocs (type and default value).


