# --------------------------------------------
# Inject functions from an external module
#
# It is kept outside the plugin.py file,
# so as to be testable (plugin.py does not run on its own)
#
# Laurent Franceschetti (c) 2018
# MIT License
# --------------------------------------------

import repackage, importlib
import os

DEFAULT_MODULE_NAME = 'main'



def load_variables(variables, config):
    """
    Add the template functions, via the python module
    located in the same directory as the Yaml config file.

    The python module must contain the following hook:

    declare_variables(variables, macro):

        variables['a'] = 5


        @macro
        def bar(x):
            ....

        @macro
        def baz(x):
            ....


    """

    def macro(v, name=''):
        """
        Registers a variable as a macro in the template,
        i.e. in the variables dictionary:

            macro(myfunc)

        Optionally, you can assign a different name:

            macro(myfunc, 'funcname')


        You can also use it as a decorator:

        @macro
        def foo(a):
            return a ** 2

        More info:
        https://stackoverflow.com/questions/6036082/call-a-python-function-from-jinja2
        """

        name = name or v.__name__
        variables[name] = v
        return v



    # determine the package name, from the filename:
    python_module = config.get('python_module') or DEFAULT_MODULE_NAME
    # get the directory of the yaml file:
    config_file = config['config_file_path']
    yaml_dir = os.path.dirname(config_file)
    # print("Found yaml directory: %s" % yaml_dir)

    # that's the directory of the package:
    repackage.add(yaml_dir)
    try:
        module = importlib.import_module(python_module)
        print("Found module '%s'" % python_module)
        # execute the hook, passing the template decorator function
        module.declare_variables(variables, macro)
    except ModuleNotFoundError:
        print("No module found.")


# -------------------
# Test
# -------------------
if __name__ == '__main__':
    from jinja2 import Template

    # simulation of the environment:
    markdown = """
{% set company = 'Acme company' %}
I say, {{foo}}. This is {{bar(5)}} and {{baz}} ({{barbaz(0.4)}}).
Please buy products from {{ company }}.
"""
    extra = {'foo': 'Hello world'}
    config = { # 'config file' is in this directory
               'config_file_path':'./mkdocs.yaml',
               # the extra variables:
               'extra':extra,
               # name of the main module:
               'python_module': 'test'}



    # Get the environment
    variables = config.get('extra')
    md_template = Template(markdown)

    # add the functions
    load_variables(md_template.globals, config)


    # Execute the template and return
    result = md_template.render(**variables)
    print("Sentence:", markdown)
    print("Result  :", result)
