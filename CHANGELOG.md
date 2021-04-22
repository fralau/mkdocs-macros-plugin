# Changelog: mkdocs-macros

## 0.5.9, 2021-04-22

* Added: Changelog (Fixed #82)


## 0.5.8, 2021-04-21

* Fixed: display better message in case of macro syntax error 
    (line_no, message, incriminated line in file).
    Traceback was useless with that specific exception, and has been removed.

## 0.5.7, 2021-04-21

* Added: Possibility (for large projects) to exclude a markdown page 
    from macro rendering, with `ignore_macros: true` in YAML header
    (fixed issue #78, and answered discussion #79)

## 0.5.6, 2021-04-19

* Added: Files object to the mkdocs-macros environment (fixed #80)
* Fixed: Documentation errors or omissions
* Fixed: Do not install pluglet mkdocs-macros-test by default (#50)
    In order to do testing, 
    type: `pip install 'mkdocs-macros-plugin[test]'`

## 0.5.5, 2021-03-03

* Starting point