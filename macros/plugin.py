# --------------------------------------------
# Main part of the plugin
# Defines the VariablesPlugin class
#
# Laurent Franceschetti (c) 2018
# MIT License
# --------------------------------------------

from mkdocs.plugins import BasePlugin
from jinja2 import Environment
from mkdocs.config import config_options
from mkdocs import utils

from . import module_reader

# The subset of the YAML file that will be used for the variables:
YAML_SUBSET = 'extra'

# the list of variables (including functions) to be injected
variables = {}

class MacrosPlugin(BasePlugin):
    """
    Inject config 'extra' variables into the markdown
    plus macros / variables defined in external module.

    The python code is located in 'main.py' or in a 'main' package
    in the root directory of the website
    (unless you want to redefine that name in the 'python_module' value
    in the mkdocs.yml file)
    """

    config_scheme = (
        ('block_start_string', config_options.Type(utils.string_types, default='{%')),
        ('block_end_string', config_options.Type(utils.string_types, default='%}')),
        ('variable_start_string', config_options.Type(utils.string_types, default='{{')),
        ('variable_end_string', config_options.Type(utils.string_types, default='}}')),
    )

    @property
    def variables(self):
        "The list of variables"
        try:
            return self._variables
        except AttributeError:
            return None

    def on_config(self, config):
        "Fetch the variables and functions"
        #print("Here is the config:", config)

        # fetch variables from YAML file:
        self._variables = config.get(YAML_SUBSET)

        jinja_env_config = {
            'block_start_string': self.config['block_start_string'],
            'block_end_string': self.config['block_end_string'],
            'variable_start_string': self.config['variable_start_string'],
            'variable_end_string': self.config['variable_end_string'],
        }
        self.jinja_env = Environment(**jinja_env_config)

        # add variables and functions from the module:
        module_reader.load_variables(self._variables, config)

        print("Variables:", self.variables)


    def on_page_markdown(self, markdown, page, config,
                          site_navigation=None, **kwargs):
        "Provide a hook for defining functions from an external module"

        # the site_navigation argument has been made optional
        # (deleted in post 1.0 mkdocs, but maintained here
        # for backward compatibility)

        if not self.variables:
            return markdown

        else:

            # Create template and get the variables
            md_template = self.jinja_env.from_string(markdown)

            # Execute the jinja2 template and return
            return md_template.render(**self.variables)
