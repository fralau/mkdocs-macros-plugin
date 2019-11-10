# --------------------------------------------
# Main part of the plugin
# Defines the VariablesPlugin class
#
# Laurent Franceschetti (c) 2018
# MIT License
# --------------------------------------------

import os, importlib

import repackage
from mkdocs.plugins import BasePlugin
from jinja2 import Environment, FileSystemLoader

from termcolor import colored

from .module_reader import load_module

# The subset of the YAML file that will be used for the variables:
YAML_SUBSET = 'extra'
DEFAULT_MODULE_NAME = 'main'


def trace(*args, **kwargs):
    "General purpose print function, with first item emphasized"
    COLOR = 'green'
    first = args[0]
    rest = args[1:]
    emphasized = colored("[macros] " + first, COLOR)
    print(emphasized, *rest, **kwargs)


class MacrosPlugin(BasePlugin):
    """
    Inject config 'extra' variables into the markdown
    plus macros / variables defined in external module.

    The python code is located in 'main.py' or in a 'main' package
    in the root directory of the website
    (unless you want to redefine that name in the 'python_module' value
    in the mkdocs.yml file)
    """

    # ------------------------------------------------
    # These properties are available in the env object
    # ------------------------------------------------
    @property
    def variables(self):
        "The list of variables"
        try:
            return self._variables
        except AttributeError:
            return None

    @property
    def filters(self):
        "The list of variables"
        try:
            return self._filters
        except AttributeError:
            self._filters = {}
            return self._filters

    @property
    def conf(self):
        """
        Content of the whole config file (by default: mkdocs.yml)

        This property may be useful if the code in the module needs to access
        general configuration information.
        """
        return self._conf


    def macro(self, v, name=''):
        """
        Registers a variable as a macro in the template,
        i.e. in the variables dictionary:

            env.macro(myfunc)

        Optionally, you can assign a different name:

            env.macro(myfunc, 'funcname')


        You can also use it as a decorator:

        @env.macro
        def foo(a):
            return a ** 2

        More info:
        https://stackoverflow.com/questions/6036082/call-a-python-function-from-jinja2
        """

        name = name or v.__name__
        self.variables[name] = v
        return v


    def filter(self, v, name=''):
        """
        Registers a variable as a macro in the template,
        i.e. in the variables dictionary:

            env.filter(myfunc)

        Optionally, you can assign a different name:

            env.filter(myfunc, 'filtername')


        You can also use it as a decorator:

        @env.filter
        def reverse(x):
            "Reverse a string (and uppercase)"
            return x.upper().[::-1]

        See: https://jinja.palletsprojects.com/en/2.10.x/api/#custom-filters
        """

        name = name or v.__name__
        self.filters[name] = v
        return v


    # ------------------------------------------------
    # Initialization
    # ------------------------------------------------
    def load_module(self, config):
        """
        Add the template functions, via the python module
        located in the same directory as the Yaml config file.

        This function enriches the variables dictionary

        The python module must contain the following hook:

        declare_env(env):
            "Declare environment for jinja2 templates for markdown"

            env.variables['a'] = 5

            @env.macro
            def bar(x):
                ...

            @env.macro
            def baz(x):
                ...

            @env.filter
            def foobar(x):
                ...

        """


        # fetch variables from YAML file:
        self._conf = config # export the whole file, in case of need
        self._variables = config.get(YAML_SUBSET)

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
            trace("Found external Python module '%s' in:" % python_module,
                    yaml_dir)
            # execute the hook, passing the template decorator function
            function_found = False
            if hasattr(module, 'define_env'):
                module.define_env(self)
                function_found = True
            if hasattr(module, 'declare_variables'):
                module.declare_variables(self.variables, self.macro)
                function_found = True
            if not function_found:
                raise NameError("No valid function found in module '%s'" %
                                config_file)
        except ImportError:
            raise ImportError("Macro plugin could not find custom '%s' "
                              "module in '%s'." %
                             (python_module, yaml_dir))



    # ----------------------------------
    # Standard Hooks for a mkdocs plugin
    # ----------------------------------
    def on_config(self, config):
        """
        Called once (initialization)
        Provide a hook for defining variables, functions and filters
        from an external module
        """

        # the docs_dir directory (default: 'docs')
        DOCS_DIR = config.get('docs_dir')
        trace("Docs directory:", DOCS_DIR)

        # add variables and functions from the module:
        self.load_module(config)

        trace("Variables:", self.variables)
        trace("Filters:", self.filters)

        env_config = {
            'loader': FileSystemLoader(DOCS_DIR)
        }
        self.env = Environment(**env_config)
        self.env.filters = self.filters


    def on_page_markdown(self, markdown, page, config,
                          site_navigation=None, **kwargs):
        """
        Rendering of each page
        """

        # the site_navigation argument has been made optional
        # (deleted in post 1.0 mkdocs, but maintained here
        # for backward compatibility)

        if not self.variables:
            return markdown

        else:

            # Create template and get the variables
            md_template = self.env.from_string(markdown)

            # Execute the jinja2 template and return
            return md_template.render(**self.variables)
