"""
Specific for MkDocs Projects

(C) Laurent Franceschetti 2024
"""

import warnings
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

    @property
    def pages(self) -> dict[MacrosPage]:
        "List of pages"
        pages = super().pages
        return {key: MacrosPage(value) for key, value in pages.items()}
    
    @property
    def variables(self):
        "Alias for config.extra"
        return self.config.extra
    
    @property
    def macros_plugin(self):
         "Information on the plugin"
         return self.get_plugin('macros')
