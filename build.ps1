rm -Recurse -Force .\build
rm -Recurse -Force .\dist
rm -Recurse -Force .\mkdocs_macros_plugin.egg-info

python setup.py sdist bdist_wheel