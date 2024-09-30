"""
Fixtures for the testing of Mkdocs-Macros (pytest)
This program must be in the test directory.

This is the two classes:

- DocProject
- TestMarkdownPage
 

(C) Laurent Franceschetti 2024
"""

import os
import yaml
import subprocess
import re
from dataclasses import dataclass, field
from typing import List
import json
from typing import Any, List



# from rich import print
from bs4 import BeautifulSoup


"A dictionary where the keys are also accessible with the dot notation"
from mkdocs_macros.util import SuperDict
from .fixture_util import (get_frontmatter, markdown_to_html, get_first_h1,
                find_in_html, find_after, list_markdown_files, find_page,
                run_command) 

# ---------------------------
# Initialization
# ---------------------------

"Command for build"
MKDOCS_BUILD = ['mkdocs', 'build']

"The directory of this file"
REF_DIR = os.path.dirname(os.path.abspath(__file__))

def list_doc_projects(directory:str):
    "Make the list of projects"
    # Specify the directory to start the search
    start_dir = directory
    mkdocs_dirs = []
    for entry in os.scandir(start_dir):
        if entry.is_dir():
            files_in_dir = os.listdir(entry.path)
            if 'mkdocs.yml' in files_in_dir or 'mkdocs.yaml' in files_in_dir:
                mkdocs_dirs.append(entry.name)
    return mkdocs_dirs


"All subdirectories containing mkdocs.yml"
PROJECTS = list_doc_projects(REF_DIR)

"The default docs directory"
DOCS_DEFAULT_DIRNAME = 'docs'



# ---------------------------
# Log parsing
# ---------------------------

@dataclass
class LogEntry(object):
    """
    Represents a log entry
    """
    
    "Severity (DEBUG, INFO, WARNING)"
    severity: str

    "Source, if available (e.g. [macros])"
    source: str = None

    "Title, first line"
    title: str = None

    "Payload, following lines"
    payload: str = None



def parse_log(mkdocs_log: str) -> list[LogEntry]:
    """
    Parse the log entries, e.g.:

        DEBUG   -  Running 1 `page_markdown` events
        INFO    -  [macros] - Rendering source page: index.md
        DEBUG   -  [macros] - Page title: Home
        WARNING -  [macros] - ERROR # _Macro Rendering Error_

        _File_: `second.md`

        _UndefinedError_: 'foo' is undefined

        ```
        Traceback (most recent call last):
        File "snip/site-packages/mkdocs_macros/plugin.py", line 665, in render
        DEBUG   -  Copying static assets.

    RULES:
    1. Every entry starts with a severity code (Uppercase).
    2. The message is then divided into:
        - source: between brackets, e.g. [macros]
        - title: the remnant of the first line, e.g. "Page title: Home"
        - payload: the rest of the message
    """
    log_entries = []
    current_entry = None
    mkdocs_log = mkdocs_log.strip()

    for line in mkdocs_log.split('\n'):
        match = re.match(r'^([A-Z]+)\s+-\s+(.*)', line)
        if match:
            if current_entry:
                log_entries.append(current_entry)
            severity = match.group(1)
            message = match.group(2)
            source_match = re.match(r'^\[(.*?)\]\s+-\s+(.*)', message)
            if source_match:
                source = source_match.group(1)
                title = source_match.group(2)
            else:
                source = ''
                title = message
            current_entry = {'severity': severity, 
                             'source': source, 
                             'title': title,
                             'payload': []}
        elif current_entry:
            # current_entry['payload'] += '\n' + line
            current_entry['payload'].append(line)
    if current_entry:
        log_entries.append(current_entry)

    # Transform the payloads into str:
    for entry in log_entries:
        entry['payload'] = '\n'.join(entry['payload']).strip()
    return [SuperDict(item) for item in log_entries]

