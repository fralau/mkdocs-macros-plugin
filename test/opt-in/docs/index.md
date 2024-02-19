# This is a test of opt-in with various mechanisms

**This is the case of opt-in, where `render_by_default` is set to
`false` in the config file.**


{# The jinja2 code in this index page should not be rendered
(since there must be an opt-in) #}

{{ macros_info() }}

