<div align="center">

![Mkdocs-Macros](logo.png)

#  Unleash the power of MkDocs with variables and macros



[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
![Language](https://img.shields.io/github/languages/top/fralau/mkdocs_macros_plugin)
![PyPI](https://img.shields.io/pypi/v/mkdocs-macros-plugin)
![Github](https://img.shields.io/github/v/tag/fralau/mkdocs_macros_plugin?label=github%20tag)
![macros](https://img.shields.io/pypi/dm/mkdocs-macros-plugin)

:open_file_folder: [Used by > 2K repositories on Github](https://github.com/fralau/mkdocs_macros_plugin/network/dependents)<br>
🥇 Listed as [High-Quality Plugin](https://github.com/mkdocs/catalog#-code-execution-variables--templating)


**mkdocs-macros-plugin** is a general-purpose plugin for [MkDocs](https://www.mkdocs.org/)<br>that uses  **variables** and **macros** (functions) to  automate tasks, and produce richer and more beautiful pages.





```markdown
The unit price of product A is {{ unit_price }} EUR.
Taking the standard discount into account,
the sale price of 50 units is {{ price(unit_price, 50) }} EUR.
```


View the [mkdocs-macro documentation](https://mkdocs-macros-plugin.readthedocs.io/) on Read the Docs.
</div>


<!-- To update, run the following command:
markdown-toc -i README.md 
-->

<!-- toc -->

## Overview
**mkdocs-macros-plugin** is a plugin that makes it easier for contributors
of an [MkDocs](https://www.mkdocs.org/) website to produce richer and more beautiful pages. It transforms the markdown pages
into [jinja2](https://jinja.palletsprojects.com/en/2.10.x/) templates
that use **variables**, calls to **macros** and custom **filters**.

> **You can also partially replace MkDocs plugins with mkdocs-macros modules,
> and [pluglets](https://mkdocs-macros-plugin.readthedocs.io/en/latest/pluglets/) 
> (pre-installed modules).**


### Using variables
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

> The result of a macro can be **HTML code**:
this makes macros especially useful
to make custom extensions to the syntax of markdown, such as buttons,
calls to email, embedding YouTube videos, etc.

It is possible to use the wide range of facilities provided by
[Jinja2 templates](http://jinja.pocoo.org/docs/2.10/templates/) such
as conditions (`{% if ... %}`) and loops (`{% for ... %}`).

### Defining variables

Regular **variables** can be defined in five ways:

| No | Validity | For whom | Description |
| --- | --- | --- | ---- |
| 1. | global | designer of the website | in the `mkdocs.yml` file, under the `extra` heading |
| 2. | global | contributor | in external yaml definition files |
| 3. | global | programmer | in a `main.py` file (Python), by adding them to a dictionary |
| 4. | local (page) | writer | in the YAML header of each Markdown page |
| 5. | local (page) | writer | with a `{%set variable = value %}`  statement |

In addition, predefined objects are provided (local and global), typically
for the environment, project, page, git information, etc. 


### Macros and filters
Similarly programmers can define their own **macros** and **filters**,
as Python functions in the `main.py` file, 
which the users will then be able to
use without much difficulty, as jinja2 directives in the markdown page.



## Installation

### Prerequisites

  - Python version > 3.7
  - MkDocs version >= 1.0
    (compatible with post 1.5 versions)

### Standard installation
```
pip install mkdocs-macros-plugin
```

### "Manual installation"
To install the package, download it and run:

```
pip install .
# or...
python setup.py install
```

### Development/test installation
To install the extra dependencies required for testing the package, run:

```
pip install "mkdocs-macros-plugin[test]"
```

### Declaration of plugin
Declare the plugin in the file `mkdocs.yml`:

```yaml
plugins:
    - search
    - macros
```

> **Note:** If you have no `plugins` entry in your config file yet,
you should also add the `search` plugin.
If no `plugins` entry is set, MkDocs enables `search` by default; but
if you use it, then you have to declare it explicitly.

By default, undefined variables are printed to the page as-is. If you
wish for a page to fail on undefined variables, you should use the
below configuration instead:

```yaml
plugins:
    - search
    - macros
          on_undefined: strict
```

For details and more options, see the [documentation](
https://mkdocs-macros-plugin.readthedocs.io/en/latest/troubleshooting/#what-happens-if-a-variable-is-undefined).

### Check that it works
The recommended way to check that the plugin works properly is to add the 
following command in one of the pages of your site (let's say `info.md`):

```
{{ macros_info() }}
```

In the terminal, restart the environment:

```
> mkdocs serve
````
You will notice that additional information now appears in the terminal:

```
INFO    -  Building documentation...
[macros] Macros arguments: {'module_name': 'main', 'include_yaml': [], 'j2_block_start_string': '', 'j2_block_end_string': '', 'j2_variable_start_string': '', 'j2_variable_end_string': ''}
```

Within the browser (e.g. http://127.0.0.1:8000/info), you should
see a description of the plugin's environment: 

![macros_info()](macros_info.png)

If you see it that information, you should be all set.

Give a good look at the General List, since it gives you an overview
of what you can do out of the box with the macros plugin.

The other parts give you more detailed information.


## Using pluglets

### What are pluglets?

**Pluglets** are small, easy-to-write programs
that use mkdocs-macro's foundation
to offer services to mkdocs projects, which would normally
be offered by plugins.

Pluglets are Python packages, which can be hosted on github, and 
distributed through [PyPI](https://pypi.org/).


### How to add a pluglet to an mkdocs project?

Install it: 

```shell
pip install <pluglet_name>
```

Declare it in the project's config (`mkdocs.yml`) file:

```yaml
plugins:
  - search
  - macros:
      modules:
        - <pluglet_name> 
```

### How to write a pluglet?

[See instructions in the documentation](https://mkdocs-macros-plugin.readthedocs.io/en/latest/pluglets/).

A sample pluglet can be found in [mkdocs-test (github)](https://github.com/fralau/mkdocs-macros-test).

### List of existing pluglets

[See the wiki page on Github](https://github.com/fralau/mkdocs-macros-plugin/wiki/Mkdocs%E2%80%90Macros-Pluglets).
