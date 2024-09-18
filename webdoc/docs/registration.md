# Registering macros/variables/filters in MkDocs-Macros

_As of 1.1.2 (Experimental)_ 

!!! Info "Important note"
    This is technical documentation for writers of MkDocs Plugins. 


## Introduction

This is description of how other MkDocs [plugins](https://www.mkdocs.org/dev-guide/plugins/) (see [a list]([existing plugins](https://github.com/mkdocs/catalog)))
can register their macros and variables with MkDocs-Macros.

There can exist two motivations:

1. Provide additional functionality to the plugin, by providing
   macros, variables and filters, accessible through MkDocs-Macros.
2. Resolve syntax incompatibility issues, if the plugin uses a syntax
  similar to Jinja2 (typically expressions between `{{` and `}}`). 

## Syntax Incompatibility between plugins

### Description of the issue

MkDocs-Macros was written so that it does not interact with other plugins;
it interacts only with MkDocs' events.

However, there might be a number of reasons why incompatibilities
could occur.

!!! Note
    The most common one derives from the fact that 
    MkDocs-Macros uses the Jinja2 syntax
    (typically expressions between `{{` and `}}`). 
    
    For example a plugin might define `foo(x)` as a function,
    which might need a call as `{{ foo(x) }}` in a Markdown page.

    The plugin might fail
    (if declared before MkDocs-Macros in the [config file's list of plugins](https://www.mkdocs.org/user-guide/configuration/#plugins),
    because it now sees many calls with the same syntax
    that it can't interpret),
    or might make MkDocs-Macros fail (if declared later), since
    it is very strict and won't accept a non existent macro.

    

!!! Tip
    Workarounds exist to change the way MkDocs-Macros handles syntax.

    They are described in the page on
    [controlling macros rendering](rendering.md).

    They can be useful if MkDocs-Macros is used as a secondary plugin.
    They might be inadequate if MkDocs-Macros is considered "core".


### Solutions without plugin

- A [macros module](macros.md) is the simplest a fastest solution,
  for solving a specific need that requires a simple function.
- For a solution across several documentation projects,
 [pluglets](pluglets.md) were introduced so that a developer
  could quickly develop a solution from scratch, that does not
  involve a plugin. Pluglets are macros module easily distributable
  through Pypi.


!!! Warning "What about rewriting existing a Plugin as an MkDocs-Macros pluglet?" 

    This could be a solution.
    
    **However, it might not be convenient or desirable for the author of a
    plugin to rewrite it as pluglet**.

    **A solution had to be found for that case.**
   

## How to adapt a plugin to register macros, filters and variables


### Theory

Existing MkDocs plugins might find advantage in using MkDocs-Macros's
framework as a support for their own "macros", if they use the same syntax.

This is done extremely easily, with the use of three methods
exported by the `MacrosPlugin` class (itself based on `BasePlugin`).

- `register_macros()`, which takes a dictionary of Python functions
  (Callables) as argument. Those functions must return an `str` result,
  or some object that can be converted to that type.
- `register_variables()`, which takes a dictionary of Python variables
  as argument.
- `register_filters()`, which takes a dictionary of Jinja2 filters
  as an argument (see [definition in the official documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/#filters)).
  For our purposes,filters are Python callables where the first argument becomes
  implicit (it is considered as the input value before the `|` symbol).


!!! Tip "Independence from the declaration order"
    These macros are designed to work independently from the order
    in which MkDocs plugins are declared.

    - If the plugin is declared **before** Mkdocs-Macros, then the
      macros/variables/filters will be "kept aside" and registered last,
      at the [`on_config`](https://www.mkdocs.org/dev-guide/plugins/#on_config) event. 
    - If the plugin is declared **after** Mkdocs-Macros, then
      the items will be registered immediately.

    In both cases, a conflict with a pre-existing macro/variable/filter 
    name will raise a `KeyError` exception.


### Practice

You want to register those macros/filters/variables
at the `on_config()` method of your plugin, providing
the MkDocs-Macros plugin is declared. 

Its argument `config` allows you to access the Mkdocs-Macros plugin (`macros`),
and its three registration methods.

```python

def foo(x:int, y:str):
  "First macro"
  return f"{x} and {y}"

def bar(x:int, y:int):
  "Second macro"
  return x + y

def scramble(s:str, length:int=None):
    """
    Dummy filter to reverse the string and swap the case of each character. 

    Usage in Markdown page:

    {{ "Hello world" | scramble }}    -> DLROw OLLEh
    {{ "Hello world" | scramble(6) }} -> DLROw
    """
    r = s[::-1].swapcase()
    if length is not None:
      r = r[:length]
    return r


MY_FUNCTIONS = {"foo": foo, "bar": bar}
MY_VARIABLES = {"x1": 5, "x2": 'hello world'}
MY_FILTERS   = {"scramble": scramble}



class MyPlugin(BasePlugin):
  "Your existing MkDocs plugin"

  ...

  def on_config(self, config, **kwargs):

    # get MkdocsMacros plugin, but only if present
    macros_plugin = config.plugins.get("macros")
    if macros_plugin:
      macros_plugin.register_macros(MY_FUNCTIONS)
      macros_plugin.register_variables(MY_VARIABLES)
      macros_plugin.register_filters(MY_VARIABLES)
```



