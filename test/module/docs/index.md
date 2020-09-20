---
# This YAML header contains variables used inside the page.
announcement: Hello world
bottles:
  orange_juice: 500
  coca_cola: 123
  lemonade: 10
  ginger_ale: 3
---

# Test Page (Modules)

The total costs is {{ unit_price }} euros.

> The figure 50 should appear (`unit_price`), defined in config file).



## Variables
### Predefined

- **Project directory**: `{{ config.docs_dir }}`
- **Project directory**: `{{ special_docs_dir or "NOT FOUND" }}`


### From the module

> This was defined as variable `cwd` in `main.py`

**Current working directory**: `{{ cwd }}`.


### Git version:

{% if git.status %}

{{ git.short_commit }} ({{ git.date }})

{{ git.date.strftime("%b %d, %Y %H:%M:%S") }}


({{ git.non_existent or now() }})

{% endif %}

### Page
Page: {{ page }}

Date: {{ now().year }} {{ now().month }}

### List of users
{% set users = ['joe', 'jill', 'david', 'sam'] %}
With a made up list: `{{ users }}`

Enumerate:
{% for user in users %}
1. {{ user }}
{% endfor %}


## Macro (defined in module)

From the `button()` macro.

This is a:

{{ button ("Try this", 'https://squidfunk.github.io/mkdocs-material')}}

## Included file

With Jinja2 `include` directive (file `foo.md`)

---
{% include 'foo.md' %}

---

## Accessing meta variables in the Markdown page

> Those are variables in the YAML header at the top of the markdown page.
Here is my announcement:

** {{ page.meta.announcement }} **


Here is the content of the `meta` vars:

{{ context(page.meta) | pretty }}

> Using the `context()` macro and the `pretty` filter.

### Dot notation 
We have **{{ page.meta.bottles.orange_juice }}** bottles of orange juice and
**{{ page.meta.bottles.lemonade }}** bottles of lemonade
{% raw %} 
(respectively: `{{ page.meta.bottles.orange_juice }}` 
and `{ page.meta.bottles.lemonade }}`).
{% endraw %}

### Use of a for loop
> Here is an example of a for loop, using Jinja2 directives.

{% for bottle, quantity in page.meta.bottles.items() %}
1. {{ bottle }}: {{ quantity }}
{% endfor %}

