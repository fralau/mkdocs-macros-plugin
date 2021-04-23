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

In principle a rendering error in a macro will not stop the server, but
display the error in the browser's page (as you would expect, e.g. with
php). The terminal's running log also displays errors when they occur.

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


Help! mkdocs-macros is eating pieces of my documentation!
------------------------------------------------

The problem is that mkdocs-macros is believing that statements
of the form `\{\{ .... }}` or `{% ... %}` 
in your pages, which you want to appear in the HTML output,
are intended for it.

![dog eating ice-cream, credit: https://unsplash.com/photos/OYUzC-h1glg](../dog-eating.jpg)

This result is usually **an empty string where you expected one**.

For the solutions to that problem, see 
[how to prevent interpretation of Jinja-like
statements](../advanced/#how-to-prevent-interpretation-of-jinja-like-statements).




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





Where Can I get Help?
---------------------

### Issues

Check the [issues](https://github.com/fralau/mkdocs_macros_plugin/issues) 
on the github repo.


!!! Tip "Tips"

    - Some issues have the marker **Useful Tip**.
    - Also check the **closed issues**. It could be that your issue
      has already been solved and closed!
    - Also, you could check similar questions, to see if they could
      point you to the right questions.


If you want to add a new issue (for a bug or an enhancement request), 
or comment on an existing one,
you are more than welcome!

All issues are carefully reviewed and often get a quick answer.

### If all else fails...

If you still have questions:

- Check the Q&As 🙏 in the [project's Discussions space, on github](https://github.com/fralau/mkdocs_macros_plugin/discussions).
- Post a Q&A 🙏 item!
