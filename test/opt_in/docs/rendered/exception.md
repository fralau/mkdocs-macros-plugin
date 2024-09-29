---
render_macros: false # opt-out
---
# Opt-out by page header (priority)

{# This page should not be rendered #}

In theory, this page should be rendered because its source file
is in the `rendered/` directory.

However, it can be NEVER be rendered, because the variable `render_macros`
is set to `false` in the YAML header.

When it is set to `false`, it takes precedence over the directives
in the `force_render_paths` variable!

{{ macros_info() }}