# mkdocs-macros-plugin: Unleash the power of MkDocs with variables and macros


<!-- To update, run the following command: markdown-toc -i README.md -->

<!-- toc -->

- [Overview](#overview)
- [Context and purpose](#context-and-purpose)
  * [Sources of inspiration](#sources-of-inspiration)
    + [mkdocs-markdownextradata (rosscdh)](#mkdocs-markdownextradata-rosscdh)
    + [jinja2: variables can also be Python callables](#jinja2-variables-can-also-be-python-callables)
    + [Macros in Wiki engines](#macros-in-wiki-engines)
  * [Use Case: Overcoming the Intrinsic Limitations of Markdown Syntax](#use-case-overcoming-the-intrinsic-limitations-of-markdown-syntax)
    + [Solution 1: Markdown extensions](#solution-1-markdown-extensions)
    + [Solution 2: Custom HTML Code](#solution-2-custom-html-code)
    + [Solution 3: Enter Macros](#solution-3-enter-macros)
- [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [Procedure](#procedure)
- [How to use it](#how-to-use-it)
  * [Defining variables in the configuration file](#defining-variables-in-the-configuration-file)
  * [Defining variables and macros in Python code](#defining-variables-and-macros-in-python-code)
  * [Location of the module](#location-of-the-module)
  * [Content of the module](#content-of-the-module)
  * [Defining local variables and macros within the markdown page](#defining-local-variables-and-macros-within-the-markdown-page)
    + [Variables](#variables)
    + [Macros and other templating tools](#macros-and-other-templating-tools)

<!-- tocstop -->

## Overview
**mkdocs-macros-plugin** is a plugin to make it easier for the contributors
to a [MkDocs](mkdocs-macros-plugin) website to make richer and more beautiful
pages, by using **variables** and calls to **macros** in the markdown code.

Regular **variables** can be defined in three ways:

  1. global (for contributors): in the `mkdocs.yml` file,
  under the 'extra' heading
  1. global (for programmers): in a `main.py` file (Python),
  by adding them to a dictionary
  1. local (for contributors): in the markdown file, with a `{%set variable = value %}`
 statement


Similarly programmers can define **macros**, as Python functions in the `main.py` file, which the users will then be able to
use without much difficulty inside of the Python code.

With these two tools, you could write e.g.:

```markdown
The unit price of product A is {{ unit_price }} EUR.
Taking the standard discount into account,
the sale price of 50 units is {{ price(unit_price, 50) }} EUR.
```

Which could translate into:

```
The unit price of product A is 10.00 EUR.
Taking the standard discount into account,
the sale price of 50 units is 450.00 EUR.
```

> The result of a macro can be **HTML code**:
this makes macros especially useful
to make custom extensions to the syntax of markdown.

In reality, it is possible to use the full range of facilities of
[Jinja2 templates](http://jinja.pocoo.org/docs/2.10/templates/).



## Context and purpose

### Sources of inspiration

#### mkdocs-markdownextradata (rosscdh)
The idea for that extension came to me after I saw the excellent plugin
[mkdocs-markdownextradata](https://github.com/rosscdh/mkdocs-markdownextradata-plugin) created by rosscdh, which takes metadata data
from the `mkdocs.yml` file,  and allows you to insert them
with double curly brackets:

```
The price of the item is {{price}}.
```

His concept of using the [jinja2](http://jinja.pocoo.org/docs/2.10/)
templating engine for that purpose was  simple and beautiful:
all it took for this plugin was a few lines of code.


#### jinja2: variables can also be Python callables

And then I discovered that the creators of jinja2,
in their great wisdom (thanks also to them!),
had decided to support *any* kind of Python variables,
*including the callables*, typically functions, e.g.:

```
The price of the item is {{calculate(2, 7.4)}}.
```

They did not think it was worth more a few words,
but it was a diamond in plain sight.

**Oh yeah?** So let's support them also in the markdown pages of MkDocs!

#### Macros in Wiki engines
> **The idea of using 'macros' to speed up the process of writing web pages
is in fact rather old**.

Most wiki engines,
which also rely on some [markup](http://wiki.c2.com/?MarkupLanguage)
language, had the same problems of enriching the presentation of the pages,
at the turn of the year 2000.
In response, they often implemented macros in one form or another
(in mediawiki, they were confusingly called [templates](https://www.mediawiki.org/wiki/Help:Templates)).
And in many cases, these wiki engines relied on the double-curly-braces syntax.

After all, a **static website generator** can be defined as a wiki whose
online editing features have been removed, to make it "wiki-wikier"!


### Use Case: Overcoming the Intrinsic Limitations of Markdown Syntax

[MkDocs](https://www.mkdocs.org/) is a powerful and simple
tool for generating websites. Pages are based on markdown, which is simple by design. The downside is that the expressiveness of markdown is
necessarily limited.

What do you do if you want to enrich your web with new features like buttons,
fancy images, etc. without messing up with templates?


#### Solution 1: Markdown extensions

In order to express more things with it, the standard recourse is to extend
markdown through standard
[markdown extensions](https://python-markdown.github.io/extensions/).
Adding extensions is straightforward, as they
can be directly activated through the `mkdocs.yml`configuration file
of the website e.g.:

```YAML
markdown_extensions:
    - footnotes
```

(If they are non-standard, you just have to install them first on your
machine.)

The problem is, however, that there will *always* be *something* specific
you will want to do, for which there is no markdown extension available.
Or the extension will be too complicated, or not quite what you wanted.

Furthermore, the are limitations to the number of possible extensions,
because extending the grammar of markdown is always a little tricky and
can create incompabilities with the standard syntax or other extensions.

#### Solution 2: Custom HTML Code
If don't have an extension, the standard recourse
is to write some pure HTML within your markdown,
which may also contain some
css code (especially if you are using css that
is specific to your theme or website), e.g.:

```HTML
Here is my code:

<a class='button' href="http:your.website.com/page">Try this</a>
```

The combination of HTML and css works well and can solve a wide range of issues.

But it will soon become tedious, if you have to type
the same code again and again with some variations;
and if you want to change something to the
call (typically the css class), you will then have to manually change
*all* instances of that code, with all the related risks.
This solution doesn't scale.

#### Solution 3: Enter Macros
What if you had a **macro** instead, that would allow you to write
the above HTML as:

```
{{button('Try this', 'http:your.website.com/page')}}
```

... that call was translated into the proper HTML?

**That would be something you could teach to a person who can
already write markdown, without the need for them to get involved
in *any* css or HTML!**

And, what's more,
you could *easily* (as a programmer) write your own new macro in Python,
 whenever you needed one?

A **macro** is, simply stated, a *Python function* that takes a few arguments
and returns a string. It could contain all the logic you want; it could
be as simple as the example above, or as sophisticated as making a query from
a database and formatting the results as markdown.

All of this becomes possible, thanks to **mkdocs-macros-plugin**!






## Installation

### Prerequisites

  - Python version > 3.5
  - MkDocs version > 0.17 (compatible with post 1.0 versions)

### Standard installation
```
pip install mkdocs-macros-plugin
```

### "Manual installation"
To install the package, download it and run:

```python
python setup.py install
```

### Declaration of plugin
Declare the plugin in the the file `mkdocs.yml`:

```yaml
plugins:
    - search
    - macros
```

> **Note:** If you have no `plugins` entry in your config file yet,
you should also add the `search` plugin.
If no `plugins` entry is set, MkDocs enables `search` by default; but
if you use it, then you have to declare it explicitly.


## How to use it



### Defining variables in the configuration file

To easily and quickly define custom variables, declare them in you `mkdocs.yml`
file:

```yaml
extra:
    price: 12.50
    company:
        name: Acme
        address: ....
        website: www.acme.com
```

In your markdown file:

```markdown
The price of the product is {{ price }}.

See [more information on the website]({{ company.website }}).

See <a href="{{ company.website }}">more information on the website</a>.
```



### Defining variables and macros in Python code

### Location of the module
Python code must go into a `main.py` file in the main website's directory
(beside the `mkdocs.yml` file).

>In can also be a package (i.e. a `main` directory),
as long as the `declare_variables` function is accessible.

If you wish, you can change the name of that module by adding a
`python_module` parameter to the `mkdocs.yml` file
(no need to add the `.py` suffix):

```yaml
python_module: source_code
```


### Content of the module
As a first step, you need declare a hook function
called `declare_variables`, with two arguments:

   - `variables`: the dictionary that will contain your variables.
   - `macro`: a decorator function that you can use to declare a Python
function as a Jinja2 callable ('macro' for MkDocs).



The example should be self-explanatory:

```python
def declare_variables(variables, macro):
    """
    This is the hook for the functions

    - variables: the dictionary that contains the variables
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

Here is the code for the `button` function:

```
@macro
def button(label, url):
    "Add a button"
    url = fix_url(url)
    HTML = """<a class='button' href="%s">%s</a>"""
    return HTML % (url, label)
```


Your **registration** of variables or macros for MkDocs
should be done inside that
hook function. On the other hand, nothing prevents you from making imports or
declarations **outside** of this function.

> **Note:** You can export a wide range of objects, and their attributes
remain accessible (see [more information](http://jinja.pocoo.org/docs/2.10/templates/#variables))




### Defining local variables and macros within the markdown page

If you really need a variable or macro that needs to remain **local**
to the markdown page,
you can use a standard Jinja2 declaration.

#### Variables
Variables can be defined with the `set` keyword, e.g.:

```jinja2
{% set acme = 'Acme Company Ltd' %}

Please buy the great products from {{ acme }}!
```

#### Macros and other templating tools
> In fact, you can do
[all the fancy footwork you want with Jinja2](http://jinja.pocoo.org/docs/2.10/templates/),
including defining pure Jina2 macros, conditionals and for loops!

Here is an example of macro, from the official Jinja2 documentation:

```jinja2
{% macro input(name, value='', type='text', size=20) -%}
    <input type="{{ type }}" name="{{ name }}" value="{{
        value|e }}" size="{{ size }}">
{%- endmacro %}
```

Which can be called (within the page) as:

```jinja2
<p>{{ input('username') }}</p>
<p>{{ input('password', type='password') }}</p>
```


> Only remember that you don't need to define any header, footer or navigation,
as this is already taken care of by MkDocs.
Also, all definitions will remain **local** to the page.
