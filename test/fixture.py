"""
Fixtures for the testing of Mkdocs-Macros (pytest)
This program must be in the test directory.

This is the two classes:

- MacrosDocProject
- TestMarkdownPage
 

(C) Laurent Franceschetti 2024
"""

import os
from dataclasses import dataclass, field
from typing import List
import json
from typing import Any, List


from super_collections import SuperDict

from .fixture_util import list_markdown_files, find_after
from .docproject import (MarkdownPage, DocProject, REF_DIR, 
                         DOCS_DEFAULT_DIRNAME)

# not used in the code here, but necessary for the tests
from .docproject import PROJECTS, parse_log



# ---------------------------
# The Macros Doc project
# ---------------------------

"The directory containing the macros rendered"
RENDERED_MACROS_DIRNAME = '__docs_macros_rendered'

"The error string"
MACRO_ERROR_STRING = '# _Macro Rendering Error_'

@dataclass
class TestMarkdownPage(MarkdownPage):
    "A subclass of markdown page, for MkDocs-Macros purposes"

    "The source markdown page (before the rendering of macros)"
    source_page: MarkdownPage = field(init=False)

    "The source doc dir (normally the docs dir)"
    source_doc_dir: str = DOCS_DEFAULT_DIRNAME

    # "Difference of the source"
    # diff_markdown: str = field(init=False)


    def __post_init__(self):
        "Additional actions after the rest"
        super().__post_init__()
        self.source_page = MarkdownPage(self.filename, 
                                        project_dir=self.project_dir,
                                        doc_dir=self.source_doc_dir)
        # this should be the case, always, or something is wrong
        assert self.filename == self.source_page.filename
        assert self.metadata == self.source_page.metadata


    @property
    def has_error(self) -> bool:
        "Checks whether there is an error"
        return self.markdown.startswith(MACRO_ERROR_STRING)

    @property
    def is_rendered(self) -> bool:
        """
        "Rendered" means that the target markdown 
        is different from the source;
        more accurately, that the source markdown is not 
        contained in the target markdown.

        Hence "not rendered" is a "nothing happened". 
        It covers these cases: 
        1. An order to render was given, but there where actually 
           NO jinja2 directives.
        2. A jinja2 rendering has not taken place at all
           (some order to exclude the page).
        3. A header and/or footer were added (in `on_pre_page_macros()
            or in `on_post_page_macro()`) but the text itself
            was not modified. 
        """
        # make sure that the source is stripped, to be sure.
        return self.source_page.markdown.strip() not in self.markdown
    

    def __repr__(self):
        """
        Important for error printout
        """
        return f"Markdown page ({self.filename}):\n{self.text}"




class MacrosDocProject(DocProject):
    """
    An object that describes the current MkDocs-Macros project
    being tested.

    The difference is that it relies heavily on the Markdown
    pages rendered by Jinja2. These are produced at the end of
    the `on_page_markdown()` method of the plugin.

    The pages() property has thus been redefined.
    """


    @property
    def target_doc_dir(self):
        "The target directory of markdown files (rendered macros)"
        return os.path.join(REF_DIR, 
                            self.project_dir, 
                            RENDERED_MACROS_DIRNAME)

    @property
    def pages(self) -> List[TestMarkdownPage]:
        """
        The list of Markdown pages produced by the build.
        It must be called after the build.
        """
        try:
            return self._pages
        except AttributeError:
            # Make the list and 
            full_project_dir = os.path.join(REF_DIR, self.project_dir)
            full_target_dir = os.path.join(REF_DIR, self.target_doc_dir)
            self._pages = [TestMarkdownPage(el, 
                            project_dir = full_project_dir,
                            doc_dir=RENDERED_MACROS_DIRNAME,
                            source_doc_dir=DOCS_DEFAULT_DIRNAME
                            ) 
                            for el in list_markdown_files(full_target_dir)]
            return self._pages
    
    @property
    def macros_plugin(self) -> SuperDict:
        "Return the plugin config"
        return self.get_plugin('macros')
    

    # ----------------------------------
    # Smart properties (from log, etc.)
    # ----------------------------------
    @property
    def modules(self) -> List[str]:
        "List of modules imported (from the log)"
        entries = self.find_entries('external Python module')
        l = []
        # word between quotes:
        PATTERN = r"'([^']*)'"
        for entry in entries:
            module_name = find_after(entry.title, 'module', PATTERN)
            if module_name:
                l.append(module_name)
        return l
    
    @property
    def variables(self) -> SuperDict:
        """
        List of all variables, at the moment of on_config (from the log)

        We have the data as the payload of a DEBUG entry
        called "config variables".
        """
        entry = self.find_entry('config variables', severity='debug')
        return SuperDict(json.loads(entry.payload))
    

    
    @property
    def macros(self) -> SuperDict:
        """
        List of all macros, at the moment of on_config (from the log))

        We have the data as the payload of a DEBUG entry
        called "config macros".
        """
        entry = self.find_entry('config macros', severity='debug')
        if entry and entry.payload:
            return SuperDict(json.loads(entry.payload))
    
    @property
    def filters(self) -> SuperDict:
        """
        List of all filters, at the moment of on_config (from the log)

        We have the data as the payload of a DEBUG entry
        called "config filters".
        """
        entry = self.find_entry('config filters', severity='debug')
        if entry and entry.payload:
            return SuperDict(json.loads(entry.payload))