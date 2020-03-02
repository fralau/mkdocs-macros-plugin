# Nav Example

## Pages

{% for p in nav.pages %}
* {{ p.title }}
{% endfor %}

## Files

{% for f in files %}
* {{ f.src_path }}
{% endfor %}