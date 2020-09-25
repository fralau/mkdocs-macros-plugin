
# Test Page (Modules)

## Variable (defined in YAML file)
The total costs is {{ unit_price }} euros.

> The figure 50 should appear (`unit_price`), defined in config file).



## Variables (defined in the module)


> This was defined as variable `cwd` in `main.py`

**Current working directory**: `{{ cwd }}`.


## Macro (defined in module)

From the `button()` macro.

This is a:

{{ button ("Try this", 'https://squidfunk.github.io/mkdocs-material')}}

## Page
Page: {{ page }}

Date: {{ now().year }} {{ now().month }}






