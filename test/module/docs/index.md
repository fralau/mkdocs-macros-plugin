# This is a title

It costs {{ unit_price }}.

## Info
Current working directory is '{{ cwd }}'.
Project directory: {{ project_dir }}

### Git version:
{{ git.short_commit }} ({{ git.date }})

{{ git.date.strftime("%b %d, %Y %H:%M:%S") }}


({{ git.non_existent or now() }})

### Page
Page: {{ page }}

Date: {{ now().year }} {{ now().month }}



## Included file

{% include 'foo.md' %}
