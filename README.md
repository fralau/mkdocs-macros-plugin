# mkdocs-macros-plugin: Unleash the power of MkDocs with variables and macros


<!-- To update, run the following command:
markdown-toc -i README.md 
-->

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
  * [Standard installation](#standard-installation)
  * ["Manual installation"](#manual-installation)
  * [Declaration of plugin](#declaration-of-plugin)
  * [Check that it works](#check-that-it-works)
- [How to use the macros plugin](#how-to-use-the-macros-plugin)
  * [Definitions](#definitions)
  * [Defining variables in the configuration file](#defining-variables-in-the-configuration-file)
  * [Separating documentation variables from configuration variables: using external yaml files](#separating-documentation-variables-from-configuration-variables-using-external-yaml-files)
    + [Use case](#use-case)
    + [Declaring the external files](#declaring-the-external-files)
    + [Merging granches](#merging-granches)
  * [Defining variables, macros, and filters in Python code](#defining-variables-macros-and-filters-in-python-code)
    + [Location of the module](#location-of-the-module)
    + [The `define_env()` function](#the-define_env-function)
    + [The `declare_variables()` function (old)](#the-declare_variables-function-old)
    + [Accessing variables from within a function](#accessing-variables-from-within-a-function)
    + [Accessing the whole config file from within a function](#accessing-the-whole-config-file-from-within-a-function)
    + [Example: Button Function](#example-button-function)
    + [Validating environment variables in Python code](#validating-environment-variables-in-python-code)
  * [Defining local variables and macros within the markdown page](#defining-local-variables-and-macros-within-the-markdown-page)
    + [Local variables](#local-variables)
    + [Macros and other templating tools](#macros-and-other-templating-tools)
  * [Using includes](#using-includes)
  * [Solving syntax conflicts](#solving-syntax-conflicts)
    + [Issue](#issue)
    + [Solution 1: Inline snippets as jinja2 strings](#solution-1-inline-snippets-as-jinja2-strings)
    + [Solution 2: Explicitly marking the snippets as 'raw'](#solution-2-explicitly-marking-the-snippets-as-raw)
    + [Solution 1: Altering the syntax of jinja2](#solution-1-altering-the-syntax-of-jinja2)
  * [Troubleshooting](#troubleshooting)
    + [Error Information in case of module error](#error-information-in-case-of-module-error)
    + [`macros_info()` as the go-to tool](#macros_info-as-the-go-to-tool)
    + [Is there some function or variable for information XYZ?](#is-there-some-function-or-variable-for-information-xyz)
    + [How can I get detailed debug information on an object?](#how-can-i-get-detailed-debug-information-on-an-object)

<!-- tocstop -->

## Overview
**mkdocs-macros-plugin** is a plugin that makes it easier for contributors
of an [MkDocs](https://www.mkdocs.org/) website to produce richer and more beautiful pages. It transforms the markdown pages
into [jinja2](https://jinja.palletsprojects.com/en/2.10.x/) templates
that use **variables**, calls to **macros** and custom **filters**.

Regular **variables** can be defined in four ways:

  1. global (for designers of the website): in the `mkdocs.yml` file,
  under the `extra` heading
  1. global(for contributors): in external yaml definition files
  1. global (for programmers): in a `main.py` file (Python),
  by adding them to a dictionary
  1. local (for contributors): in the markdown file, with a `{%set variable = value %}`
 statement


Similarly programmers can define **macros** and **filters**,
as Python functions in the `main.py` file, which the users will then be able to
use without much difficulty, as jinja2 directives in the markdown page.

By leverage the power of Python in markdown thanks to jinja2, you could write in
one of the pages, e.g.:

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
to make custom extensions to the syntax of markdown, such as buttons,
calls to email, embedding YouTube videos, etc.

It is possible to use the wide range of facilities provided by
[Jinja2 templates](http://jinja.pocoo.org/docs/2.10/templates/).



## Context and purpose

### Sources of inspiration

#### mkdocs-markdownextradata (rosscdh)
The idea for that extension came to me after I saw the excellent plugin
[mkdocs-markdownextradata](https://github.com/rosscdh/mkdocs-markdownextradata-plugin) created by rosscdh, which takes metadata data
from the `mkdocs.yml` file,  and allows you to insert them
with double curly brackets:

```
The price of the item is {{ price }}.
```

His idea of using the [jinja2](http://jinja.pocoo.org/docs/2.10/)
templating engine for that purpose was  simple and beautiful:
all it took for this plugin was a few lines of code.


#### jinja2: variables can also be Python callables

I then discovered that the creators of jinja2,
in their great wisdom (thanks also to them!),
had decided to support *any* kind of Python variables,
*including callables*, typically functions, e.g.:

```
The price of the item is {{ calculate(2, 7.4) }}.
```

Perhaps they did not think it was worth more than a few words in their
documentation, but it was a diamond in plain sight.

> **Oh yeah?** So let's call Python functions from the
markdown pages of MkDocs!

#### Macros in Wiki engines

> **The idea of using 'macros' to speed up the process of writing web pages
is in fact rather old**.

> Most wiki **engines**,
which also rely on some [markup](http://wiki.c2.com/?MarkupLanguage)
language, had the same issue of enriching the markup language of their pages,
at the turn of the year 2000.

In response, they often implemented macros in one form or another
(in mediawiki, they were confusingly called [templates](https://www.mediawiki.org/wiki/Help:Templates)).
And in many cases, these wiki engines already relied on
the double-curly-braces syntax.

After all, a **static website generator** can be defined as a wiki whose
online editing features have been removed, to make it "wiki-wikier"!


### Use Case: Overcoming the Intrinsic Limitations of Markdown Syntax

[MkDocs](https://www.mkdocs.org/) is a powerful, elegant and simple
tool for generating websites. Pages are based on **markdown**,
which is simple by design.

The power and appeal of markdown comes from its extreme simplicity.

> The downside of markdown's powerful simplicity is that its expressiveness
necessarily limited.

> What do you do if you want to enrich markdown pages with features like buttons, 
fancy images, etc.?


#### Solution 1: Markdown extensions

In order to express more concepts with markdown,
one possible recourse is to extend
its through **standard**
[markdown extensions](https://python-markdown.github.io/extensions/).
Adding extensions to mkdocs is straightforward, since those extensions
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
because extending the grammar of markdown is always a little tricky.

Some markdown extensions could alter what you meant with the standard
markdown syntax
(in other words, some markdown text you already wrote could be
accidentally reinterpreted);
or it could be incompatible with other extensions.

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
  - MkDocs version >= 1.0 (it should work > 0.17
    (it should be compatible with post 1.0 versions)

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

### Check that it works
The recommended way to check that the plugin works properly is to add the 
following command in one of the pages of your site (let's say `info.md`):

```
{{ macros_info() }}
```

In the terminak, restart the environment:

```
> mkdocs serve
````
You will notice that additional information now appears in the terminal:

```
INFO    -  Building documentation...
[macros] Macros arguments: {'module_name': 'main', 'include_yaml': [], 'j2_block_start_string': '', 'j2_block_end_string': '', 'j2_variable_start_string': '', 'j2_variable_end_string': ''}
Found: Darwin
```

Within the browser (e.g. http://127.0.0.1:8000/info), you should
see a description of the plugins environment: 

![macros_info()](macros_info.png)

If you see it that information, you should be all set.

Give a good look at the General List, since it gives you an overview
of what you can do out of the box with the macros plugin.

The other parts give you more detailed information.

## How to use the macros plugin

### Definitions

- A **variable** is a predefined value.
  - The primary source of variables
    is the `extra` namespace in the **config** file (by default: `mkdocs.yml`).
  - You can add variables in the Python module.
  - Finally **local variables** can be added directly to each markdown page,
    thanks to jinja2 directives, called `set`
   (those local variables are accessible by jinja2 directives,
   but not the Python code).
- We call **macros**, Python functions (or callables) that will be
  used in jinja2 snippets within the markdown pages.
  A macro should return a *string* that can be plain, markdown
  or HTML.
- A custom *filter* is a jinja2 concept. It is essentially a Python
  function used with a different syntax, e.g. `{{ 'my text ' | uppercase}}`
  (supposing there was a custom function called `uppercase` and declared
  as a filter). Just as a macro, a filter should return a *string*
  that can be plain, markdown or HTML.

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

### Separating documentation variables from configuration variables: using external yaml files

#### Use case

When a documentation site is growing in number of pages and complexity,
the number of variables in the yaml configuration file may start to grow.
At this point it contains not only configuration data
to help build the website (environment, repetitive snippets, etc.),
but it has started including
information that is pertinent to the subject one is documenting.

The solution is to use external yaml files, which contain the
domain-specific information. This creates a separation of concerns.

It also reduces the number of modifications to the configuration file,
and thus the risk that it becomes accidentally corrupted.

> **Tip:** You may also want to generate some of these external yaml
files automatically, e.g. from a database.

#### Declaring the external files
To inlude external data files, add the `include_yaml` to the configuration file
of mkdocs (`mkdocs.yml` by default), followed by the list of external files:

```yaml
plugins:
    - search
    - macros:
        include_yaml:
          - data/foo.yaml
          - data/bar.yaml
```
The default directory is the project directory.

Upon loading, the plugin will read each yaml file in order and merge the variables with those read from the main configuration file.
In case of conflicts, the latest value will override the earlier ones.

#### Merging granches
The "branches" of the trees of dictionaries will be merged and,
in case of conflict, the plugin will attempt to privilege the latest branch.

> The purpose of this feature is only to allow a separation of concerns.
> For organizational purposes, you should separate your yaml files in a
> clean way, so that each yaml file covers a specific part of the tree.
> Otherwise, this might create complicated cases were the merging
> algorithm might not work as you expect.




### Defining variables, macros, and filters in Python code


#### Location of the module
By default, the Python code must go into a `main.py` file
in the main website's directory
(beside the `mkdocs.yml` file).

>Instead of a module file, it also be a *package* (i.e. a `main` subdirectory),
as long as the `declare_env` function is accessible through the __init__.py
file.

If you wish, you can change the name of that module by adding a
`module_name` entry to the `mkdocs.yml` file
(no need to add the `.py` suffix):

```yaml
module_name: source_code
```


#### The `define_env()` function

> New as of version 0.3.0

As a first step, you need declare a hook function
called `define_env`, with one argument: `env` (object).

This object contains the following attributes:

   - `variables`: the dictionary that contains the variables and macros
 It is initialized with the values contained in the `extra` section of the
configuration file (and optionally, with external yaml files).
   - `macro`: a decorator function that you can use to declare a Python
     function as a Jinja2 callable ('macro' for MkDocs).
  - `filters`: a list list of jinja2 filters (default None)
  - `filter`: a decorator for declaring a Python function as a jinja2
    custom filter.


> In case of conflict, jinja2 variables declared in Python will override
> those created by users in yaml files.
> This is a safety feature, to ensure that
> contributors will not accidentally break the setup defined by programmers.

The example should be self-explanatory:

```python
def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """

    env.variables['baz'] = "John Doe"

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
> For the pre 0.3.0 version (`define_variables()`), use `variables` directly,
without prefixing with `env`.


Your **registration** of variables or macros for MkDocs
should be done *within* that hook function.

No special imports are required (the `env` object does all the 'magic').
On the other hand, nothing prevents you from making imports or
declarations **outside** of the `declare_env` function.



> **Note:** You can export a wide range of objects,
and their attributes
will remain accessible to the jinja2 template via the
standard Python convention, e.g. `{{ foo.bar }}`.
Jinja2 will even
(see [more information](http://jinja.pocoo.org/docs/2.10/templates/#variables))


#### The `declare_variables()` function (old)

> This is the old paradigm, before 0.3.0 (still supported).
> Prefer the `define_env` function.

As a first step, you need declare a hook function
called `declare_variables`, with two arguments:

   - `variables`: the dictionary that contains the variables.
 It is initialized with the values contained in the `extra` section of the
 `mkdocs.yml` file.
   - `macro`: a decorator function that you can use to declare a Python
function as a Jinja2 callable ('macro' for MkDocs).

The example should be self-explanatory:

```python
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




Your **registration** of variables or macros for MkDocs
should be done inside that
hook function. On the other hand, nothing prevents you from making imports or
declarations **outside** of this function.

> **Note:** You can export a wide range of objects, and their attributes
remain accessible (see [more information](http://jinja.pocoo.org/docs/2.10/templates/#variables))


#### Accessing variables from within a function
In case you need to access some variables defined in the config
file (under `extra`), use the `variables` dictionary:

Suppose you have:
```yaml
extra:
    price: 12.50
```

You could write a macro:

```python
@macro
def compare_price(my_price):
    "Compare the price to the price in config file"
    if my_price > env.variables['price']:
        return("Price is higher than standard")
    else:
        return("Price is lower than standard")
```


#### Accessing the whole config file from within a function
Sometimes, you might need information from the whole config file,
e.g. `site_description`, `theme`, `copyright`, etc.

The property `conf` of the `env` object contains that information.

For example you could define such a function:

```python
@env.macro
def site_info():
    "Return general info on the website (name, description and theme)"
    info = (env.conf['site_name'], env.conf['site_description'],
            env.conf['theme'].name)
    return "%s/%s (theme: %s)" % info
```

#### Example: Button Function
Here is the code for the `button` function:

```python
@env.macro
def button(label, url):
    "Add a button"
    url = fix_url(url)
    HTML = """<a class='button' href="%s">%s</a>"""
    return HTML % (url, label)
```

#### Validating environment variables in Python code

By design, the call to define_env() is the last stage of
the build process, to create the jinja2 environment that will interpret
the jinja2 directives inserted in the markdown code.

It means in particular, that you can test the variables dictionary
to validate its key/values, and to take appropriate action.

For example, to check that root branches are present
in the variables tree:

```python
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

> This is a place where you could check that you code will not
> conflict with variables defined in the configuration files.


> You may also verify other aspects of the configuration file (`env.conf`).
> Note that the attributes of the `pluging->macro` branch are automatically
> checked by mkdocs (type and default value).

### Defining local variables and macros within the markdown page

If you really need a variable or macro that needs to remain **local**
to the markdown page,
you can use a standard Jinja2 declaration.

#### Local variables
Variables can be defined in the template with the `set` keyword, e.g.:

```jinja2
{% set acme = 'Acme Company Ltd' %}

Please buy the great products from {{ acme }}!
```

Contrary to variables defined in the `extra` section of the `mkdocs.yml` file,
they are accessible only within the specific page.
They are not accessible from the python code.

> If you need reference information on the page, there is a page object,
which you could use in the form e.g.: `{{ page.title }}`, `{{ page.url }}`,
`{{ page.is_homepage }}`, etc. 

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

All definitions will remain **local** to the page.


### Using includes

You may use the `include` directive from jinja2, directly
in your markdown code e.g.:

```Jinja2
## Paragraph
{% include 'snippet.md' %}
```

Including another markdown file **will** therefore execute the macros.

The root directory for your included files is in
[docs_dir](https://www.mkdocs.org/user-guide/configuration/#docs_dir),


You could conceivably also include HTML files, since markdown may contain
pure HTML code:
```Jinja2
{% include 'html/content1.html' %}
```
The above would fetch the file from a
in a html subdirectory (by default: `docs/html`).


> Remember that you do not need to define any header, footer or navigation,
as this is already taken care of by MkDocs.

> *Tip:* To further enhance your website, you could generate some of these
> includes automatically (markdown or html),
> e.g. from information contained in a database.

### Solving syntax conflicts
#### Issue
Sometimes, the form of the block or variable markers in the template 
(e.g. `{{ foo }}` or `{{%if ....%}}`) may cause a conflict,
because the plugin will try to interpret 
snippets of code which should not be interpreted.

This may happen typically when the markdown document is documenting
a "djangolike" language that could be confused with jinja2: typically
Django Template Language, Liquid, or Twig. The markdown page 
will therefore provides examples that should _not_ be interpreted 
([here is a list of templating languages](https://medium.com/@i5ar/template-languages-a7b362971cbc)).

> Fencing these parts as blocks of code with the markdown convention
(using three backticks or three tildes) will not prevent interpretation,
because the plugin deliberately ignores them.

This is to allow advanced use cases where the content of the code block
can be computed on the fly. 

> Note that, in principle, there is no risk that jinja2 syntax will
interfere at a later stage, when mkdocs will convert the markdown
into html.

#### Solution 1: Inline snippets as jinja2 strings
This works for simple one-line snippets. Suppose you want to prevent the string
`{{ 2 + 2 }}` from being interpreted. It is sufficient to treat it
as if it was a string in jinja2.

```
{{ "{{ 2 + 2 }}" }}
```

You could also use expressions with double quotes, but in this case use the 
simple quotes:
```
{{ '{{ "Hello world" }}' }}
```

#### Solution 2: Explicitly marking the snippets as 'raw'
The prefered solution is to isolate each snippet of code 
that should not be interpreted, using the standard jinja2 directive
for that purpose:
```
{% raw %}
- task: "create a directory
  file:
    path: "{{ folder_path }}"
    state: directory
    recurse: true
{% endraw %}
```

#### Solution 1: Altering the syntax of jinja2
Sometimes the use of mkdocs-macros comes late in the chain, 
and rather than refactoring all the markdown pages, it may be
preferable to alter the markers for variables or blocks.

For example, you may want to replace the curly brackets by square ones,
like this:

```
# This is a title

It costs [[ unit_price ]].

[[% if unit_price > 5 %]]
This is expensive!
[[% endif %]]
```


> **Caution 1:** **You are walking out of the beaten path.**
Altering the standard markers used in jinja2 has
far-reaching consequences, because it will oblige you henceforth use a
new form for templates, which is specific to your project.
When reading the standard documentation, 
you will have to mentally convert all the examples. 



To obtain this result, simply add the following parameters in the 
`macros` section. There are two parameters for code blocks (start and end) 
and two for variables (start and end).

```
  - macros:
      j2_block_start_string: '[[%'
      j2_block_end_string: '%]]'
      j2_variable_start_string: '[['
      j2_variable_end_string: ']]'
```

You may of course chose the combination that best suits your needs

> **Caution 2:** Errors in defining these new markers, or some
accidental combinations of markers may have unpredictable consequences.
**Use with discretion, and at your own risk**.
In case of trouble, please do not expect help from the maintainers
of this plugin.

### Troubleshooting
#### Error Information in case of module error
In principle a rendering error in a macro will not stop the server, but
display the error in the browser's page (as you would expect, e.g.
with php).
The terminal's running log also displays errors when they occur.

#### `macros_info()` as the go-to tool
Attempting to run the following line in a page:

```
{{ macros_info() }}
```

and restarting the server in the temrinal with `mkdocs serve` will usually give
you a wealth of information within the browser:

- If the information page appears (as e.g. phpinfo() for php),
  then you know that the plugin must be working. 
- If the page displays and an error message appears, then there
  may be a problem with the plugin's installation.
- If the page does not display at all, then the mkdocs server might not
  be running or there can be a problem running it.

#### Is there some function or variable for information XYZ?
If you cannot find an answer in this readme,
use `macros_info()` to display the information on all the variables,
functions and filters available in a page.

#### How can I get detailed debug information on an object?
For example, if you want to have more information on the `config` object:

```
{{ context('config') | pretty }}
```
(the `pretty` filter displays the result in a nice table form)

You can use this pattern for pretty much any object, even those
you declared in a module.

When used on its own, `context()` gives the general list of variables
in the plugin's environment:
```
{{ context() | pretty }}
```

