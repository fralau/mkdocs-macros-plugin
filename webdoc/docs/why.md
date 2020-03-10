Why developing the macros plugin?
=================================

Sources of inspiration
----------------------

### mkdocs-markdownextradata (rosscdh)

The idea for that extension came to me after I saw the excellent plugin
[mkdocs-markdownextradata](https://github.com/rosscdh/mkdocs-markdownextradata-plugin)
created by rosscdh, which takes metadata data from the `mkdocs.yml`
file, and allows you to insert them with double curly brackets:

    The price of the item is {{ price }}.

His idea of using the [jinja2](http://jinja.pocoo.org/docs/2.10/)
templating engine for that purpose was simple and beautiful: all it took
for this plugin was a few lines of code.

### jinja2: variables can also be Python callables

I then discovered that the creators of jinja2, in their great wisdom
(thanks also to them!), had decided to support *any* kind of Python
variables, *including callables*, typically functions, e.g.:

    The price of the item is {{ calculate(2, 7.4) }}.

Perhaps they did not think it was worth more than a few words in their
documentation, but it was a diamond in plain sight.

> **Oh yeah?** So let's call Python functions from the markdown pages of
> MkDocs!

### Macros in Wiki engines

> **The idea of using 'macros' to speed up the process of writing web
> pages is in fact rather old**.

> Most wiki **engines**, which also rely on some
> [markup](http://wiki.c2.com/?MarkupLanguage) language, had the same
> issue of enriching the markup language of their pages, at the turn of
> the year 2000.

In response, they often implemented macros in one form or another (in
mediawiki, they were confusingly called
[templates](https://www.mediawiki.org/wiki/Help:Templates)). And in many
cases, these wiki engines already relied on the double-curly-braces
syntax.

After all, a **static website generator** can be defined as a wiki whose
online editing features have been removed, to make it "wiki-wikier"!

Use Case: Overcoming the Intrinsic Limitations of Markdown Syntax
-----------------------------------------------------------------

[MkDocs](https://www.mkdocs.org/) is a powerful, elegant and simple tool
for generating websites. Pages are based on **markdown**, which is
simple by design.

The power and appeal of markdown comes from its extreme simplicity.

> The downside of markdown's powerful simplicity is that its
> expressiveness necessarily limited.

> What do you do if you want to enrich markdown pages with features like
> buttons, fancy images, etc.?

### Solution 1: Markdown extensions

In order to express more concepts with markdown, one possible recourse
is to extend its through **standard** [markdown
extensions](https://python-markdown.github.io/extensions/). Adding
extensions to mkdocs is straightforward, since those extensions can be
directly activated through the `mkdocs.yml`configuration file of the
website e.g.:

``` {.yaml}
markdown_extensions:
    - footnotes
```

(If they are non-standard, you just have to install them first on your
machine.)

The problem is, however, that there will *always* be *something*
specific you will want to do, for which there is no markdown extension
available. Or the extension will be too complicated, or not quite what
you wanted.

Furthermore, the are limitations to the number of possible extensions,
because extending the grammar of markdown is always a little tricky.

Some markdown extensions could alter what you meant with the standard
markdown syntax (in other words, some markdown text you already wrote
could be accidentally reinterpreted); or it could be incompatible with
other extensions.

### Solution 2: Custom HTML Code

If don't have an extension, the standard recourse is to write some pure
HTML within your markdown, which may also contain some css code
(especially if you are using css that is specific to your theme or
website), e.g.:

``` {.html}
Here is my code:

<a class='button' href="http:your.website.com/page">Try this</a>
```

The combination of HTML and css works well and can solve a wide range of
issues.

But it will soon become tedious, if you have to type the same code again
and again with some variations; and if you want to change something to
the call (typically the css class), you will then have to manually
change *all* instances of that code, with all the related risks. This
solution doesn't scale.

### Solution 3: Enter Macros

What if you had a **macro** instead, that would allow you to write the
above HTML as:

    {{button('Try this', 'http:your.website.com/page')}}

... that call was translated into the proper HTML?

**That would be something you could teach to a person who can already
write markdown, without the need for them to get involved in *any* css
or HTML!**

And, what's more, you could *easily* (as a programmer) write your own
new macro in Python, whenever you needed one?

A **macro** is, simply stated, a *Python function* that takes a few
arguments and returns a string. It could contain all the logic you want;
it could be as simple as the example above, or as sophisticated as
making a query from a database and formatting the results as markdown.

All of this becomes possible, thanks to **mkdocs-macros-plugin**!
