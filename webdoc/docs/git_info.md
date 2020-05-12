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

## Catalogue
Here is a list of attributes of the git object:

!!! Tip
    To explore all attributes of the git object:

        {{ context(git)| pretty }}

Attribute | Description
--- | --- 
`short_commit` | short hash of the last commit (e.g. _2bd7950_) 
`commit` | long hash of the last commit
`author` | author of the commit
`tag` | last active tage of the repo
`date` | full date of the commit (ISO format)
`message` | full message of the last commit
`raw` | string description of the last commit

