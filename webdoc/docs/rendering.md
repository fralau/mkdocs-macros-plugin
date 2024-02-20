Controlling the rendering of macros
========================================

What is meant here by _**rendering**_ is the translation
by Mkdocs-Macros of macros as well as [Jinja2 control structures](https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-control-structures) 
and [comments](https://jinja.palletsprojects.com/en/3.1.x/templates/#comments) into pure Markdown/HTML.

!!! Tip "Migrations to Mkdocs-Macros"
    This page may be useful for **large MkDocs projects**
    that have decided to:
    
    - adopt Mkdocs-Macros at a later stage of their existence; 
    - include a **subproject** using Mkdocs-Macros into a main project
      that doesn't.




## Introduction

### Issue
The most frequent issue, when adding the Mkdocs-Macros plugin to an
existing MkDocs project, is that some pre-existing markdown pages 
may not be rendered correctly,
or cause a syntax error, or some other error.

The reason is that, by default, when the Jinja2 template engine in the **macro plugin** 
encounters any text that has the standard markers (typically starting with `{%`} or
`{{`) this will cause a conflict:
it will try to interpret that text as as Jinj2 directive or macro
and fail to behave properly. 

The most likely places where this can occur are the following:

| Location in Markdown file (Block or Inline) | Description                                                                                                |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Code**                                    | Documented Jinja2 statements (or similar syntax), LaTeX                                                    |
| **Maths**                                   | LaTeX statements                                                                                           |
| *_Elsewhere_*                               | Some pre-existing templating or macro language, typically with some constructs starting with `{#` or `{{`. |

<br>