# ---------------------------
# An Mkdocs Documentation project
# ---------------------------
@dataclass
class MarkdownPage(object):
    "A markdown page (rendered)"

    "The destination filename in the doc hierarchy"
    filename: str

    "Full path of the project directory"
    project_dir: str

    "Reference directory (name of directory where the page)"
    doc_dir: str

    "The full pathname of the file"
    full_filename: str = field(init=False)

    "The full content of the file"
    text: str = field(init=False)

    "The content of the file"
    markdown: str = field(init=False)

    "The front matter"
    frontmatter: str = field(init=False)

    "The metadata (the front-matter, interpreted)"
    metadata: SuperDict = field(init=False)

    "The HTML code (rendered, without frills)"
    html: str = field(init=False)

    "THe page rendered in plain text"
    plain_text: str = field(init=False)

    "First h1"
    h1: str| None = field(init=False)


    def __post_init__(self):
        self.full_filename = os.path.join(self.project_dir,
                                          self.doc_dir, self.filename)
        with open(self.full_filename, "r") as f:
            self.text = f.read()
        # Parse
        (self.markdown, 
         self.frontmatter, 
         self.metadata) = get_frontmatter(self.text)
        self.html = markdown_to_html(self.markdown)
        soup = BeautifulSoup(self.html, "html.parser")
        self.plain_text = soup.get_text()
        self.h1 = get_first_h1(self.markdown)


    def find(self, pattern: str, 
             header: str = None, header_level: int = None) -> str | None:
        """
        Find a text or regex pattern in the markdown page (case-insensitive).
        
        Arguments
        ---------
        - html: the html string
        - pattern: the text or regex
        - header (text or regex): if specified, it finds it first,
        and then looks for the text between that header and the next one
        (any level).
        - header_level: you can speciy it, if there is a risk of ambiguity.

        Returns
        -------
        The line where the pattern was found, or None
        """
        # it operates on the html
        return find_in_html(self.html,
                            pattern=pattern, 
                            header=header, header_level=header_level)



