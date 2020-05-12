Tips and Tricks
===============

Is there some function or variable for information XYZ?
-------------------------------------------------------

If you cannot find an answer in this readme, use `macros_info()` to
display the information on all the variables, functions and filters
available in a page.

How can I create a button?
--------------------------

See [Example](../python/#example-creating-a-button-macro)


It would be great if XY function was available in mkdocs-macro...
----

Have you considered [writing your own macro in Python](../python)?
It's quick and easy.

!!! Tip "Seriously: macros are easy to write"
    Generating HTML to enrich a page, 
    for adding additional git information,
    listing the content of files, etc.: 
    if you know how to write a Python function,
    you can turn it into a **macro**.



How can I access git information?
--------------------------

See the [page on git](../git_info).


I would like to include a text file, from line a to line b
----------------------------------

In the source directory of your documentation (where `mkdocs.yml` generally is),
create a file `module.py`:


```{.python}
import os

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """


    @env.macro
    def include_file(filename, start_line=0, end_line=None):
        """
        Include a file, optionally indicating start_line and end_line
        (start counting from 0)
        The path is relative to the top directory of the documentation
        project.
        """
        full_filename = os.path.join(SOURCE_DIR, filename)
        with open(full_filename, 'r') as f:
            lines = f.readlines()
        line_range = lines[start_line:end_line]
        return '\n'.join(line_range)

```

!!! Caution
    This solution loads the whole file into memory, so it should not be used
    for huge files.

In your markdown page, add the call:

    Here is the description:

    {{ include_file('mkdocs.yml', 0, 5) }}


Restart the mkdocs server (or rebuild the website) and _voilà_ !


