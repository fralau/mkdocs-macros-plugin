Troubleshooting
===============

Before anything else
--------------------

!!! Important
    Make sure you you have the **last version** of mkdocs-macros.
    Perhaps the issue is already fixed?

    Also, check that your version of mkdocs is sufficiently up-to-date.

Error Information in case of module error
-----------------------------------------

By default a rendering error in a macro will not stop the server, 
but display the error in the browser's page (as you would expect,
e.g. with php). 
The terminal's running log also displays errors when they occur.




Is it possible to make the building process fail in case of page error?
-----------------------------------------------------------
Yes. In a context of CD/CI (Continuous Development/Continuous Integration)
the generation of the mkdocs site can be part of a larger script.

In that case, the expected behavior is _not_ to display the error message
in the respective webpage (default behavior), 
but to terminate the build process with an error code.
That is the best way to advertise that something went wrong.

It should then be possible to consult the log (console output)
and track down the offending markdown file and line number.


There are two ways to achieve that:

1. Instruct Mkdocs-Macros to fail in case of error
2. Instruct Mkdocs to fail in case of any warning (strict mode)




### Instructing Mkdocs-Macros to fail in case of error

A simple way to make the build fail in case of a problem with variable/macro rendering,
is to set the `on_error_fail` parameter to `true`
in the config file:

```yaml
plugins:
  - search
  - macros:
      # toggle to true if you are in CD/CI environment
      on_error_fail: true
```

In that case, an error in a macro will terminate 
the MkDocs build or serve process with an **error 100**.

