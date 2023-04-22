Advanced usage
==============

Introduction
------------

The purpose of this page is to provide information 
for **large projects**, or **projects with 
specific technical requirements**.


Can I make mkdocs-macros build process to fail in case of error (instead of displaying the error on the page)?
-----------------------------------------------------------
Yes. In a context of CD/CI (Continuous Development/Continuous Integration)
the generation of the mkdocs site can be part of a larger script.

In that case, the expected behavior is not to display the error message
in the respective webpage (default behavior), 
but to terminate the build process with an error code.
That is the best way to advertise that something went wrong.

It should then be possible to consult the log (console output)
and track down the offending markdown file and line number.

To activate that behavior, set the `on_error_fail` parameter to `true`
in the config file:

```yaml
plugins:
  - search
  - macros:
      # toggle to true if you are in CD/CI environment
      on_error_fail: true
```

In that case, an error in a macro will terminate 
the mkdocs-macros build or serve process with an **error 100**.

!!! Tip "Make the behavior depend on an environment variable"

    As of version 1.2, [mkdocs incorporates a yaml extension](https://www.mkdocs.org/user-guide/configuration/#environment-variables)
    that allows the value of a configuration option to be set 
    to the value of an environment variable.

You could therefore write:

```yaml
plugins:
    - search
    - macros:
        on_error_fail: !ENV [MACRO_ERROR_FAIL, false]
```

Meaning that the parameter "`on_error_fail` should be set to the value of 
`MACRO_ERROR_FAIL`; or if the environment variable is absent to `false`.




Including snippets in pages
---------------------------------

### Usage

To include snippets (markdown files) within a markdown file, you may use the
`include` directive from jinja2, directly in your markdown code e.g.:

``` {.jinja2}
## Paragraph
{% include 'snippet.md' %}
```

Including another markdown file **will** therefore execute the macros.

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
auto-reload the pages in the browser (the directory is added to the list
of the "watched" directories).

### Other uses

You could conceivably also include HTML files, since markdown may
contain pure HTML code:

``` {.jinja2}
{% include 'html/content1.html' %}
```

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

```
{% import 'includes.md' as includes %}
```

(in this case, all macros defined in the imported file 
will be available with a prefixed notation 
as, e.g.  `includes.myfunction`)

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
_____________________

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




## What you can and can't do with `define_env()`

The fact is that you **cannot** actually access page information
in the `define_env()` function, since
it operates at the configuration stage of the page building process 
(during the [`on_config()` event of MkDocs](https://www.mkdocs.org/user-guide/plugins/#on_config)). 
At that point, **you don't have access to specific pages**


!!! Warning "Vital Note on mkdocs-macros" 
    Of course, you **can** declare **macros**, which **appear** to act on pages. 
    But realize that these are only **declarations** and that their
    execution is **deferred**. 
    The macros will actually be run ** later** 
    (by MkDocs' [`on_page_markdown()` event](https://www.mkdocs.org/user-guide/plugins/#on_page_markdown)),
    just before the markdown is rendered. The framework is so organized
    that, in macros, you are actually "talking" about objects that don't exist yet.

    So you **cannot** influence the rendering process other than by
    adding macros, variables and filters to `mkdocs_macros`.





!!! Danger "Do not modify system entities in `env.variables`"

    Also, the system information in `env.variables`
    is for **reading** purposes.
    You could modify it in your Python code, of course (at your own peril).
    But **by design**, it may have no effect on the mechanics
    of `mkdocs` (these are shallow copies). 

    Whatever you do in that way, is likely to be branded **black magic**.



## Directly influencing the markdown pages generated

_From version 0.5.2_


There are specific cases where you want your module code to be able to modify
the markdown code of a **page, without using macros**.

The proper time to do that, would be 
**before or after** the macros (Jinja2 directives) have been processed.

!!! Note "Technical note: a limitation of the macros mechanism"
    The `define_env()` function operates at the time when MkDocs prepares the
    configuration of website (the `on_config()` event). This is a 
    [global event](https://www.mkdocs.org/user-guide/plugins/#global-events), i.e. any change made at this point will affect the whole
    website. 

    The limitation is that the `define_env()` function is
    "aware" of the general configuration, not of the content of single pages.
    
    **True**,
    it allows you to declare **macros** which will be interpreted later,
    for each page (on the `on_page()` event). **But** it won't
    allow you to modify pages outside of that mechanism.



### Use Case 1: Adding meta values to a page

There are cases where you want to make modifications to a specific 
markdown page, based on the content of that page.

Typically, you may want to programmatically add some meta values to a page,
to be forwarded to the HTML template.

For example you'd want to be able to always have a value for this:

```HTML
<meta name="description" content="{{ page.meta.description }}" />
```
!!! Warning
    Note that in the snippet above, Jinja2 is used by
    MkDocs to produce HTML pages.
    This is **completely distinct** from MkDocs-macros' use of Jinja2
    on Markdown pages (it occurs at a later stage).



Normally [metadata would be defined in the YAML header of the markdown page](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data):

```YAML
---
title: my title
description: This is a description
---
```

!!! Note "Issue"
    **But supposing this was not the case ?** Or supposing you want
    to check or alter that information?

### Use Case 2: Modifying the raw_markdown generated for a page



You might still change that raw markdown, if you really want,
e.g. by adding "footer" information at the bottom of each page.


### Solution
To act on such cases that vary with each markdown page (and depend on
each page, not on the general configuration), 
you may use the two functions, before the markdown is actually rendered:

1. `on_pre_page_macros(env)` : ** before ** the macros are interpreted
   (macros are still present).
1. `on_post_page_macros(env)` : ** after ** the macros are rendered
   (macros have been interpreted). At that point, you have a string `env.raw_markdown` property available, which contains the markdown _after_ the conversion of the Jinja2 template.




For example:

```python
def on_post_page_macros(env):
    """
    Actions to be done after macro interpretation,
    when the markdown is already generated
    """
    # This information will get carried into the HTML template.
    env.page.meta['description'] = ...

    # This will add a (Markdown or HTML) footer
    footer = '\n...'
    env.raw_markdown += footer
```


### Additional Notes for `on_pre_page_macros()` and `on_post_page_macros()`

#### Time of execution

They are executed by the [`on_page_markdown()` event of MkDocs](https://www.mkdocs.org/user-guide/plugins/#on_page_markdown):

- ** before** the rendering the page
- ** before or after** interpretation of the macros, respectively


They operates on a single page.



#### Content and availability of `env.page`
The `page` attribute of `env`, which contains much information specific to the
page (title, filename, metadata, etc.), is available only from the point
of `on_pre_page_macros()` on. 

It is **not** available for the `define_env(env)` function.

It contains notably the following information:

| Attribute       | Value                                                                                                                             |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `title`         | title of the page                                                                                                                 |
| `abs_url`       | the absolute url of the page from the top of the hierarchy                                                                        |
| `canonical_url` | the complete url of the page (typically with `https://...`)                                                                       |
| `markdown`      | the whole markdown code (**before** interpretation; for the **interpreted markdown**, use instead `env.raw_markdown`, see below). |
| `meta`          | the meta data dictionary, as updated (typically) from the YAML header.                                                            |

---

#### Accessing the raw markdown

For the `on_post_page_macros()` event,
the `env` object contains a `raw_markdown` attribute,
which contains the markdown with the macros already interpreted.

!!! Tip "In case of need"
    If the code of the macro modifies `env.raw_markdown`,
    the modifications **will** be reflected in the final HTML page.

#### Use of Global variables
To facilitate the communication between `define_env()` and 
`on_page_markdown()` you may want to define **global variables** within
your module. For a refresher on this, 
[see the summary on W3 Schools](https://www.w3schools.com/python/gloss_python_global_variables.asp). 

## Adding post-build files to the HTML website

_From version 0.5_

### Use case

Sometimes, you want your Python code to add
some files to the HTML website that
MkDocs is producing, completely aside of MkDoc's usual production workflow.

These could be:

- an extra HTML page
- an additional or updated image
- a RSS feed
- a form processor (written for example in the php language)
- ....

!!! Tip
    The logical idea is to add files to the site (HTML) directory,
    which is given by `env.conf['site_dir']`.

!!! Note "Beware the of the 'disappeared file' trap"

    One problem will occur if you attempt to add files to the site directory
    from within the `define_env()` function in your macro module.

    **The file will be created, but nevertheless it is going to "disappear".**

    The reason is that the code of `define_env()` is executed during the 
    `on_config` event of MkDocs; **and you can expect the site directory
    to be wiped out later, during the build phase (which produces
    the HTML files)**. So, of course, the files you
    just created will be deleted.


### Solution: Post-Build Actions



The solution to do that, is to perform those additions
as **post-build** actions (i.e. executed with `on_post_build` event).

Here is an example. Suppose you want to add a special file (e.g. HTML).

```Python
import os
MY_FILENAME = 'foo.html'
my_HTML = None

def define_env(env):
    "Definition of the module"

    # put here your HTML content
    my_HTML = ......


def on_post_build(env):
    "Post-build actions"

    site_dir = env.conf['site_dir']
    file_path = os.path.join(site_dir, MY_FILENAME)
    with open(file_path, 'w') as f:
        f.write(my_HTML)
```

The mkdocs-macros plugin will pick up that function and execute it during
as on `on_post_build()` action.

!!! Warning "Argument of `on_post_build()`"
    In this case, the argument is `env` (as for `define_env()`);
    it is **not**
    `config` as in the `on_post_build()` method in an MkDocs plugin.

    If you want to get the plugin's arguments, you can find them in the
    `env.conf` dictionary.

!!! Note "Global variables"
    To facilitate the communication between `define_env()` and 
    `on_post_build` you may want to define **global variables** within
    your module (in this example: `MY_FILENAME` and `my_HTML`).

!!! Warning
    Do not forget that any variable assigned for the first time
    within a function is _by default_
    a **local** variable: its content will be lost once the function
    is fully executed.

    In the example above, `my_HTML` **must** appear in the global definitions;
    which is why it was assigned an empty value.

    
