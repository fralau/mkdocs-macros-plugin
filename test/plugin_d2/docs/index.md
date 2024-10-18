# Home

This checks the compatibility with the d2 plugin.

There used to be an issue, see [Github](https://github.com/fralau/mkdocs-macros-plugin/issues/249).

It was due to the CustomEncoder class (in util module),
which was susceptible to fail if an object was not printable.

```d2
A -> B
```
