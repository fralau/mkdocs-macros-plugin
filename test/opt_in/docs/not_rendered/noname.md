---
text: Hello world
times: 5
---

# This page must NOT be rendered

You should have some uninterpreted Jinja2 here.

This is because there is opt-in (`render_by_default` is set to `false`).


{% for n in range(times) %}
- {{ n }}: {{text}} 
{% endfor %}