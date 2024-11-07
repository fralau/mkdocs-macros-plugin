# Main Page

{{ greeting }}

{{ macros_info() }}

## Testing built-in filters

The result is: {{ (-35.0/2) | abs }}

{% set testing = 'hello world' %}

Saying: {{ greeting | upper }}

The length is: {{ greeting | length }}