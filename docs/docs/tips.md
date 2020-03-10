Tips and Tricks
===============

Is there some function or variable for information XYZ?
-------------------------------------------------------

If you cannot find an answer in this readme, use `macros_info()` to
display the information on all the variables, functions and filters
available in a page.

How can I create a button?
--------------------------

See [Example](../python/#example-creating-a-button-macro)


How can I access git data?
--------------------------

Providing of course the site is under a git repository, 
information is provided out of the box in a page, through the `git` 
variable.

To have the full string (corresponding to `git log -1` on the command line):


    {{ git.raw }}



To have, e.g. the short hash of the last commit, the date and the author:

    {{ git.short_commit}} ({{ git.date}}) by {{ git.author}}

To explore all elements of the git object:

    {{ context(git)| pretty }}