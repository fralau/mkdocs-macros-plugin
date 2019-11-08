# --------------------------------------------
# Main part of the plugin
# Defines the VariablesPlugin class
#
# Laurent Franceschetti (c) 2018
# MIT License
# --------------------------------------------

from mkdocs.plugins import BasePlugin
from jinja2 import Environment, FileSystemLoader

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


    @property
    def variables(self):
        "The list of variables"
        try:
            return self._variables
        except AttributeError:
            return None

    def on_config(self, config):
        "Fetch the variables and functions"

        # the docs_dir directory (default: 'docs')
        DOCS_DIR = config.get('docs_dir')
        print("Docs directory:", DOCS_DIR)

        #print("Here is the config:", config)

        # fetch variables from YAML file:
        self._variables = config.get(YAML_SUBSET)

        # add variables and functions from the module:
        module_reader.load_variables(self._variables, config)

        print("Variables:", self.variables)

        env_config = {
            'loader': FileSystemLoader(DOCS_DIR)
        }
        self.env = Environment(**env_config)


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
            md_template = self.env.from_string(markdown)

            # Execute the jinja2 template and return
            return md_template.render(**self.variables)
