---
bottles:
  whine: 500
  beer: 123
  whisky: 10
---

# This is a title

It costs {{ unit_price }}.




## Info
Current working directory is `{{ cwd }}`.

**Project directory**: `{{ special_docs_dir or "NOT FOUND" }}`

**Project directory**: `{{ config.docs_dir }}`

### Git version:
{{ git.short_commit }} ({{ git.date }})

{{ git.date.strftime("%b %d, %Y %H:%M:%S") }}


({{ git.non_existent or now() }})

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


## Button

This is a:

{{ button ("Try this", 'https://squidfunk.github.io/mkdocs-material')}}

## Included file

{% include 'foo.md' %}


## Access meta information in the page

Here is the content of the meta vars:

{{ context(page.meta) | pretty }}

### Dot notation 
We have **{{ page.meta.bottles.whine }}** bottles of whine and
**{{ page.meta.bottles.beer }}** bottles of beer
{% raw %} 
(respectively: `{{ page.meta.bottles.whine }}` 
and `{ page.meta.bottles.whine }}`).
{% endraw %}

### List of bottles
{% for bottle, quantity in page.meta.bottles.items() %}
1. {{ bottle }}: {{ bottle }}
{% endfor %}
