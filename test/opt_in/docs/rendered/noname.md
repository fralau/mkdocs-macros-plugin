---
text: Hello world
times: 10
---

# Opt-in by directory

This page is rendered, because the `rendered/` path is
specified in the `mkdocs.yml` file,
and the original filename of this page is **`{{page.file.src_uri}}`**.


{% for n in range(times) %}
- {{ n }}: {{text}} 
{% endfor %}


