mkdocs-macros
=============
** A plugin for unleashing the power of [Mkdocs](https://www.mkdocs.org/), 
by using variables and macros. **

!!! Tip "A mini-framework"
    mkdocs-macros is more than a "plugin". It is a **mini-framework**
    developped with one goal in mind: 
    
    **To enhance mkdocs with the macro and automation capabilities
    available to a [wiki engine](https://wiki.c2.com/?WikiEngine).** [^6]

    For more information, see [Why this project?](why)
    

[^6]: With reference to existing wiki engines such as [Dokuwiki](https://www.dokuwiki.org/dokuwiki) or [Atlassian Confluence](https://www.atlassian.com/software/confluence).

## Overview

### Definition

**mkdocs-macros-plugin** is a plugin/framework that
makes it easy for contributors
of an [MkDocs](https://www.mkdocs.org/) website to produce richer and more beautiful pages. It can do two things:

1. Transforming the markdown pages
into [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates
that:  
     - Use environment or custom **variables**, 
     - Call pre-defined or custom **macros**, 
     - Exploit standard or custom **filters**
1. **Replacing MkDocs plugins** for a wide range of tasks: e.g. manipulating the navigation, adding files after the html pages have already been generated etc.

The capabilities of **mkdocs-macros-plugin** are such 
that it can be called a **"mini-framework"**.

**mkdocs-macros-plugin** is very easy to use **out of the box**,
even for small documentation projects: it provides
data about the platform, the git repository (if any), etc. 





### Variables
Regular **variables** are loaded with each markdown page which is 
being rendered.

Variables can be defined in five different ways:

  1. **Global**, i.e. for the whole documentation project:
    1. (for designers of the website): in the `mkdocs.yml` file,
       under the `extra` heading
    2. (for contributors): in external yaml definition files
    3. (for programmers): in a module (Python),
    by adding them to a dictionary
  2. **Local**, i.e. in each Markdown page (for contributors): 
    1. in the YAML header
    2. in the text, with a `{%set variable = value %}`
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

    If you are a Python programmer, go ahead and  **[create your own
    macros and filters in Python!](python)**

    It's actually much, much easier than writing 
    a VBA function for Excel...

    Create a `main.py` file in the top directory of your mkdocs
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

### Boosting large or complex documentation projects
mkdocs-macros was also developed with 
[**large or complex projects in mind**](advanced).

You can include separate configurations files, import Jinja2 macro definitions,
add "post-production" elements to your website, etc.

You can go all the way as to pre-package modules
into [**pluglets**](pluglets) that can be installed as Python packages.




!!! Note

    By using mkdocs-macros, you can **cut down the number of plugins required**
    for your documentation project.

    In a wide range of cases, **[writing your own module with macros](python)**
    (Python functions for a single website), 
    could **save the effort of developing
    _new_ plugins for mkdocs**.


## Installation

### Prerequisites

  - Python version > 3.5
  - MkDocs version >= 1.0 (it should work > 0.17
    (it should be compatible with post 1.0 versions)

### Standard installation
```
pip install mkdocs-macros-plugin
```

If you wish to also run the tests or rebuild the project's documentation:

```
pip install 'mkdocs-macros-plugin[test]'
```

### "Manual installation"
To install the package, download the code from its
[github page](https://github.com/fralau/mkdocs_macros_plugin/) and run:

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

### Configuration of the plugin

Here are all the possible arguments in the `plugin` section
of the MkDocs' config file:

| Argument | Default | Description
| -- | -- | --
| `module_name` | `main` | [Name of the Python module](python/#local-module) containing macros, filters and variables. Indicate the file or directory, without extension; you may specify a path (e.g. `include/module`). If no `main` module is available, it is ignored.
| `modules` | `[]`| [List of preinstalled Python modules](python/#adding-pre-installed-modules), i.e. listed by `pip list`.
| `include_dir` | | [Directory for including external files](advanced/#changing-the-directory-of-the-includes) 
| `include_yaml`| `[]` | [List of yaml files to be included](advanced/#including-external-yaml-files)
| `j2_block_start_string` | | [Non-standard Jinja2 marker for start of block](advanced/#solution-3-altering-the-syntax-of-jinja2-for-mkdocs-macros)
| `j2_block_end_string` || [Non-standard Jinja2 marker for end of block](advanced/#solution-3-altering-the-syntax-of-jinja2-for-mkdocs-macros)
| `j2_variable_start_string` || [Non-standard Jinja2 marker for start of variable](advanced/#solution-3-altering-the-syntax-of-jinja2-for-mkdocs-macros) 
| `j2_variable_end_string` || [Non-standard Jinja2 marker for end of variable](advanced/#solution-3-altering-the-syntax-of-jinja2-for-mkdocs-macros)


___
For example:

```yaml
plugins:
  - search
  - macros:
      module_name: mymodule
      include_dir: include
```
