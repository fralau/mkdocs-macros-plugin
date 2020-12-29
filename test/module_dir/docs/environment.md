---
foo: "Hello world"
bar: 
    baz: 124
    barbaz: "See bar + baz"
---

{{ macros_info() }}


## Updates
{% for page in navigation.pages %}
1. {{ page.title }} ({{ page.update_date }})
{% endfor %}


# Navigation

{{ show_nav( )}}



