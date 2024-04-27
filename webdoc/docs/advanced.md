Advanced usage (large projects)
==============

Introduction
------------

The purpose of this page is to provide information 
for **large projects**, or **projects with 
specific technical requirements**, typically with automated deployment.


Gracefully handling variable and macro errors
--------------------------------

By default, Mkdocs-Macros does not render a page that contains
a non-existent variable or non-existent macro, but displays an error
page stating the error.

_From version 1.1.2_

A WARNING message is generated when this occur. 
If the `--strict` or `-s` switch has been applied, the build process
fails when this occus:

```sh
mkdocs serve --strict
```

You can, as well, change the default behavior of Mkdocs-Macros to make it
stricter or laxer on various levels:

- Make the build fail even if the `--strict` switch has not been applied.
- Be more or less strict or lax with errors.

See the [full description of troubleshooting/debugging options](troubleshooting.md).

Including external files in pages
---------------------------------

### Usage

To include external files within a page, you may use the
[`include` directive of jinja2](https://jinja.palletsprojects.com/en/3.1.x/templates/#include), 
directly in your markdown code e.g.:

```jinja2
## Paragraph
{% include 'snippet.md' %}
```

Including another file file **will** therefore execute the macros in that file.

By default the root directory for your included files is in
[docs\_dir](https://www.mkdocs.org/user-guide/configuration/#docs_dir),

### Changing the directory of the includes

You may change the directory of the includes, by setting the
`include_dir` parameter in the plugin's configuration in the yaml file,
e.g.:

    plugins:
      - search
      - macros:
          include_dir: include

In this case, all files to be included will be found in the `include`
subdirectory of your project's directory.

These are the advantages for using a distinct directory for includes:

-   The files to be included ("partials") will not be automatically
    rendered into html
-   A better separation between normal pages and included pages

If you often use `mkdocs serve`, modifying an included page *will*
auto-reload the pages in the browser (this include directory
is added to the list of the "watched" directories).

### Other uses of {% include ... %}

You could conceivably include any type of text file;
and particularly HTML files, since markdown may
contain pure HTML code:

{% raw %}
```jinja2
{% include 'html/content1.html' %}

```
{% endraw %}

The above would fetch the file from a in a html subdirectory (by
default: `docs/html`).


!!! Warning
    The external HTML file must not contain any `<HTML>` and `<BODY>` tags,
    as this will likely break the page.

    Also, you do not need to define any header, footer or
    navigation, or formatting instructions, 
    as this is already taken care of by MkDocs.


!!! Tip
    To further enhance your website, you could use the `include()` macro to 
    insert automatically generated files that contain 
    regularly updated information
    (markdown or html), e.g.: 

    - last result of compilation / deployment, 
    - information contained in a database,
    - etc.


Importing macros from a separate file
-------------------------------------
_From version 0.5.10_

On the other hand, it is possible to place your definitions
in a single file, which you can import
(see [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.11.x/templates/#import)):

{% raw %}
```jinja2
{% import 'includes.md' as includes %}
```
{% endraw %}

(in this case, all Jinja2 macros[^1] defined in the imported file 
will be available with a prefixed notation 
as, e.g.  `includes.myfunction`)

[^1]: These [macros are written in jinja2](https://jinja.palletsprojects.com/en/3.1.x/templates/#macros); they are distinct from the macros of mkdocs.

You may also write:

```
{% from 'includes.md' import myfunction %}
```

By default the root directory for your included files is in [docs_dir](https://www.mkdocs.org/user-guide/configuration/#docs_dir), in other words your `docs`
directory. 

You can change this directory [by setting `include_dir` parameter
in the config file](#changing-the-directory-of-the-includes).

!!! Warning
    _For versions < 0.5.10_

    Macros were imported as variables in the page context. It means
    what they were not available from imported definition files,
    which did not have access to this context
    (see [explanation in Jinja2 documentation](https://jinja.palletsprojects.com/en/2.11.x/templates/#import-visibility)).

    There workaround is to force Jinja2 to use the current page's context, e.g.:  

    - `{% import 'includes.md' as includes with context%}` 
    - `{% from 'includes.md' import myfunction with context%}`.


Treating macros as variables?
-----------------------------

_From version 0.5.10._ 

The `@env.macro` decorator inserts macros into the `env.macros` dictionary.
Macros thus defined will be
part of the **globals** of the Jinja2 environment
(see [explanation in Jinja2 documentation](https://jinja.palletsprojects.com/en/2.11.x/templates/#import-visibility).

In principle you could _also_ insert functions (or any other callable) into
the `env.variables` dictionary, e.g.:

```Python
def foo(...):
    ...
    return ...

env.variables['foo'] = foo
```

In this case, functions will also be available as Jinja2 macros, 
from the markdown pages.

There is no particular reason, at this stage, to do this, but
this information is given as clarificaiton, or 
in case it could find some application in the future.


!!! Warning "Difference with default method"

    The difference is that macros defined in this way 
    will be part of the **context**
    of each page (together with any other variables). 
    They will not be available
    for `{% import .. %}` statements, unless you add the `with context` clause.

    You might also notice some (unsupported) side-effects when
    executing `{{ macros_info() }}` (those functions might not
    necessarily be listed where you would expect them).






Including external yaml files
--------------------------------------------

### Use case

!!! Tip
    If the size of your `mkdocs.yml` file getting **too large** because
    of variables?
    Why not **splitting** this file into separate files? 

When a documentation site is growing (number of pages and complexity),
the number of variables in the `extra:` section of the yaml
configuration file may start to increase fast. 

At this point the config file contains not only configuration data to help
build the website (environment, repetitive snippets, etc.), but **it has
started including information that is pertinent to the subject of the documentation**.

The **solution** is to **split** the config file, 
by using **external yaml files**, which contain the
domain-specific information. This creates a separation of concerns.

It also reduces the number of modifications to the configuration file,
and thus the risk that it becomes accidentally corrupted.

!!! Tip
    You may also want to generate some of these external yaml
    files automatically, e.g. from a database.

### Declaring external YAML files

To include external data files, add the `include_yaml` to the
configuration file of mkdocs (`mkdocs.yml` by default), followed by the
list of external filenames or `key: filename` pairs:

``` {.yaml}
plugins:
    - search
    - macros:
        include_yaml:
          - data/foo.yaml
          - data/bar.yaml
          - key: data/baz.yaml
```

The default directory is the project's root.

Upon loading, the plugin will read each yaml file in order and merge the
variables with those read from the main configuration file. If an entry is
specified in the `key: filename` format, the data from the file will be assigned
to the `key`. In case of conflicts, the latest value will override the earlier
ones.

### Merging branches

The "branches" of the trees of dictionaries will be merged and, in case
of conflict, the plugin will attempt to privilege the latest branch.


!!! Warning "Caution"
    The purpose of this feature is only to allow a separation of concerns.
    For organizational purposes, you should separate your yaml files in a
    clean way, so that each yaml file covers a specific part of the tree.
    Otherwise, this might create complicated cases were the merging
    algorithm might not work as you expect.


Using Macros in the title of the page (Navigation)
-------------------------------

### General Principle

Standard MkDocs looks into the following pieces of data to give a **title** to each 
page in the navigation of the website, in that order of priority
(see [official documentation](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)):

1. The `nav` section in the config file (`My Title : page.md`).
2. The YAML front-matter of the page (`title: My title`).
3. The (first) header of level 1 in the page (`# My title`).
4. The file name (`page.md`).

!!! Warning
    Note how the config file overrides
    the YAML front-matter of the page.

### MkDocs-Macros's policy

**MkDocs does not interfere with that process**, except that it
makes sure that (after the page itself has been rendered),
**any macro found in the **title** is also rendered**.

!!! Tip
    It means that you can call macros in the title of a page,
    in the front matter of the page, in the config file, or
    in the (first) header 1. Whichever will be rendered correctly.

### Front matter of the page (example)

In file `page.md`:

```yaml
---
address: Hello world
title: My Title {address}
---
```


### Config file (example)

```yaml
nav:
   My Title {address} : page.md

extra:
   address: Hello world
```

### Heading 1 of the page (example)

In file `page.md`:

```markdown
---
address: Hello world
---

# My Title {address}
```

### Limitations with emojis

[pymdownx.emoji](https://facelessuser.github.io/pymdown-extensions/extensions/emoji/)
is a Markdown extension that used to convert special strings
(e.g. `:material-robot-happy-outline:`) into actual emojis.

For some obscure reason, the forced rendering of macros in the page's title
prevents the rendering of those emoji strings by the pymdownx.emoji  extension
in the title (see [issue 215](https://github.com/fralau/mkdocs-macros-plugin/issues/215)).

To alleviate that problem, MkDocs-Macros does not attempt to render
macros in the title of a page, when it is obvious that none is present.

!!! Warning
    Please note that currently, when a macro is present in a page title
    AND a smiley string is also found , then the emoji will be
    probably not be rendered.




Controlling the rendering of pages (Syntax Issues)
--------------------------------------------

A frequent issue, when adding the Mkdocs-Macros plugin to an
**existing MkDocs project**, is that some pre-existing markdown pages 
may not be rendered correctly,
or cause a syntax error, or some other error.

That is because Mkdocs-Macros might confuse snippets in those pages
with Jinja2 statements, try to render them and fail.

This issue (as well as its solutions) is described in the chapter 
on [rendering](rendering.md). 


