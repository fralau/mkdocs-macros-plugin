---
foo: "Hello world"
bar: 
    baz: 124
    barbaz: "See bar + baz"
bingo: Hello
---

{{ macros_info() }}


## Updates
{% for page in navigation.pages %}
1. {{ page.title }} ({{ page.update_date }})
{% endfor %}


## Mkdocs.yaml file (portion)

```
{{ include_file('mkdocs.yml', 0, 5)}}
```

## List env object

```
{{ doc_env() | pprint }}
```