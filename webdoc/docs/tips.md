Tips and Tricks
===============

Can I use macros in page titles?
--------------------------------
_New in 1.0.2_

Yes. You can use a macro in the title of the page in:

1. The `nav` section of the config file 
1. As the metadata `title` in the yaml header of the page.
1. Directly as the header 1 of the page, e.g.  
`#Environment at {{unit_price}}"`.

For example, in `nav`section of the config file,
e.g. 

```yaml
nav:
    - Home: index.md
    - Environment at {{ unit_price}}: environment.md
    - Second:
        - Also for {{ unit_price}}: other.md
    - Not interpreted: literal.md
```

!!! Note "Rendering"
    The macros in the title are rendered _just after_ those in the markdown
    file. Hence they benefit from the whole context (variables, functions, filters) available in the page.

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

Have you considered [writing your own macro in Python](macros.md)?
It's quick and easy.

!!! Tip "Seriously: macros are easy to write"
    Generating HTML to enrich a page, 
    for adding additional git information,
    listing the content of files, etc.: 
    if you know how to write a Python function,
    you can turn it into a **macro**.





How can I access git information?
--------------------------

See the [page on git](git_info.md).


How do I deal with relative links to documents/images?
---------------------------------------------------

### Issues
A general problem with MkDocs is that you may encounter problems
when referring to other pages.

Suppose you want to refer to another page `foo.md` in the same
directory (undermarkdown).


!!! Bug "This will NOT work with hyperlinks"

    Intuitively one would write:


        See this [other page](foo)

        ![This is an image](image.jpg)


    Unfortunately, this is **NOT** going to work !

!!! Tip "Correct way with hyperlinks"

    The correct way is:


        See this [other page](../foo)

        ![This is an image](../image.jpg)



### Explanation


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

### The `fix_url()` function

The purpose of `fix_url()` is to capture relative urls and lift them
up one level.


Supposing you had an `attachment` directory just under the `docs` directory,
**then a pdf could be accessed with `attachments/foo.pdf`, as you
would in markdown**. You could write, e.g. a macro:

```python
# note the spelling of mkdocs_macros in Python programs (underscore):
from mkdocs_macros import fix_url 


def define_env(env):
    "Define macros..."

    @macro
    def image(url:str, alt:str='')
        url = fix_url(url)
        return '<img src="%s", alt="%s">
```

If you called, as you would expect:

```python 
{{ image('foo.jpg', alt='A foo image')}}
```

Then this would be translated as:
```html
<img src="../foo.jpg", alt="A foo image">
```

!!! Tip
    The `fix_url()` function will only fix relative links,
    and leave other ones (e.g. `https://...` unchanged).


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
    reference to the `docs` directory**
    (other types of URLs are left unchanged).

    See [more information on the subject of relative links](#how-do-i-deal-with-relative-links-to-documentsimages). 
    


I would like to include a text file, from line a to line b
----------------------------------

In the source directory of your MkDocs project
(where `mkdocs.yml` generally is),
create a file `main.py`:


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
        return ''.join(line_range)

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

Macros do not respect indentation (they break admonitions)!
-----------------------------------------------------------

### Issue

When a macro producing text with newlines is rendered in Markdown, 
the additional lines will start from the first column.

It often doesn't matter, but there are cases where **indentation**
is a part of the Markdown syntax.

This is particularly true with the [Admonition](https://python-markdown.github.io/extensions/admonition/) syntax extension, used for defining notes, warnings, etc. 
(see also the [description in the documentation for Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)).


In order to be considered part of an admonition, 
all the text needs to be indented with four columns:

```markdown
!!! note

    I just want to say:

    hello
    there
    world
```

It will be rendered as:
!!! note

    I just want to say:

    hello
    there
    world


Now consider the following macro, which defines the `say_hello()` macro:

```python
# main.py
def define_env(env):
    """
    Hook for macros
    """

    @env.macro
    def say_hello():
        return "hello\nthere\nworld!"
```

### Incorrect

If you have a page like this one, which defines a note:

```markdown
# Homepage

{{ say_hello() }}

Now inside an admonition

!!! note

    I just want to say:

    {{ say_hello() }}
```

The result of the macros' expansion will be:

```markdown
# Homepage

hello
there
world

Now inside an admonition

!!! note

    I just want to say:

    hello
there
world
```

The result of the rendering to HTML in the first case will work.
However, the rendering of the call in the admonition will not be what you expect:

![](admonition.png)

The reason is that the Admonition syntax requires an **indentation**
of 4 characters, for `there\nworld`n to be considered part of the note.

### Correct

This can be solved by using the standard [`indent()`](https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.indent) filter provided by
Jinja2, giving the number of columns as an argument:

```markdown
!!! note

    I just want to say:

    {{ say_hello() | indent(4) }}
```

The result of the macros' rendering into Markdown will be:

```markdown
!!! note

    I just want to say:

    hello
    there
    world
```

And the conversion of Markdown to HTML:
!!! note

    I just want to say:

    hello
    there
    world

The admonition now appears correctly.




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


And call it in within a markdown page:

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

## Can I use my code editor's auto-discovery function in a module? 

Yes. If your code editor is smart enough to provide auto-completion,
then you can make your life much easier, by giving a type hint
to your `declare_env()` function:

```
from mkdocs_macros import MacrosPlugin

def define_env(env:MacrosPlugin):
    "Definition of the module"
    ...
```
In this way, you will benefit from "auto-discovery" each time you invoke
the `env` object. 


Indeed, `env` belongs to the `MacrosPlugin` class,
which is itself
a subclass of [MkDocs' `BasePlugin` class](https://www.mkdocs.org/user-guide/plugins/#baseplugin).



!!! Caution
    Note that you cannot use the `help()` function from the Python interpreter console
    as this raises an error:
    
        >>> from mkdocs_macros import MacrosPlugin
        >>> help(MacrosPlugin)
    

    This is a behavior inherited from the the MkDocs `BasePlugin` class.

    
