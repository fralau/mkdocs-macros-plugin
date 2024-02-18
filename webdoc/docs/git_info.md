# Using Git Information

## Introduction

A frequent requirement for the documentation of software projects,
is to insert version information. Nowadays, the tool of choice for
version control is [git](https://git-scm.com/).

Several specific plugins exist, this comes out of the box with mkdocs-macros.
Plus, covers a wide range of use cases, from the simplest to more
complicated ones.

## How to access

Providing of course the site is under a git repository, 
information is provided out of the box in a page, through the `git` 
variable.

To have the full string (corresponding to `git log -1` on the command line):


    {{ git.raw }}

To have, e.g. the short hash of the last commit, the date and the author:

    {{ git.short_commit}} ({{ git.date}}) by {{ git.author}}


For the date, you may use the standard Python methods, e.g.
[`strftime()`](https://docs.python.org/3.7/library/datetime.html#datetime.date.strftime):

    {{ git.date.strftime("%b %d, %Y %H:%M:%S") }}


!!! Tip "Testing for the presence of git repo"
    If the plugin cannot find the git executable, 
    or if the page is not in a
    git repository, then `git.status` is set to False.

    If you want to print git information only if applicable:

        {% if git.status %}
        Git: {{ git.short_commit }}
        {% endif %}

    If the page is indeed in a git repo, but `git.status`
    is still False, try displaying `{{ git.error }}`


## Catalogue
Here is a list of attributes of the git object:


| Attribute         | Description                                    |
|-------------------|------------------------------------------------|
| `short_commit`    | short hash of the last commit (e.g. _2bd7950_) |
| `commit`          | long hash of the last commit                   |
| `author`          | author's name                                  |
| `author_email`    | author's email                                 |
| `committer`       | committer's name                               |
| `committer_email` | committer's email                              |
| `tag`             | last active tag of the repo                    |
| `short_tag`       | last active tag of the repo, abbreviated       |
| `date`            | full date of the commit (as a date object)     |
| `date_ISO`        | full date of the commit (as an ISO string)     |
| `message`         | full message of the last commit                |
| `raw`             | string description of the last commit          |
| `root_dir`        | root dir of the git repository                 |
| `status`          | is git present?                                |

!!! Note
    Most of the time, you might be interested in the author's information.
    For more information on the difference between author and committer, see the [Pro Git Book, chapter 2.3](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History.)

!!! Tip
    To get the full list all attributes of the git object:

        {{ context(git)| pretty }}

## Date of the last commit

In order to obtain a printout of the date of the last commit, you can use:

    {{ git.date }}

which would return e.g.:

    2020-05-13 16:08:52+02:00

!!! Note
    For the commit dates (`date` and `date_ISO`) the common sense choice has been to use 
    git's _committer date_, since that guarantees that if the commit has been
    modified (rebased, etc.), the date has been updated.

Since it is a [datetime](https://docs.python.org/3.8/library/datetime.html) 
object, you can also use any of the usual attributes
(`.year`, `.month`), as well as the 
[`strftime()`](https://docs.python.org/3.8/library/datetime.html#strftime-and-strptime-format-codes)
formatting
method, e.g.:

    {{ git.date.strftime("%b %d, %Y %H:%M:%S") }}

which would return e.g.

    May 13, 2020 16:08:52        

## `tag` and `short_tag`

The tag attribute shows the full description of the tag, for
example `v1.0.4-14-g2414721`. Meanwhile, `short_tag` shows the
tag name without any suffix, for example `v1.0.4`. The later can
be useful when showing the latest release.

## Tip: Is this really a git repo?

In case you are not sure that there really is a git repo, you could use:

    {{ git.date or now() }}

Which would give you at least the build date for the static website.
Note that `now()` is also a datetime object.