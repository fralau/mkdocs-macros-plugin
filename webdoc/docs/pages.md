How to Write "Enriched" Markdown Pages
============================

Definitions
-----------

### 1. Variable

A **variable** is a predefined value.

-   The primary source of variables is the `extra` namespace in the
    **config** file (by default: `mkdocs.yml`).
-   You can add variables in the Python module.
-   Also **local variables** can be added directly to each
    markdown page, thanks to jinja2 directives, called `set` (those
    local variables are accessible by jinja2 directives, but not the
    Python code).

### 2. Macro
We call **macros**, Python functions (or callables) that will be
used in jinja2 snippets within the markdown pages. A macro should
return a *string* that can be plain, markdown or HTML.
Each call to the macro in markdown page will be replaced by that result.

!!! Note
    For more information on the full concept of a macro, 
    see [the detailed explanation](why.md#use-case-overcoming-the-intrinsic-limitations-of-markdown-syntax).
    
### 3. Filter
A custom **filter** is a Jinja2 concept. It is essentially a Python
function used with a different syntax,
e.g. `{{ 'my text ' | uppercase}}` (supposing there was a custom
function called `uppercase` and declared as a filter). Just as a
macro, a filter should return a *string* that can be plain, markdown
or HTML.

"Batteries included": defaut objects
--------------------------------------

The following objects are, in particular, available by default,
with their set of attributes:

| Object | Description
| -- | --
| `config` | The standard [config](https://www.mkdocs.org/user-guide/configuration/#project-information) information on MkDocs' environment.
| `page` | Info on the current page ([source](https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/pages.py))
| `navigation` | List of all pages/sections of the website; sections are themselves list of pages; ([source](https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/nav.py))
| `environment` | Data on the system on which MkDocs is currently running.
| `plugin` | Arguments of the macro plugin, in the config file
| `git` | Information on the git version of the website (if part of a git repository)
| `files`| The file structure (for advanced users who know how to manipulate the `mkdocs.structure.files.Files` object, as well as `mkdocs.structure.files.File` objects)

<br/>

For example, 

- `{{ config.site_name }}` returns the main title of the
website
- `{{ environment.system }}` returns the name of the OS.
- `{{ navigation.pages }}` returns a flattened list of all pages
- `{{ plugin.module }}` name of the Python module

To discover what each of these objects contain, you can use the `pretty`
filter provided with the plugin, e.g.:

    {{ context(page) | pretty }}

Configuration variables
-----------------------

To easily and quickly define custom variables, declare them in you
`mkdocs.yml` file:

``` {.yaml}
extra:
    price: 12.50
    company:
        name: Acme
        address: ....
        website: www.acme.com
```

In your markdown file:

``` {.markdown}
The price of the product is {{ price }}.

See [more information on the website]({{ company.website }}).

See <a href="{{ company.website }}">more information on the website</a>.
```


Local (page-level) variables and macros
---------------------------------------

If you really need a variable or macro that needs to remain **local** to
the markdown page, you can use a standard Jinja2 declaration.

!!! Warning
    Note that the `context()` macro (for listing variables)
    will **not** display variables defined at page level. 

### In the YAML header of the page

Variables defined in the YAML header of the page are accessible as themselves
and via the `page.meta` object.

For example, if the the header is as follows:

```yaml
---
title: My special title
bottles:
  whine: 500
  beer: 123
---
```

Then you can access the content of the YAML header in two ways:

1. By name e.g. `{{ title }}` and `{{ bottles.whine }}`
1. Explicitly, i.e. using the dot notation, e.g. 
`{{ page.meta.title }}` and `{{ page.meta.bottles.whine }}`.



!!! Tip
    `{{ page.meta }}` gives the content of the header.
    If you wish to have it typed in a nice tabular form, you can use:
    `{{ context(page.meta) | pretty }}`

!!! Warning "Caution"
    If variables in the metadata have the same name as variables
    already defined (suche as `extra`, `config`, etc.) those will
    be overwritten, but for this page only.

### Using the`Set` keyword

Variables can be defined in the template with the `set` keyword, e.g.:

``` {.jinja2}
{% set acme = 'Acme Company Ltd' %}

Please buy the great products from {{ acme }}!
```

Contrary to variables defined in the `extra` section of the `mkdocs.yml`
file, they are accessible only within the specific page. They are not
accessible from the python code.

!!! Tip
    If you need reference information on the page, there is a `page` object 
    e.g.: `{{ page.title }}`,
    `{{ page.url }}`, `{{ page.is_homepage }}`, etc.

### Page-level macros
It is possible to write **Jinja2 macros** 
written with the Jinja2 syntax (instead of a Python module). 
This allows you benefit from the power of that language
for the manipulation of strings.


Here is an example of Jinja2 macro, 
from the official documentation:

``` {.jinja2}
{% macro input(name, value='', type='text', size=20) -%}
    <input type="{{ type }}" name="{{ name }}" value="{{
        value|e }}" size="{{ size }}">
{%- endmacro %}
```

Which can be called (within the page) as:

``` {.jinja2}
<p>{{ input('username') }}</p>
<p>{{ input('password', type='password') }}</p>
```

!!! Note
    All definitions will remain **local** to the page.

    It is possible to define Jinja2 macros in a separate file,
    and to import them from there in any page, using the
    `{% import ..}` directive.
    See explanations under [Advanced Usage](advanced/#importing-macros-from-a-separate-file).


Conditionals, loops, etc.
-------------------------

With the macros plugin, you may use the [conditional](https://jinja.palletsprojects.com/en/2.11.x/templates/#if)
statement of Jinja2, e.g.

``` {.jinja2}
### My title
{% if  == 'bar' %}
We will write this **first version**
{% else %}
_Second version_
{% endif %}
```

You may produce Markdown or any mix of Markdown, HTML, css
and even javascript that you wish.

Similarly, you could use [for loops](https://jinja.palletsprojects.com/en/2.11.x/templates/#for):

``` {.jinja2}
### List of users
{% set users = ['joe', 'jill', 'david', 'sam'] %}
{% for user in users %}
1. {{ user }}
{% endfor %}
```



In fact, you can do [all the fancy footwork you want with
Jinja2](http://jinja.pocoo.org/docs/2.11/templates/)!
