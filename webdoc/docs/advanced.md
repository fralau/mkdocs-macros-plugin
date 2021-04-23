Advanced usage
==============

Introduction
------------

The purpose of this page is to provide information 
for **large projects**, or **projects with 
specific technical requirements**.

!!! Tip "Migrations to mkdocs-macros"
    It may be useful for mkdocs projects
    which that have decided to adopt mkdocs-macros at some
    stage in their existence.


How to prevent accidental interpretation of "Jinja-like" statements
------------------------

### Issue

The most frequent issue, when adding the mkdocs-macros plugin to an
existing mkdocs project, is some markdown pages 
may no be rendered correctly,
or cause a syntax error, or some other error.

The reason is that if Jinja2 template engine in the **macro plugin** 
meets any text that has the standard markers (typically starting with `{%`} or
`{{`) this will cause a conflict:
it will try to interpret that text as a macro
and fail to behave properly. 




The most likely places where this can occur are the following:

Location in Markdown file (Block or Inline) | Description 
-- | --
**Code** | Documented Jinja2 statements (or similar syntax), LaTeX  
**Maths** | LaTeX statements 
*_Elsewhere_* | Some pre-existing templating or macro language, typically with some constructs starting with `{#` or `{{`.

<br>


!!! Warning "Expected behaviors in case of failure"

    1. If the statement does not fit Jinja2 syntax, a syntax error
       will be displayed in the rendered page.

    2. If mkdocs-macros mistakenly tries to interprets a syntactically
    valid Jinja2 statement
    containing a variable,
    the most likely result is that **it will "eat" that statement**:
    since it cannot make any sense of it, 
    **it will silently replace it with an empty string**.

    1. If the statement looks like a macro (callable, with arguments),
       an error and traceback will be displayed in the page.

