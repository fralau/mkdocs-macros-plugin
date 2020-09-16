# This is a title

It costs {{ unit_price }}.

## Button

This is a:

{{ button ("Try this", 'https://squidfunk.github.io/mkdocs-material')}}

## Info
Current working directory is '{{ cwd }}'.

**Project directory**: {{ special_docs_dir or "NOT FOUND" }}

**Project directory**: {{ config.docs_dir }}

### Git version:
{{ git.short_commit }} ({{ git.date }})

{{ git.date.strftime("%b %d, %Y %H:%M:%S") }}


({{ git.non_existent or now() }})

### Page
Page: {{ page }}

Date: {{ now().year }} {{ now().month }}



## Included file

{% include 'foo.md' %}
