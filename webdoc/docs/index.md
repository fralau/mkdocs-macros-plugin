mkdocs-macros
=============
** A plugin for unleashing the power of Mkdocs, by using variables and macros **

!!! Tip "Attention"
    This is more than a plugin: it's a **mini-framework**!

## Overview
**mkdocs-macros-plugin** is a plugin/framework that
makes it easy for contributors
of an [MkDocs](https://www.mkdocs.org/) website to produce richer and more beautiful pages. It transforms the markdown pages
into [jinja2](https://jinja.palletsprojects.com/en/2.10.x/) templates
that use **variables**, calls to **macros** and custom **filters**.

**mkdocs-macros-plugin** is very easy to use out of the box: it provides
data about the platform, the git repository (if any), etc. 
Yet it so powerful that it could be called a "mini-framework".


!!! Note

    By using mkdocs-macros, you can **cut down the number of plugins required**
    for your documentation project.

    In a wide range of cases, **[writing your own macros](../python)**
    (Python functions), 
    could **save the effort of developing
    _new_ plugins for mkdocs**.


### Variables
Regular **variables** can be defined in four ways:

  1. global (for designers of the website): in the `mkdocs.yml` file,
    under the `extra` heading
  1. global(for contributors): in external yaml definition files
  1. global (for programmers): in a `main.py` file (Python),
    by adding them to a dictionary
  1. local (for contributors): in the markdown file, with a `{%set variable = value %}` or `{{page.meta.*}}` variables.
 statement


### Enrich markdown with templating

You can leverage the power of Python in markdown thanks to jinja2
by writing this :

```markdown
The unit price of product A is {{ unit_price }} EUR.
Taking the standard discount into account,
the sale price of 50 units is {{ price(unit_price, 50) }} EUR.
```

If you defined a `price()` function, this could translate into:

```
The unit price of product A is 10.00 EUR.
Taking the standard discount into account,
the sale price of 50 units is 450.00 EUR.
```



It is possible to use the wide range of facilities provided by
[Jinja2 templates](http://jinja.pocoo.org/docs/2.10/templates/).

### Create Your Own Macros and Filters

Instead of creating countless new plugins, programmers can define 
their **macros** and **filters**.

!!! Note "Getting Started with Macros"
    Need a function to display some repetitive markdown,
    or environment information? 

    If you are are Python programmer, go ahead and  **[create your own
    macros and filters in Python!](../python)**

    It's actually much, much easier than writing 
    a VBA function for Excel...

    Create a `module.py` file in the top directory of your mkdocs
    project and add this call:

        import ...

        def define_env(env):
          "Hook function"

          @env.macro
          def mymacro(...)
              ...
              return some_string
    

    You can insert a call in any markdown page of your project:

        {{ mymacro(...) }}

    Restart your mkdocs server.
    
    Et _voilà_ !


!!! Tip "Producing HTML"
    The result of a macro can also be **HTML code**:
    this makes macros especially useful
    to make custom extensions to the syntax of markdown, such as buttons,
    calls to email, embedding YouTube videos, etc.




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

### Declaration of the macros plugin
Declare the plugin in the the file `mkdocs.yml`:

```yaml
plugins:
    - search
    - macros
```

!!! Warning
    If you are creating the `plugins` entry in your config file,
    you should also insert a line for the `search` plugin.

    In the absence of the `plugins` entry,
    MkDocs enables `search` by default.
    But when it is present, then you MUST declare it explicitly if you 
    want to use it.

### Check that it works

!!! Tip
    The recommended way to check that the plugin works properly is to add the 
    following command in one of the pages of your site (let's say `info.md`):

    ```
    {{ macros_info() }}
    ```

In the terminal, restart the environment:

```
> mkdocs serve
```
You will notice that additional information now appears in the terminal:

```
INFO    -  Building documentation...
[macros] Macros arguments: {'module_name': 'main', 'include_yaml': [], 'j2_block_start_string': '', 'j2_block_end_string': '', 'j2_variable_start_string': '', 'j2_variable_end_string': ''}
```

Within the browser (e.g. http://127.0.0.1:8000/info), you should
see a description of the plugins environment: 

![macros_info()](macros_info.png)

If you see it that information, you should be all set.

Give a good look at the General List, since it gives you an overview
of what you can do out of the box with the macros plugin.

The other parts give you more detailed information.

