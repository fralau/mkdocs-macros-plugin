{#
Template for the macro_info() command
(C) SettleNext 2019
#}


# Macros Plugin Environment

## General List
All available variables and filters within the macros plugin:
{{ context() | pretty }}

## Config Information
Standard mkdocs configuration information. Do not try to modify.

e.g. {{ "`{{ config.docs_dir }}`" }}

See also the [MkDocs documentation on the config object](https://www.mkdocs.org/user-guide/custom-themes/#config).

{{ context(config)| pretty }}

## Page Attributes
Provided by mkdocs. These attributes change for every page.

e.g. {{ "`{{ page.title }}`" }}

See also the [MkDocs documentation on the page object](https://www.mkdocs.org/user-guide/custom-themes/#page).


{{ context(page)| pretty }}




## Plugin Filters
These filters are provided as a standard by the macros plugin.
{{ context(filters)| pretty }}

## Builtin Jinja2 Filters
These filters are provided by Jinja2 as a standard.

See also the [Jinja2 documentation on builtin filters](https://jinja.palletsprojects.com/en/2.11.x/templates/#builtin-filters)).

{{ context(filters_builtin) | pretty }}
