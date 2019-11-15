# --------------------------------------------
# Main part of the plugin
# Defines the VariablesPlugin class
#
# Laurent Franceschetti (c) 2018
# MIT License
# --------------------------------------------

import os, importlib

import repackage
import yaml
from jinja2 import Environment, FileSystemLoader



from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type as PluginType
from mkdocs.utils import string_types

from .util import trace, update


# ------------------------------------------
# Initialization
# ------------------------------------------

# The subsets of the YAML file that will be used for the variables:
YAML_VARIABLES  = 'extra'

# The default name of the Python module:
DEFAULT_MODULE_NAME = 'main' # main.py

# ------------------------------------------
# Plugin
# ------------------------------------------
class MacrosPlugin(BasePlugin):
    """
    Inject config 'extra' variables into the markdown
    plus macros / variables defined in external module.

    The python code is located in 'main.py' or in a 'main' package
    in the root directory of the website
    (unless you want to redefine that name in the 'python_module' value
    in the mkdocs.yml file)
    """

    # what is under the 'macros' namespace (will go into the config property):
    config_scheme = (
        ('module_name', PluginType(string_types, default=DEFAULT_MODULE_NAME)),
        ('include_yaml', PluginType(list, default=[]))
    )


    # ------------------------------------------------
    # These properties are available in the env object
    # ------------------------------------------------
    @property
    def conf(self):
        """
        Dictionary containing of the whole config file (by default: mkdocs.yml)

        This property may be useful if the code in the module needs to access
        general configuration information.

        NOTE: this property is called 'conf', because there is already
              a 'config' property in a BasePlugin object,
              which is the data connected to the macros plugin
              (in the yaml file)
        """
        try:
            return self._conf
        except AttributeError:
            raise AttributeError("Conf property of macros plugin "
                                 "was called before it was initialized!")


    @property
    def variables(self):
        "The cumulative list of variables, initialized by on_config()"
        try:
            return self._variables
        except AttributeError:
            raise AttributeError("Property called before on_config()")


    @property
    def filters(self):
        "The list of filters defined in the module, initialized by on_config()"
        try:
            return self._filters
        except AttributeError:
            self._filters = {}
            return self._filters


    @property
    def project_dir(self):
        "The directory of project"
        # we calculate it from the configuration file
        CONFIG_FILE = self.conf['config_file_path']
        return os.path.dirname(CONFIG_FILE)


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
        Register a filter in the template,
        i.e. in the filters dictionary:

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


    # ----------------------------------
    # load elements
    # ----------------------------------

    def _load_yaml(self):
        "Load the the external yaml files"
        for el in self.config['include_yaml']:
            # get the directory of the yaml file:
            filename = os.path.join(self.project_dir, el)
            if os.path.isfile(filename):
                with open(filename) as f:
                    # load the yaml file
                    # NOTE: for the SafeLoader argument, see: https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
                    content = yaml.load(f, Loader=yaml.SafeLoader)
                    trace("Loading yaml file:", filename)
                    update(self.variables, content)
            else:
                trace("WARNING: YAML configuration file was not found!",
                    filename)

    def _load_module(self):
        """
        Add variables and functions to the config dictionary,
        via the python module
        (located in the same directory as the Yaml config file).

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
        config = self.conf

        # determine the package name, from the filename:
        python_module = self.config['module_name']

        repackage.add(self.project_dir)
        try:
            module = importlib.import_module(python_module)
            trace("Found external Python module '%s' in:" % python_module,
                    self.project_dir)
            # execute the hook, passing the template decorator function
            function_found = False
            if hasattr(module, 'define_env'):
                module.define_env(self)
                function_found = True
            if hasattr(module, 'declare_variables'):
                module.declare_variables(self.variables, self.macro)
                trace("You are using declare_variables() in the python "
                      "module '%s'. Prefer the define_env() function "
                      "(see documentation)!" % python_module)
                function_found = True
            if not function_found:
                raise NameError("No valid function found in module '%s'" %
                                config_file)
        except ImportError:
            raise ImportError("Macro plugin could not find custom '%s' "
                              "module in '%s'." %
                             (python_module, self.project_dir))



    # ----------------------------------
    # Standard Hooks for a mkdocs plugin
    # ----------------------------------
    def on_config(self, config):
        """
        Called once (initialization)
        From the configuration file, builds a Jinj2 environment
        with variables, functions and filters.
        """
        trace("Macros arguments:", self.config)
        # define the variables as a plain dictionary
        # (for update function to work):
        self._variables = dict(config.get(YAML_VARIABLES))

        # export the whole data, in case of need:
        self._conf = config

        # load other yaml files
        self._load_yaml()

        # add variables, functions and filters from the Python module:
        # by design, this MUST be the last step, so that programmers have
        # full control on what happened in the configuration files
        self._load_module()
        # Provide information:
        trace("Variables:", self.variables)
        trace("Filters:", self.filters)

        # Create the jinja2 environment:
        DOCS_DIR = config.get('docs_dir')
        trace("Docs directory:", DOCS_DIR)
        env_config = {
            'loader': FileSystemLoader(DOCS_DIR)
        }
        self.env = Environment(**env_config)
        self.env.filters = self.filters


    def on_page_markdown(self, markdown, page, config,
                          site_navigation=None, **kwargs):
        """
        Pre-rendering for each page of the website.
        It uses the jinja2 directives, together with
        variables, macros and filters, to create pure markdown code.
        """
        # the site_navigation argument has been made optional
        # (deleted in post-1.0 mkdocs, but maintained here
        # for backward compatibility)
        if not self.variables:
            return markdown
        else:
            # Create template and get the variables
            md_template = self.env.from_string(markdown)
            # Execute the jinja2 template and return
            return md_template.render(**self.variables)