class DocProject(object):
    """
    An object that describes the current MkDocs project being tested
    (any plugin).
    """

    def __init__(self, directory:str=''):
        "Initialize"
        project_dir = os.path.join(REF_DIR, directory)
        if not os.path.isdir(project_dir):
            raise FileNotFoundError(f"Doc directory '{directory}' "
                                    "does not exist.")
        self._project_dir = project_dir
        # test existence of YAML file or fail
        self.config_file

    @property
    def project_dir(self) -> str:
        "The source directory of the MkDocs project (abs or relative path)"
        return self._project_dir
    
    @property
    def config_file(self) -> str:
        "The config file"
        try:
            return self._config_file
        except AttributeError:
            # List of possible mkdocs configuration filenames
            CANDIDATES = ['mkdocs.yaml', 'mkdocs.yml']
            for filename in os.listdir(self.project_dir):
                if filename in CANDIDATES:
                    self._config_file = os.path.join(self.project_dir, filename)
                    return self._config_file
            raise FileNotFoundError("This is not an MkDocs directory")
        
    @property
    def config(self) -> SuperDict:
        """
        Get the configuration from the config file.
        All main items of the config are accessible with the dot notation.
        (config.site_name, config.theme, etc.)
        """
        try:
            return self._config
        except AttributeError:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                self._config = SuperDict(yaml.safe_load(file))
            return self._config
        

    @property
    def source_doc_dir(self):
        "The target directory of markdown files (rendered macros)"
        return os.path.join(REF_DIR, 
                            self.project_dir, 
                            DOCS_DEFAULT_DIRNAME)

    

    


    

    # ----------------------------------
    # Build
    # ----------------------------------


    def build(self, strict:bool=False,
              verbose:bool=True) -> subprocess.CompletedProcess:
        """
        Build the documentation, to perform the tests

        Arguments:
            - strict (default: False) to make the build fail in case of warnings
            - verbose (default: True), to generate the target_files directory

        Returns:
        (if desired) the low level result of the process 
        (return code and stderr).

        This is not needed, since, those values are stored, and parsed.
        """
        os.chdir(self.project_dir)
        command = MKDOCS_BUILD.copy()
        assert '--strict' not in command
        if strict:
            command.append('--strict')
        if verbose:
            command.append('--verbose')
        print("BUILD COMMAND:", command)
        self._build_result = run_command(*command)
        return self.build_result


    # ----------------------------------
    # Post-build properties
    # Will fail if called before build
    # ----------------------------------
    @property
    def build_result(self) -> subprocess.CompletedProcess:
        """
        Result of the build (low level)
        """
        try:
            return self._build_result
        except AttributeError:
            raise AttributeError("No build result yet (not run)")
        
    @property
    def trace(self) -> str:
        "Return the trace of the execution (log as text)"
        return self.build_result.stderr
    
   
    @property
    def success(self) -> bool:
        "Was the execution of the build a success?"
        return self.build_result.returncode == 0
    
    @property
    def log(self) -> List[SuperDict]:
        """
        The parsed trace
        """
        try:
            return self._log
        except AttributeError:
            self._log = parse_log(self.trace)
            # print("BUILT:", self.log)
            return self._log

    @property
    def log_severities(self) -> List[str]:
        """
        List of severities (DEBUG, INFO, WARNING) found
        """
        try:
            return self._log_severities
        except AttributeError:
            self._log_severities = list({entry.get('severity', '#None') 
                                     for entry in self.log})
            return self._log_severities


    def find_entries(self, title:str='', source:str='',
                     severity:str='') -> List[SuperDict]:
        """
        Filter entries according to criteria of title and severity;
        all criteria are case-insensitive.

        Arguments:
            - title: regex
            - source: regex, for which entity issued it (macros, etc.)
            - severity: one of the existing sevirities
        """
        if not title and not severity and not source:
            return self.log
        
        severity = severity.upper()
        # if severity and severity not in self.log_severities:
        #     raise ValueError(f"{severity} not in the list")
        
        filtered_entries = []
        # Compile the title regex pattern once (if provided)
        title_pattern = re.compile(title, re.IGNORECASE) if title else None
        source_pattern = re.compile(source, re.IGNORECASE) if source else None
        
        for entry in self.log:
            # Check if the entry matches the title regex (if provided)
            if title_pattern:
                title_match = re.search(title_pattern, entry.get('title', ''))
            else:
                title_match = True
            # Check if the entry matches the source regex (if provided)
            if source_pattern:
                source_match = re.search(source_pattern, entry.get('source', ''))
            else:
                source_match = True

            # Check if the entry matches the severity (if provided)
            if severity:
                severity_match = (entry['severity'] == severity)
                # print("Decision:", severity_match)
            else:
                severity_match = True
            # If both conditions are met, add the entry to the filtered list
            if title_match and severity_match and source_match:
                filtered_entries.append(entry)
        assert isinstance(filtered_entries, list)
        return filtered_entries


    def find_entry(self, title:str='', 
                   source:str = '',
                   severity:str='') -> SuperDict | None:
        """
        Find the first entry according to criteria of title and severity

        Arguments:
            - title: regex
            - source: regex
            - severity
        """
        found = self.find_entries(title, 
                                  source=source,
                                  severity=severity)
        if len(found):
            return found[0]
        else:
            return None

    # ----------------------------------
    # Get the Markdown pages
    # ----------------------------------


    @property
    def pages(self) -> List[MarkdownPage]:
        "The list of Markdown pages + the HTML produced by the build (TBD)"
        try:
            return self._pages
        except AttributeError:
            # Make the list and 
            full_project_dir = os.path.join(REF_DIR, self.project_dir)
            full_doc_dir = os.path.join(REF_DIR, self.source_doc_dir)
            self._pages = [MarkdownPage(el, 
                            project_dir = full_project_dir,
                            doc_dir=DOCS_DEFAULT_DIRNAME
                            ) 
                            for el in list_markdown_files(full_doc_dir)]
            return self._pages
        
    def get_page(self, name:str):
        """
        Find a name in the list of Markdown pages (filenames)
        using a name (full or partial, with or without extension).
        """
        # get all the filenames of pages:
        filenames = [page.filename for page in self.pages]
        # get the filename we want, from that list:
        filename = find_page(name, filenames)
        # return the corresponding page:
        for page in self.pages:
            if page.filename == filename:
                return page
        
            
    def get_plugin(self, name:str) -> SuperDict:
        "Get the plugin by its plugin name"
        for el in self.config.plugins:
            if name in el:
                if isinstance(el, str):
                    return SuperDict()
                elif isinstance(el, dict):
                    plugin = el[name]
                    return SuperDict(plugin)
                else:
                    raise ValueError(f"Unexpected content of plugin {name}!")
        return SuperDict(self.config.plugins.get(name))



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