!!! Note
    This question of accidental rendering is covered generally in the Jinja2 documentation as
    [escaping](https://jinja.palletsprojects.com/en/2.11.x/templates/?highlight=raw#escaping). 
    
    Here we need to help **mkdocs-macros** clearly distinguish
    between  **two types of Jinja2 statements**:
    
    1. **Documentation statements**, 
       which must appear as-is in the final HTML pages,
       and therefore **must not** be interpreted by mkdocs-macros.
    2. **Actionable Jinja2 statements**: calls to variables or macros, etc.,
       which mkdocs-macros **must** replace by their equivalent.


### Special Cases

#### Code Blocks Containing Similar Languages

With MkDocs, this situation typically occurs when the website 
is documenting an application that relies on a 
"[djangolike/jinjalike language](https://medium.com/@i5ar/template-languages-a7b362971cbc)" like:

- Django Template Language
- Jinja2 (Python)
- Nunjucks (Javascript)
- Twig (PHP)
- ...

This may also happen for pages that documents
[Ansible](https://ansible-docs.readthedocs.io/zh/stable-2.0/rst/intro.html) directives, which often contain
[variables expressed in a Jinja2 syntax](https://ansible-docs.readthedocs.io/zh/stable-2.0/rst/playbooks_variables.html#using-variables-about-jinja2).


#### Snippets Containing LaTeX

With the plug-in enabled, LaTeX snippets 
would fail to build because {{?}} will trigger the interpretation
of a Jinja2 macro (since `{{` and `}}` are markers).LaTeX snippets

For example, the following LaTeX snippet is used to draw a table:

    ```LaTeX
    \begin{tabular}{|ccc|}
        \hline
        2   & 9     & 4\\
        7   & \multicolumn{2}{c|} {\multirow{2}*{{?}}} \\
        6   &       &\\
        \hline
    \end{tabular}
    ```


### Two Essential Notes

!!! Warning
    Fencing Jinja2 statements parts as blocks of code
    with the markdown convention
    (using three backticks or three tildes) **will not prevent**
    their interpretation, because this macros plugin intentionally ignores them.

    This is to allow advanced use cases where the content of the code block
    must be computed on the fly.

!!! Note "No Risk of intereference of Jinja2 statements with HTML Rendering"

    There is, of course, a **third use of Jinja2 statements**:
    MkDocs also use them in templates to render HTML pages. **Fortunately,
    we can safely ignore that fact.**

    **There is in principle no risk that MkDocs will accidentally
    interpret any Jinja2 statements in markdown pages, during the HTML
    rendering process**.

    The reason is that **MkDocs contains a safety**: **it automatically
    escapes symbols such as '\{'**, which could have a meaning for the later
    rendering in HTML (which also uses Jinja2 templates). 
 
    Here we are trying to solve a different problem:
    **how to avoid interpretation** of Jinja2 statements
    **by mkdocs-macros**,
    so that **they actually appear in the HTML output**?

### Solutions

#### Solution 1: Exclude a page from the rendering process

_From version 0.5.7_

!!! Tip
    This solution is a quick fix, if you are "migrating"
    a pre-existing mkdocs project under mkdocs-macros, and
    some markdown pages fail, or do not display correctly.

    This will leave more time to implement the next solutions.


In the header of the markdown page, indicate that the markdown should
be used "as-is" (no rendering of mkdocs-macros),
by setting the `ignore_macros` meta-data key to the `true`value.

```yaml
---
# YAML header
ignore_macros: true
---
```

Any other value than `true` (or an absence of this key), will be interpreted
as a `false` value.


#### Solution 2: Snippets as jinja2 strings (one-liners)

This hack works for simple one-line snippets.
Suppose you want to prevent the
string `{{ 2 + 2 }}` from being interpreted. It would be sufficient to treat
it as if it was a string in jinja2.

    {{ "{{ 2 + 2 }}" }}

You could also use expressions that contain the double quote symbol,
but in this case you must bracket them with simple quotes:

    {{ '{{ "Hello world" }}' }}

!!!Warning
    Triple quotes (`"""`) around strings are not allowed in Jinja2, so this
    hack cannot be used for multiline statements.

#### Solution 3: Explicitly marking the snippets as 'raw'

The standard solution is to isolate each snippet of code that should not
be interpreted, using the standard jinja2 `raw` directive,
which exists for that purpose:

    {% raw %}
    - task: "create a directory
      file:
        path: "{{ folder_path }}"
        state: directory
        recurse: true
    {% endraw %}

#### Solution 4: Altering the syntax of jinja2 for mkdocs-macros

Sometimes the introduction of mkdocs-macros comes late in the chain, and the
existing pages already contain a lot of Jinja2 statements that are
should appear in the final HTML pages: escaping all of them
would not really be an option.

Or else, you do not wish to bother the writers of markdown pages
with the obligation of escaping Jinja2 statements.

!!! Tip "Solution"
    Rather than refactoring all the existing markdown pages to fence
    those Jinja2 statements,
    it may be preferable to alter the markers for variables or blocks
    used in mkdocs-macros.

For example, you may want to replace the curly brackets by square ones,
like this:

    # This is a title

    It costs [[ unit_price ]].

    [[% if unit_price > 5 %]]
    This is expensive!
    [[% endif %]]

To obtain this result, simply add the following parameters in the
`macros` section. There are two parameters for code blocks (start and
end) and two for variables (start and end).

      - macros:
          j2_block_start_string: '[[%'
          j2_block_end_string: '%]]'
          j2_variable_start_string: '[['
          j2_variable_end_string: ']]'

You may, of course, chose the combination that best suits your needs.

!!! Warning "Caution 1: You are walking out of the beaten path."
    Altering the standard markers used in jinja2 has far-reaching consequences,
    because it will oblige you henceforth use a new form for templates,
    which is specific to your project. When reading this
    documentation, you will have to mentally convert all the examples.

!!! Warning "Caution 2: Use with discretion"
    Errors in defining these new markers, or some
    accidental combinations of markers may have unpredictable
    consequences. **Use with discretion, and at your own risk**. In case
    of trouble, please do not expect help from the maintainers of this
    plugin.



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
list of external files:

``` {.yaml}
plugins:
    - search
    - macros:
        include_yaml:
          - data/foo.yaml
          - data/bar.yaml
```

The default directory is the project's root.

Upon loading, the plugin will read each yaml file in order and merge the
variables with those read from the main configuration file. In case of
conflicts, the latest value will override the earlier ones.

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



### Use Case

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



### Solution
To act on such cases that vary with each markdown page (and depend on
each page, not on the general configuration), 
you may use the two functions, before the markdown is actually rendered:

1. `on_pre_page_macros(env)` : ** before ** the macros are interpreted
   (macros are still present).
1. `on_post_page_macros(env)` : ** after ** the macros are rendered
   (macros have been interpreted). At that point you have an
   `env.raw_markdown` property available.



For example:

```python
def on_post_page_macros(env):
    """
    Actions to be done after macro interpretation,
    just before the markdown is generated
    """
    env.page.meta['description'] = ...
```
This information will get carried into the HTML template.



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

Attribute | Value
--- | -----
`title` | title of the page
`abs_url` | the absolute url of the page from the top of the hierarchy
`canonical_url`| the complete url of the page (typically with `https://...`)
`markdown` | the whole markdown code (**before** interpretation; for the **interpreted markdown**, use instead `env.raw_markdown`, see below).
`meta` | the meta data dictionary, as updated (typically) from the YAML header.

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

    
