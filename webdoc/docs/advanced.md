Advanced usage
==============

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


How to prevent interpretation of Jinja-like statements
------------------------

### Issue

Sometimes, the form of the block or variable markers in the template
(e.g. `{{ foo }}` or `{{%if ....%}}`) may cause a conflict, because the
**macro plugin** will try to interpret snippets of "Jinja-like" code
which should not be
interpreted.

!!! Warning

    If mkdocs-macros mistakenly tries to interprets a Jinja2 statement,
    the most likely result is that **it will "eat" that statement**:
    since it cannot make any sense of it, 
    **it will silently replace it with an empty string**.

!!! Note
    This question is covered generally in the Jinja2 documentation as
    [escaping](https://jinja.palletsprojects.com/en/2.11.x/templates/?highlight=raw#escaping). 
    
    Here we need to help **mkdocs-macros** clearly distinguish
    between  **two types of Jinja2 statements**:
    
    1. **Documentation statements**, 
       which must appear as-is in the final HTML pages,
       and therefore **must not** be interpreted by mkdocs-macros.
    2. **Actionable Jinja2 statements**: calls to variables or macros, etc.,
       which mkdocs-macros **must** replace by their equivalent.


    

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

### Solution 1: Snippets as jinja2 strings (one-liners)

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

### Solution 2: Explicitly marking the snippets as 'raw'

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

### Solution 3: Altering the syntax of jinja2 for mkdocs-macros

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

