# --------------------------------------------
# Main part of the plugin
# Defines the VariablesPlugin class
#
# Laurent Franceschetti (c) 2018
# MIT License
# --------------------------------------------

import os, traceback
from copy import copy

import yaml
from jinja2 import Environment, FileSystemLoader



from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type as PluginType

from .util import trace, update, SuperDict, import_module
from .context import define_env

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
    J2_STRING = PluginType(str, default='')
    config_scheme = (
        # main python module:
        ('module_name',  PluginType(str, 
                                    default=DEFAULT_MODULE_NAME)),
        # include directory for templates ({% include ....%}):
        ('include_dir',  J2_STRING),
        # list of additional yaml files:
        ('include_yaml', PluginType(list, default=[])),
        # for altering the j2 markers, in case of need:
        ('j2_block_start_string',    J2_STRING),
        ('j2_block_end_string',      J2_STRING),
        ('j2_variable_start_string', J2_STRING),
        ('j2_variable_end_string',   J2_STRING)
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
        return os.path.dirname(os.path.abspath(CONFIG_FILE))


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
        module_name = self.config['module_name']
        trace("Project dir '%s'" %  self.project_dir)
        module = import_module(self.project_dir, module_name)
        if module:
            trace("Found external Python module '%s' in:" % module_name,
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
                        "(see documentation)!" % module_name)
                function_found = True
            if not function_found:
                raise NameError("No valid function found in module '%s'" %
                                module_name)
        else:
            if module_name == DEFAULT_MODULE_NAME:
                # do not do anything if there is no main module
                # trace("No module")
                pass
            else:
                raise ImportError("Macro plugin could not find custom '%s' "
                                "module in '%s'." %
                                (module_name, self.project_dir))



    def render(self, markdown):
        """
        Render a page through jinja2: it executes the macros
        Must be run after on_config()

        Returns a pure markdown/HTML page.
        """
        try:
            md_template = self.env.from_string(markdown)
            # Execute the jinja2 template and return
            return md_template.render(**self.variables)
        except Exception as e:
            output = ["# _Macro Rendering Error_",
                        "",
                        "**%s**: %s" % (type(e).__name__, e),
                        "", "",
                        "```",
                        traceback.format_exc(),
                        "```"]
            error = "\n".join(output) 
            trace("ERROR", error)
            return error


    # ----------------------------------
    # Standard Hooks for a mkdocs plugin
    # ----------------------------------

    def on_config(self, config):
        """
        Called once (initialization)
        From the configuration file, builds a Jinj2 environment
        with variables, functions and filters.
        """
        # WARNING: this is not the config argument:
        trace("Macros arguments:", self.config)
        # define the variables as a plain dictionary
        # (for update function to work):
        self._variables = SuperDict()

        # load the extra variables
        extra = dict(config.get(YAML_VARIABLES))
        # make a copy for documentation:
        self.variables['extra'] = extra 
        # actual variables (top level will be loaded later)

        # export the whole data, in case of need:
        self._conf = config
        # add a copy to the template variables
        # that copy may be manipulated
        self.variables['config'] = copy(config)
        assert self.variables['config'] is not config

        # load other yaml files
        self._load_yaml()

        # load the standard plugin context
        define_env(self)

        # at this point load the actual variables from extra (YAML file)
        self.variables.update(extra)
        

        # add variables, functions and filters from the Python module:
        # by design, this MUST be the last step, so that programmers have
        # full control on what happened in the configuration files
        self._load_module()
        # Provide information:
        trace("Variables:", list(self.variables.keys()))
        trace("Extra variables (config file):", extra)
        trace("Filters:", self.filters)
        

        # -------------------
        # Create the jinja2 environment:
        # -------------------
        DOCS_DIR = config.get('docs_dir')
        trace("Docs directory:", DOCS_DIR)
        # define the include directory:
        # NOTE: using DOCS_DIR as default is not ideal,
        # because those files get rendered as well, which is incorrect
        # since they are partials; but we do not want to break existing installs
        include_dir = self.config['include_dir'] or DOCS_DIR
        if not os.path.isdir(include_dir):
            raise FileNotFoundError("MACROS ERROR: Include directory '%s' "
                                    "does not exist!" %
                                        include_dir)
        trace("Includes directory:", include_dir)
        # will contain all parameters:
        env_config = {
            'loader': FileSystemLoader(include_dir)
        }
        # read the config variables for jinja2:
        for key, value in self.config.items():
            # take definitions in config_scheme where key starts with 'j2_'
            # (if value is not empty) 
            # and forward them to jinja2
            # this is used for the markers
            if key.startswith('j2_') and value:
                variable_name = key.split('_', 1)[1] # remove prefix
                trace("Found j2 variable '%s': '%s'" %
                            (variable_name, value))
                env_config[variable_name] = value
        
        # finally build the environment:
        self.env = Environment(**env_config)

        # -------------------
        # Process filters
        # -------------------
        # reference all filters, for doc [these are copies, so no black magic]
        # NOTE: self.variables is reflected in the list of variables
        #       in the jinja2 environment (same object)
        self.variables['filters'] = copy(self.filters) 
        self.variables['filters_builtin'] = copy(self.env.filters) 
        # update environment with the custom filters:
        self.env.filters.update(self.filters)


    def on_nav(self, nav, config, files):
        """
        Called after the site navigation is created.
        Capture the nav and files objects so they can be used by
        templates.
        """
        # nav has useful properties like 'pages' and 'items'
        # see: https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/nav.py
        self.variables['navigation'] = nav
        # files has collection of files discovered in docs_dir
        # see: https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/files.py
        # NOTE: this is not implemented, because it is unclear how to exploit that information
        # self.variables['files'] = files
        
        
    def on_serve(self, server, config, **kwargs):
        """
        Called when the serve command is used during development.
        This is to add files or directories to the list of "watched" 
        files for auto-reloading.
        """
        # define directories to add, keep non nulls
        additional = [self.config['include_dir'] # markdown includes
                     ]
        additional = [el for el in additional if el]
        trace("We will also watch: %s" % additional)
        # necessary because of a bug in mkdocs:
        # more information in:
        # https://github.com/mkdocs/mkdocs/issues/1952))
        builder = list(server.watcher._tasks.values())[0]["func"]
        # go ahead and watch
        for el in additional:
            if el:
                server.watch(el, builder)        


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
            # Update the page info in the document
            # page is an object with a number of properties (title, url, ...)
            # see: https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/pages.py
            self.variables["page"] = page
            return self.render(markdown)
