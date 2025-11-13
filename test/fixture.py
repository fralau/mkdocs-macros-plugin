"""
Specific for MkDocs Projects

(C) Laurent Franceschetti 2024
"""

import os
import warnings
import json
import subprocess
from typing import Dict


from super_collections import SuperDict
from mkdocs_test import DocProject, MkDocsPage
import os

class MacrosPage(MkDocsPage):
    "Specific for MkDocs-Macros"

    def has_error(self:MkDocsPage):
            "Predicate: check whether the page has an error"
            return self.find_text('Macro Rendering Error')
    
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
     def pages(self) -> Dict[str, MacrosPage]:
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
                    print("ENTRIES:", self.find_entries("config variables",
                                                  source='',
                                                  severity='debug'))
                    print("ENTRIES:", self.find_entries("config variables",
                                                  source='macros'))
                    entry = self.find_entry("config variables",
                                                  source='macros',
                                                  severity='debug')
                    if entry and entry.payload:
                         payload = json.loads(entry.payload)
                         self._variables = SuperDict(payload)
                    else:
                         # print(entry)
                         # raise ValueError("Cannot find variables")
                         self._variables = {}
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
                    # print(entry)
                    # raise ValueError("Cannot find macros")
                    self._macros = {}
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
                    #   print(entry)
                    #   raise ValueError("Cannot find filters")
                    self._filters = {}
               return self._filters
     
     # ------------------------------------
     # Special operations
     # ------------------------------------

     def add_file(self, pathname:str, content, binary=False) -> str:
          """
          Stores a file (any type) into the directory structure,
          relative to project directory.

          If you want to add a source page (markdown), prefer the
          add_source_page() method.

          Return the full pathname.
          """
          full_pathname = os.path.join(self.project_dir, pathname)
          # Ensure parent directory exists
          os.makedirs(os.path.dirname(full_pathname), exist_ok=True)
          if binary:
               with open(full_pathname, 'wb') as f:
                    f.write(content)
          else:
               with open(full_pathname, 'w', encoding="utf-8") as f:
                    f.write(content)
          return full_pathname