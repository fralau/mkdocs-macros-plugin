# mkdocs-macros-plugin: Unleash the power of MkDocs with variables and macros


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
![PyPI](https://img.shields.io/pypi/v/mkdocs-macros-plugin)

* **View the [MkDocs macro documentation](https://mkdocs-macros-plugin.readthedocs.io/)**
* View the [general Mkdocs documentation](https://www.mkdocs.org/)

<!-- To update, run the following command:
markdown-toc -i README.md 
-->

<!-- toc -->

- [Overview](#overview)
- [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [Standard installation](#standard-installation)
  * ["Manual installation"](#manual-installation)
  * [Declaration of plugin](#declaration-of-plugin)
  * [Check that it works](#check-that-it-works)

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
[Jinja2 templates](http://jinja.pocoo.org/docs/2.10/templates/).



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
see a description of the plugins environment: 

![macros_info()](macros_info.png)

If you see it that information, you should be all set.

Give a good look at the General List, since it gives you an overview
of what you can do out of the box with the macros plugin.

The other parts give you more detailed information.

