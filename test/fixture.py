"""
Specific for MkDocs Projects

(C) Laurent Franceschetti 2024
"""

import warnings
import json
import subprocess


from super_collections import SuperDict
from mkdocs_test import DocProject, MkDocsPage


class MacrosPage(MkDocsPage):
    "Specific for MkDocs-Macros"

    def has_error(self:MkDocsPage):
            "Predicate: check whether the page has an error"
            return self.find('Macro Rendering Error')
    @property
    def is_rendered(self):
        "Accomodate earlier formulation"
        warnings.warn("The page property `.is_rendered` is DEPRECATED "
                      "use `.is_markdown_rendered()` instead.", 
                      UserWarning, stacklevel=2)
        return self.is_markdown_rendered()

class MacrosDocProject(DocProject):
    "Specific for MkDocs-Macros"

    def build(self, strict:bool=False) -> subprocess.CompletedProcess:
        """
        Build the documentation, to perform the tests
        Verbose is forced to True, to get the variables, functions and filters
        """
        super().build(strict=strict, verbose=True)

    @property
    def pages(self) -> dict[MacrosPage]:
        "List of pages"
        pages = super().pages
        return {key: MacrosPage(value) for key, value in pages.items()}
    

    
    @property
    def macros_plugin(self):
         "Information on the plugin"
         return self.get_plugin('macros')
    
    # ------------------------------------
    # Get information through the payload
    # ------------------------------------
    @property
    def variables(self):
         "Return the variables"
         try:
              return self._variables
         except AttributeError:
            entry = self.find_entry("config variables",
                                          source='macros',
                                          severity='debug')
            if entry and entry.payload:
                self._variables = SuperDict(json.loads(entry.payload))
            else:
                 print(entry)
                 raise ValueError("Cannot find variables")
            return self._variables


    @property
    def macros(self):
         "Return the macros"
         try:
              return self._macros
         except AttributeError:
            entry = self.find_entry("config macros",
                                          source='macros',
                                          severity='debug')
            if entry and entry.payload:
                self._macros = SuperDict(json.loads(entry.payload))
            else:
                 print(entry)
                 raise ValueError("Cannot find macros")
            return self._macros
         

    @property
    def filters(self):
         "Return the filters"
         try:
              return self._filters
         except AttributeError:
            entry = self.find_entry("config filters",
                                          source='macros',
                                          severity='debug')
            if entry and entry.payload:
                self._filters = SuperDict(json.loads(entry.payload))
            else:
                 print(entry)
                 raise ValueError("Cannot find filters")
            return self._filters
