Tips and Tricks
===============

How can I get the project's document directory?
-------------------------------------

This would be the main directory where the project's 
markdown pages are located.

From a markdown page:

```markdown
{{ config.docs_dir }}
```

From the macro module (`main.py`):

```python
env.conf['docs_dir']
```

!!! Note
    1. `env.conf` is a pure dictionary (no dot notation in Python)
    2. In Python, you could also access that information through 
       `env.variables.config['docs_dir']`, but that is more 
       complicated...




Is there some function or variable for information XYZ?
-------------------------------------------------------

If you cannot find an answer in this readme, use `macros_info()` to
display the information on all the variables, functions and filters
available in a page.


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


How can I create a button?
--------------------------

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

!!! Warning "Hyperlinks in HTML"

    **The `fix_url()` function is there to fix _relative_ URLs
    so that they seem to work as in markdown, i.e. relative paths are in
    reference to the `docs` directory** (other URLs are left unchanged).
    
    **Here is the explanation:**
    
    Let's remember that html files are organized differently than their
    markdown counterparts.
    
    If we consider the project's directory as the root directory:
    
    - a page in `/docs/foo.md` will be translated into `/site/foo/index.html`
    - an attachment in `/docs/attachments/foo.pdf` will be copied under
      `/site/attachments/foo.pdf`

    The consequence is that a link to an attachment currently
    in `/docs/attachment/foo.pdf`, e.g.:

        <a href="attachments/foo.pdf">click here</a>

    **will not work**.
    
    You would have to write instead:

         <a href="../attachments/foo.pdf">click here</a>

    which is unintuitive, and therefore error prone.

    The purpose of `fix_url()` is to capture relative urls and lift them
    up one level.

    Supposing you had an `attachment` directory just under the `docs` directory,
    **then a pdf could be accessed with `attachments/foo.pdf`, as you
    would in markdown**.

I would like to include a text file, from line a to line b
----------------------------------

In the source directory of your MkDocs project
(where `mkdocs.yml` generally is),
create a file `module.py`:


```{.python}
import os

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
        full_filename = os.path.join(env.project_dir, filename)
        with open(full_filename, 'r') as f:
            lines = f.readlines()
        line_range = lines[start_line:end_line]
        return '\n'.join(line_range)

```

!!! Tip
    Note how we used `env.project_dir` to identify the source directory
    of the website's project.

!!! Caution
    To keep things simple, this solution reads the whole file into memory;
    so it should not be used for huge files.

In your markdown page, add the call:

    Here is the description:

    ```
    {{ include_file('mkdocs.yml', 0, 4) }}
    ```


Restart the mkdocs server (or rebuild the website) and _voilà_,
you have the first five lines of your file!


How can I discover all attributes and methods of the `env` object?
------------------------------------------------------------------

To discover _all_ items available in the environment available, for writing
custom macros,  you could declare the following macro:

    def define_env(env):
        """
        This is the hook for the functions (new form)
        """
        @env.macro
        def doc_env():
            "Document the environment"
            return {name:getattr(env, name) for name in dir(env) if not name.startswith('_')}


And call it in witin a mardkown page:

    ```
    {{ doc_env() | pprint }}
    ```

This gives the whole range of information available within a page.

!!! Warning
    It is probably **not** a good idea to expose the `env` object to web pages,
    so you should think twice before using this macro
    in a production environment.

    While the consequences of exposing the `env` object (or worse, altering it)
    have not been explored, there is likely a good potential for mischief. 
    Whatever you do with this object, is at your
    own peril.