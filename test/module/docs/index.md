# This is a title

It costs {{ unit_price }}.

## Info
Current working directory is '{{ cwd }}'.
Project directory: {{ project_dir }}

Git version: {{ git_version }}

Page: {{ page }}

Date: {{ now().year }} {{ now().month }}

## Included file

{% include 'foo.md' %}