!!! Tip "Make the behavior depend on an environment variable"

    As of version 1.2, [mkdocs incorporates a yaml extension](https://www.mkdocs.org/user-guide/configuration/#environment-variables)
    that allows the value of a configuration option to be set 
    to the value of an environment variable.

You could therefore write:

```yaml
plugins:
    - search
    - macros:
        on_error_fail: !ENV [MACRO_ERROR_FAIL, false]
```

Meaning that the parameter "`on_error_fail` should be set to the value of 
`MACRO_ERROR_FAIL`; or if the environment variable is absent to `false`.


!!! Warning "Catching undefined variables"
    By default, [an undefined variable](#what-happens-if-a-variable-is-undefined),
    all by itself, does not cause an error, but leaves the jinja2
    statement as-is (not rendered).

    If you wish to raise an error also in that case, you may want to add:
        
            on_undefined: strict
        
### Instructing Mkdocs to fail in case of any warning

_From version 1.1.2_

This approach can be useful for large projects with automated deployement.

A WARNING message is generated when an error occurs in the rendering
of variables or macros. 

If you apply the `--strict` or `-s` switch (strict mode) the 
make the serve or build process will fail when a warning is generated:

```sh
mkdocs serve --strict
```

In that case _any_ warning from any plugin (not only Mkdocs-Macros)
will make the build fail, which is a default approach to warnings
in plugins.

!!! Tip
    If you do not want to use the strict mode because other plugins are
    generating warnings that you wish to ignore, then the first approach
    (`on_error_fail:true` might be better).

What happens if a variable is undefined?
--------------------------------------

_New on 0.6.4._

The default behavior in case of undefined variable 
is called **keep** (DebugUndefined):

1. Unknown variables are rendered as is (`{{ foobar }}` will be printed as such if 
  `foobar` is undefined).
1. Any other cases (notably unknown attribute or function call) will cause the page
   to **fail** (be rendered with an error message within the page plus the traceback).  

!!! Tip Motivations for default behavior
    There were two reasons for adopting this behavior:
    
    1. This "debug" mode reduces cognitive overhead in case of misspelled variable.
       Anyone will be able to detect this error (it is better having an odd jinja2 statement 
       in the page than having a "blank" that is likely to go unnoticed) 
    2. Other plugins than mkdocs-macros make use of jinja2 variables 
       (as specified in the config file).
       In this way, mkdocs-macros will not "eat up" those variables; 
       it will give other plugins a better chance to work.

You may alter this behavior with the `on_undefined` parameter in mkdocs_macros 
section of the config file (`mkdocs.yaml`):

| Value  | Definition        | Undefined Type                   |
| ------ | -------------------------------- | ------------------------- |
| keep   | (Default) Unknown variables are rendered as-is; all other cases will cause the page to fail. | DebugUndefined                             |
| silent | Unknown variables are rendered as blank; all other cases will cause the page to fail.        | Undefined                                  |
| strict | Anything incorrect will cause the page to fail (closest behavior to Python).                 | StrictUndefined                            |
| lax    | Like silent (blank); will be more tolerant, typically in case of unknown attribute.          | LaxUndefined (_specific to mkdocs-macros_) |


For example:

```yaml
plugins:
  - search
  - macros:
      on_undefined: strict
```

!!! Warning
    A call to an unknown macro (callable) will always cause the page to fail.

The Undefined Type is the Jinja2 class used to implement that behavior (see [definition in official documentation](https://jinja.palletsprojects.com/en/3.0.x/api/#undefined-types)).



`macros_info()` as the go-to tool
---------------------------------

Adding following line in a page:

    {{ macros_info() }}

and restarting the server in the terminal with `mkdocs serve` will
usually give you a wealth of information within the browser:

-   If the information page appears (as e.g. phpinfo() for php), then
    you know that the plugin must be working.
-   If the page displays and an error message appears, then there may be
    a problem either with the page or with the plugin's installation.
-   If the page does not display at all, then the mkdocs server might
    not be running or there can be a problem running it.



How can I get detailed debug information on an object?
------------------------------------------------------

For example, if you want to have more information on the `config`
object:

    {{ context('config') | pretty }}

(the `pretty` filter displays the result in a nice table form)

You can use this pattern for pretty much any object, even those you
declared in a module.

When used on its own, `context()` gives the general list of variables in
the plugin's environment:

    {{ context() | pretty }}


Help! mkdocs-macros is breaking down or eating pieces of my documentation!
------------------------------------------------

![dog eating ice-cream, credit: https://unsplash.com/photos/OYUzC-h1glg](dog-eating.jpg)

1. In principle, anything that looks like an unknown variable (e.g. `{{ foo }}`) will be preserved.
But in some cases there could be an error page or  **an empty string where you expected one**. [See how you can change the rendering behavior](#what-happens-if-a-variable-is-undefined).

2. Another likely cause of problems is that mkdocs-macros is believing that statements
of the form `\{\{ .... }}` or `{% ... %}` 
in your pages, 
which you want to appear in the HTML output or be processed by another plugin,
are intended for it. To solve that problem, see the page 
[dedicated to that issue](rendering.md).








Traces on the console
-------

_From version 0.5.0_

### Using the console's traces for troubleshooting
To make troubleshooting while using `mkdocs serve` you 
do not need to rely only on what you see in the browser.
You should exploit the trace on the console,
which MkDocs-macros produces on the fly. 

The statements specific to mkdocs-macros appear with a
**[macros]** prefix e.g.:

```
INFO    -  [macros] - Macros arguments: {'module_name': 'main', 'modules': ['mkdocs_macros_test'], 'include_dir': 'include', 'include_yaml': [], 'j2_block_start_string': '', 'j2_block_end_string': '', 'j2_variable_start_string': '', 'j2_variable_end_string': '', 'verbose': False}
```

!!! Tip
    Reading the console's trace may help you follow up what is happening.

### Hiding mkdocs-macros' trace

You can **suppress** the trace completely (together with the rest of the
INFO trace from mkdocs), with the standard `--quiet` option :

```sh
mkdocs serve --quiet
```

or with the `-q` option.

### Debug mode for mkdocs-macros

You can **increase** the trace completely by showing the debug information
(together with the rest of the DEBUG from mkdocs), with the standard
`--verbose` option:

```sh
mkdocs serve --verbose
```

or with the `-v` option.

### Verbose (debug) statements in macros 
You could use `print()` statements to log what is happening in your macros, 
and it is going to be printed on the console. **But this can be messy**.

It is much better, within the `def define_env():` declaration, 
to use the `chatter()`
function. It will print statements **only** if the macros plugin's 
debug mode is set to true.

```yaml
plugins:
  - ...
  - macros:
      verbose: true 
```

!!! Tip
    With the `chatter()` function, you can leave those debug traces
    in the code of your macros,
    and visualize them only when you want to see them.

You need to first declare the `chatter()` function with
the `env.start_chatting()` method. 
This initialization is necessary, so that you can give a nickname for 
your module, which will allow you to recognize the traces:

```python
def define_env(env):
    """
    This is the hook for the functions (new form)
    """
    # activate trace
    chatter = env.start_chatting("Simple module")

    ...
    chatter("This is a dull statement.")
```

This will print:
```
INFO    - [macros - Simple module] - This is a dull statement.
```



!!! Warning "Important"
    
    The **verbose** mode for mkdocs-macros is **distinct** from the general debug mode of mkdocs (which is activated with the `--verbose` option).
    
    To activate the debug mode for mkdocs-macros, you need to set the `verbose`
    option to true for mkdocs-macros, in the config file (`mkdocs.yml`).

    **Toggling between `true` and `false` in the `verbose`
    option will be immediately be reflected on the console.**


!!! Note "Forcibly suppressing the console output of macros"

    If the `verbose` argument is set to true for the plugin, the messages will appear as **INFO** on the console's log.

    It means that if you suppress the trace output at the level of 
    `mkdocs serve` (using the `--quiet` option),
    **this will also suppress the trace for your macros**.

    **This is intentional, so that the behavior of MkDocs's logging
    remains entirely predictable, even for people who
    never heard of mkdocs-macros (principle of least astonishment)**

