Controlling the rendering of pages
==================================


!!! Tip "Migrations to mkdocs-macros"
    This page may be useful for **large mkdocs projects**
    that have decided to adopt mkdocs-macros at a later
    stage of their existence.




## Introduction

### Issue
The most frequent issue, when adding the mkdocs-macros plugin to an
existing mkdocs project, is some markdown pages 
may not be rendered correctly,
or cause a syntax error, or some other error.

The reason is that, by default, when the Jinja2 template engine in the **macro plugin** 
encouters any text that has the standard markers (typically starting with `{%`} or
`{{`) this will cause a conflict:
it will try to interpret that text as a macro
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

    2. If mkdocs-macros mistakenly tries to interprets a syntactically
    valid Jinja2 statement containing a variable,
    the most likely result is the page will fail (you can change
    this behavior with the [`on_undefined` parameter in the config file](../troubleshooting#what-happens-if-a-variable-is-undefined)).

    3. If the statement looks like a macro (callable, with arguments),
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


### Two Cautions

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

## Solutions

### Solution 1 (Opt-out): Exclude one page from the rendering process

_From version 0.5.7_

!!! Tip "Quick fix"
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
render_macros: false
---
```

Any other value than `true` (or an absence of this key), will be interpreted
as a `false` value.


!!! Warning "_From version 1.0.0_"
    
    This directive is also accepted, though it is now deprecated:
       
        ---
        # YAML header
        ignore_macros: true
        ---
       



### Solution 2 (Opt-in): Specify which pages must be rendered

_From version 1.0.0_

!!! Tip "Large preexisting projects"
    If you already have a large mkdocs project and have several
    problematic pages, or do not wish to control
    the rendering of all pages, this solution may be for you.

The **opt-in** solution consists of changing the defaut behavior of 
mkdocs-macros: no pages will be rendered (no macros interpreted)
unless this is specifically requested in the page's header.

To change the default behavior, set the `render_by_default` parameter
to false in the config file (mkdocs.yml):

```yaml
plugins:
  - search
  - macros:
      render_by_default: false
```

To render a specific page:

```yaml
---
# YAML header
render_macros: true
---
```

mkdocs-macros will _not_ attempt to render the other pages.

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

### Solution 5: Altering the syntax of jinja2 for mkdocs-macros

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

