How to use the macros plugin
============================

Definitions
-----------

-   A **variable** is a predefined value.
    -   The primary source of variables is the `extra` namespace in the
        **config** file (by default: `mkdocs.yml`).
    -   You can add variables in the Python module.
    -   Finally **local variables** can be added directly to each
        markdown page, thanks to jinja2 directives, called `set` (those
        local variables are accessible by jinja2 directives, but not the
        Python code).
-   We call **macros**, Python functions (or callables) that will be
    used in jinja2 snippets within the markdown pages. A macro should
    return a *string* that can be plain, markdown or HTML.
-   A custom *filter* is a jinja2 concept. It is essentially a Python
    function used with a different syntax,
    e.g. `{{ 'my text ' | uppercase}}` (supposing there was a custom
    function called `uppercase` and declared as a filter). Just as a
    macro, a filter should return a *string* that can be plain, markdown
    or HTML.

"Batteries included": defaut variables
--------------------------------------

The following variables are, in particular, available by default:

-   **config**: the standard
    [config](https://www.mkdocs.org/user-guide/configuration/#project-information)
    information on MkDocs' environment.
-   **page**: Info on the current page.
    ([source](https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/pages.py))
-   **navigation**: list of all pages/sections of the website; sections
    are themselves list of pages;
    ([source](https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/nav.py))
-   **environment**: data on the system on which MkDocs is currently
    running.
-   **git**: information on the git version of the website (if part of a
    git repository)

For example, 

- `{{ config.site_name }}` returns the main title of the
website
- `{{ environment.system }}` returns the name of the OS.
- `{{ navigation.pages }}` returns a flattened list of all pages

To discover what each of these objects contain, you can use the `pretty`
filter provided with the plugin, e.g.:

    {{ context(page) | pretty }}

Defining variables in the configuration file
--------------------------------------------

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


Defining local variables and macros within the markdown page
------------------------------------------------------------

If you really need a variable or macro that needs to remain **local** to
the markdown page, you can use a standard Jinja2 declaration.

### Local variables

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

### Macros and other templating tools

> In fact, you can do [all the fancy footwork you want with
> Jinja2](http://jinja.pocoo.org/docs/2.10/templates/), including
> defining pure Jina2 macros, conditionals and 'for' loops!

Here is an example of macro, from the official Jinja2 documentation:

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

All definitions will remain **local** to the page.

