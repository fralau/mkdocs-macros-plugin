Troubleshooting
===============

Before anything else
--------------------

!!! Important
    Make sure you you have the **last version** of mkdocs-macros.
    Perhaps the issue is already fixed?

    Also, check that your version of mkdocs is sufficiently up-to-date.


Error Information in case of module error
-----------------------------------------

In principle a rendering error in a macro will not stop the server, but
display the error in the browser's page (as you would expect, e.g. with
php). The terminal's running log also displays errors when they occur.

`macros_info()` as the go-to tool
---------------------------------

Adding following line in a page:

    {{ macros_info() }}

and restarting the server in the temrinal with `mkdocs serve` will
usually give you a wealth of information within the browser:

-   If the information page appears (as e.g. phpinfo() for php), then
    you know that the plugin must be working.
-   If the page displays and an error message appears, then there may be
    a problem either with the page or with the plugin's installation.
-   If the page does not display at all, then the mkdocs server might
    not be running or there can be a problem running it.



How can I get detailed debug information on an object?
------------------------------------------------------

For example, if you want to have more information on the `config`
object:

    {{ context('config') | pretty }}

(the `pretty` filter displays the result in a nice table form)

You can use this pattern for pretty much any object, even those you
declared in a module.

When used on its own, `context()` gives the general list of variables in
the plugin's environment:

    {{ context() | pretty }}


Help! mkdocs-macros is eating pieces of my documentation!
------------------------------------------------

The problem is that mkdocs-macros is believing that statements
of the form `\{\{ .... }}` or `{% ... %}` 
in your pages, which you want to appear in the HTML output,
are intended for it.

![dog eating ice-cream, credit: https://unsplash.com/photos/OYUzC-h1glg](../dog-eating.jpg)

This result is usually **an empty string where you expected one**.

For the solutions to that problem, see 
[how to prevent interpretation of Jinja-like
statements](../advanced/#how-to-prevent-interpretation-of-jinja-like-statements).





Where Can I get Help?
---------------------

Check the [issues](https://github.com/fralau/mkdocs_macros_plugin/issues) 
on the github repo.

!!! Tip
    Also check the **closed issues**. It could be that your issue
    has already been solved and closed!

    Also, you could check similar questions, to see if they could
    point you to the right questions.


Then, you want to add a new issue, or comment on an existing one,
you are more than welcome!

All issues are carefully reviewed and often get a quick answer.