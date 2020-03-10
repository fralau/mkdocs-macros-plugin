### Troubleshooting
#### Error Information in case of module error
In principle a rendering error in a macro will not stop the server, but
display the error in the browser's page (as you would expect, e.g.
with php).
The terminal's running log also displays errors when they occur.

#### `macros_info()` as the go-to tool
Attempting to run the following line in a page:

```
{{ macros_info() }}
```

and restarting the server in the temrinal with `mkdocs serve` will usually give
you a wealth of information within the browser:

- If the information page appears (as e.g. phpinfo() for php),
  then you know that the plugin must be working. 
- If the page displays and an error message appears, then there
  may be a problem with the plugin's installation.
- If the page does not display at all, then the mkdocs server might not
  be running or there can be a problem running it.

#### Is there some function or variable for information XYZ?
If you cannot find an answer in this readme,
use `macros_info()` to display the information on all the variables,
functions and filters available in a page.

#### How can I get detailed debug information on an object?
For example, if you want to have more information on the `config` object:

```
{{ context('config') | pretty }}
```
(the `pretty` filter displays the result in a nice table form)

You can use this pattern for pretty much any object, even those
you declared in a module.

When used on its own, `context()` gives the general list of variables
in the plugin's environment:
```
{{ context() | pretty }}
```