!!! Warning "Expected behaviors in case of failure"

    1. If the statement does not fit Jinja2 syntax, a syntax error
       will be displayed in the rendered page.

    2. If Mkdocs-Macros mistakenly tries to interprets a syntactically
    valid Jinja2 statement containing a variable,
    the most likely result is the page will fail (you can change
    this behavior with the [`on_undefined` parameter in the config file](troubleshooting.md#what-happens-if-a-variable-is-undefined)).

    3. If the statement looks like a macro (callable, with arguments),
       an error and traceback will be displayed in the page.

!!! Note
    This question of accidental rendering is covered generally in the Jinja2 documentation as
    [escaping](https://jinja.palletsprojects.com/en/2.11.x/templates/?highlight=raw#escaping). 
    
    Here we need to help **Mkdocs-Macros** clearly distinguish
    between  **two types of Jinja2 statements**:
    
    1. **Documentation statements**, 
       which must appear as-is in the final HTML pages,
       and therefore **must not** be interpreted by Mkdocs-Macros.
    2. **Actionable Jinja2 statements**: calls to variables or macros, etc.,
       which Mkdocs-Macros **must** replace by their equivalent.


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


### Two Cautions

!!! Warning
    Fencing Jinja2 statements parts as blocks of code
    with the markdown convention
    (using three backticks or three tildes) **will not prevent**
    their interpretation, because this macros plugin intentionally ignores them.

    This is to allow advanced use cases where the content of the code block
    must be computed on the fly.

!!! Note "No Risk of interference of Jinja2 statements with HTML Rendering"

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
    **by Mkdocs-Macros**,
    so that **they actually appear in the HTML output**?

## Solutions

### Solution 1 (Opt-out): Exclude one page from the rendering process

_From version 0.5.7_

!!! Tip "Quick fix"
    This solution is a quick fix, if you are "migrating"
    a pre-existing MkDocs project under Mkdocs-Macros, and
    only a few Markdown pages fail, or do not display correctly.


In the header of the markdown page, indicate that the markdown should
be used "as-is" (no rendering of Mkdocs-Macros),
by setting the `ignore_macros` meta-data key to the `true`value.


```yaml
---
# YAML header
render_macros: false
---
```

!!! Important ""
 That parameter takes priority over all other considerations.
 It guarantees that Mkdocs-Macros will not attempt to render this page.

Any other value than `true` (or an absence of this key), will be interpreted
as a `false` value.


!!! Warning "_From version 1.1.0_"
    
    This directive is no longer accepted and will cause an error:
       
        ---
        # YAML header
        ignore_macros: true
        ---
       



### Solution 2 (Opt-in): Specify which pages must be rendered

_From version 1.0.0_

!!! Tip "Large preexisting projects"
    If you already have a particularly large MkDocs project and have several
    problematic pages, or do not wish write a YAML header for all of them,
    this solution may be for you.

The **opt-in** solution consists of changing the default behavior of 
Mkdocs-Macros: no pages will be rendered (no macros interpreted)
unless this is specifically requested.

After that, there are two ways to specify which pages must be rendered:

1. In the YAML header of each markdown page
   (`render_macros: true`).
2. _From version 1.1.0_ In the configuration file, by setting the
   `force_render_paths` parameter.

To change the default behavior, set the `render_by_default` parameter
to false in the config file (mkdocs.yml):

```yaml
plugins:
  - search
  - macros:
      render_by_default: false
```



#### Opt-in with the markdown page's header

To render a specific page:

```yaml
---
# YAML header
render_macros: true
---
```

Mkdocs-Macros will _not_ attempt to render the other pages.

!!! Warning "_From version 1.1.0_"
    
    The following directive is no longer accepted and will cause an error:
       
        ---
        # YAML header
        ignore_macros: false
        ---


#### Opt-in through the config file

_From version 1.1.0_

When `render_macros` is set to `false` in the config file,
the parameter `force_render_paths` 
can be used to specify a list of **exceptions** (**opt-in**) i.e.
relative paths of pages within the documents directory
(as well as file patterns) in which macros must be rendered.


!!! Note "Use case"
    This feature was developed for very large MkDocs projects, typically when
    a whole subproject is 
    later inserted (as a subdirectory) into a bigger project that doesn't.
    
    Default rendering of macros is out of question since it would 
    break the parent project; at the same time, adding a YAML header
    in all pages of the child project would be tedious.
    
    Setting the subdirectory as an exception (opt-in) can solve the problem.



The syntax follows more or less the [.gitignore pattern matching](https://git-scm.com/docs/gitignore#_pattern_format).

For example:

```yaml
plugins:
  - search
  - macros:
      # do not render the pages by default
      # requires an opt-in
      render_by_default: false
      # render this subdirectory of the documents directory:
      force_render_paths: rendered/ 
```

!!! Warning "The page header has the last word"
    If `render_macros` is set to `false` in the YAML header of the page,
    it will _**never**_ be rendered, even if it matches the specification in
    `force_render_paths`.

    Similarly, if it is set to `true`, it will be rendered regardless of
    `force_render_paths`.



The syntax allows more than one instruction, with [examples provided in this page of the Pathlib library documentation](https://python-path-specification.readthedocs.io/en/stable/readme.html#tutorial), e.g.: 


```yaml
plugins:
  - search
  - macros:
      # do not render the pages by default
      # requires an opt-in
      render_by_default: false
      # render those paths and patterns:
      force_render_paths: |
        # this directory will be rendered:
        rendered/
        # this pattern of files will be rendered:
        render_*.md
```

!!! Note "Syntax of the multiline parameter"

    `force_render_paths` 
    can be a YAML multiline literal string (note the pipe symbol). 
    Comments (starting with a `#`) are accepted _within_ the string
    and are ignored.


It is also possible to specify exceptions with `!` operator,
(e.g. `!foo*.md` excludes all files starting with `foo` and with
the `md` extension from the list of candidates.)

!!! Warning "Location of the root directory"

    Contrary to other parameters of the plugin,
    which consider that the root directory is the Mkdocs project's directory
    (where the config file resides),
    the root directory here is the **documents** directory, generally
    named `docs`. 
    Starting the relative path from that subdirectory is logical,
    since the markdown pages are not supposed
    to exist outside of it.


### Solution 3: Snippets as jinja2 strings (one-liners)

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

### Solution 4: Explicitly marking the snippets as 'raw'

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


The same approach can also be used for inline definitions, e.g.:

     You can use the `raw` expression for inline definitions, for example: {% raw %} `{{{method}}}-{{{url}}}.json` {%  endraw %} for
     escaping 3-bracket expressions often used in Handlebars.

### Solution 5: Altering the syntax of jinja2 for Mkdocs-Macros

Sometimes the introduction of Mkdocs-Macros comes late in the chain, and the
existing pages already contain a lot of Jinja2 statements
(or statements with a similar syntax) that
should appear as-is in the final HTML pages: escaping all of them
would not really be an option.

Or else, you are using some other plugin or Markdown extension that demands
a syntax that is too similar to that normally used by Jinja2
(and you do not wish to implement an MkDocs-Macros [pluglet](pluglets.md) to replace it).


!!! Tip "Solution"
    Rather than refactoring all the existing markdown pages to fence
    those statements to protect them from rendering,
    it may be preferable, as a last resort, 
    to alter the **markers** for variables or blocks
    used in Mkdocs-Macros.

The parameters to control those markers are described in the
documentation of the [high-level API for Jinja2](https://jinja.palletsprojects.com/en/3.1.x/api/#high-level-api).

For example, you may want to replace the curly brackets by square ones,
like this:

```markdown
# This is a title
[# This is a jinja2 comment that will not appear. #]

It costs [[ unit_price ]].

[[% if unit_price > 5 %]]
This is expensive!
[[% endif %]]
```

To obtain this result, simply add the following parameters in the
`macros` section in Mkdoc's config file.  There are:

  - two parameters for code blocks (start and end)
  - two for variables (start and end)
  - two for comments (start and end)

```yaml
plugins:
  - search
  - macros:
      j2_block_start_string: '[[%'
      j2_block_end_string: '%]]'
      j2_variable_start_string: '[['
      j2_variable_end_string: ']]'
      j2_comment_start_string: '[#'
      j2_comment_end_string: '#]'
```


_New in 1.0.7: parameters `j2_comment_start_string` and `j2_comment_end_string`_

You may, of course, chose the combination of markers that best suits your needs.

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

