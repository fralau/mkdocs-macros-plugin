"""
Fixtures utilities for the testing of Mkdocs-Macros (pytest)
Part of the test package.


(C) Laurent Franceschetti 2024
"""

import os
import re
from io import StringIO
import inspect
import subprocess
import yaml
from typing import List

import markdown
import pandas as pd
from bs4 import BeautifulSoup

from mkdocs_macros.util import SuperDict

# ---------------------------
# Print functions
# ---------------------------
std_print = print
from rich import print
from rich.panel import Panel
from rich.table import Table

TITLE_COLOR = 'green'
def h1(s:str, color:str=TITLE_COLOR):
    "Color print a 1st level title to the console"
    print()
    print(Panel(f"[{color} bold]{s}", style=color, width=80))

def h2(s:str, color:str=TITLE_COLOR):
    "Color print a 2nd level title to the consule"
    print()
    print(f"[green bold underline]{s}")

def h3(s:str, color:str=TITLE_COLOR):
    "Color print a 2nd level title to the consule"
    print()
    print(f"[green underline]{s}")


# ---------------------------
# Low-level functions
# ---------------------------

def find_after(s:str, word:str, pattern:str):
    """
    Find the the first occurence of a pattern after a word
    (Both word and pattern can be regex, and the matching
    is case insensitive.)
    """
    word_pattern = re.compile(word, re.IGNORECASE)
    parts = word_pattern.split(s, maxsplit=1)
    # parts = s.split(word, 1)
    
    if len(parts) > 1:
        # Strip the remainder and search for the pattern
        remainder = parts[1].strip()
        match = re.search(pattern, remainder, flags=re.IGNORECASE)
        return match.group(0) if match else None
    else:
        return None
    
def find_page(name:str, filenames:List) -> str:
    """
    Find a name in list of filenames
    using a name (full or partial, with or without extension).
    """
    for filename in filenames:
        # give priority to exact matches
        if name == filename:
            return filename
        # try without extension
        stem, _ = os.path.splitext(filename)
        if name == stem:
            return filename
    # try again without full path
    for filename in filenames:
        if filename.endswith(name):
            return filename
        stem, _ = os.path.splitext(filename)
        if stem.endswith(name):
            return filename

def list_markdown_files(directory:str):
    """
    Makes a list of markdown files in a directory
    """
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                markdown_files.append(relative_path)
    return markdown_files


def markdown_to_html(markdown_text):
    """Convert markdown text to HTML."""
    html = markdown.markdown(markdown_text, extensions=["tables"])
    # print("HTML:")
    # print(html)
    return html


def style_dataframe(df:pd.DataFrame):
    """
    Apply beautiful and colorful styling to any dataframe
    (patches the dataframe).
    """
    def _rich_str(self):
        table = Table(show_header=True, header_style="bold magenta")

        # Add columns
        for col in self.columns:
            table.add_column(col, style="dim", width=12)

        # Add rows
        for row in self.itertuples(index=False):
            table.add_row(*map(str, row))

        return table

    # reassign str to rich (to avoid messing up when rich.print is used)
    df.__rich__ = _rich_str.__get__(df)

def extract_tables_from_html(html:str, formatter:callable=None):
    """
    Extract tables from a HTML source and convert them into dataframes
    """
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    
    dataframes = {}
    unnamed_table_count = 0
    for table in tables:
        print("Found a table")
        # Find the nearest header
        header = table.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if header:
            header_text = header.get_text()
        else:
            unnamed_table_count += 1
            header_text = f"Unnamed Table {unnamed_table_count}"
        
        # Convert HTML table to DataFrame
        df = pd.read_html(StringIO(str(table)))[0]
        if formatter:
            formatter(df)
        # Add DataFrame to dictionary with header as key
        dataframes[header_text] = df
    
    return dataframes


def get_frontmatter(text:str) -> tuple[str, dict]:
    "Get the front matter from a markdown file"
    # Split the content to extract the YAML front matter
    parts = text.split('---',maxsplit=2)
    if len(parts) > 1:
        frontmatter = parts[1]
        metadata = SuperDict(yaml.safe_load(frontmatter))
        try:
            markdown = parts[2]
        except IndexError:
            markdown = ''
        return (markdown.strip(), frontmatter, metadata)
    else:
        return (text, '', {})
    
def find_in_html(html: str, 
                 pattern: str, 
                 header: str = None, header_level: int = None) -> str | None:
    """
    Find a text or regex pattern in a HTML document (case-insensitive)
    
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
    if not isinstance(pattern, str):
        pattern = str(pattern)

    soup = BeautifulSoup(html, 'html.parser')
    
    # Compile regex patterns with case-insensitive flag
    pattern_regex = re.compile(pattern, re.IGNORECASE)
    
    if header:
        header_regex = re.compile(header, re.IGNORECASE)
        
        # Find all headers (h1 to h6)
        headers = soup.find_all(re.compile('^h[1-6]$', re.IGNORECASE))
        
        for hdr in headers:
            if header_regex.search(hdr.text):
                # Check if header level is specified and matches
                if header_level and hdr.name != f'h{header_level}':
                    continue
                
                # Extract text until the next header
                text = []
                for sibling in hdr.find_next_siblings():
                    if sibling.name and re.match('^h[1-6]$', sibling.name, re.IGNORECASE):
                        break
                    text.append(sibling.get_text(separator='\n', strip=True))
                
                full_text = '\n'.join(text)
                
                # Search for the pattern in the extracted text
                match = pattern_regex.search(full_text)
                if match:
                    # Find the full line containing the match
                    lines = full_text.split('\n')
                    for line in lines:
                        if pattern_regex.search(line):
                            return line
    else:
        # Extract all text from the document
        full_text = soup.get_text(separator='\n', strip=True)
        
        # Search for the pattern in the full text
        match = pattern_regex.search(full_text)
        if match:
            # Find the full line containing the match
            lines = full_text.split('\n')
            for line in lines:
                if pattern_regex.search(line):
                    return line
    
    return None



    


def get_first_h1(markdown_text: str):
    """
    Get the first h1 in a markdown file, 
    ignoring YAML frontmatter and comments.
    """
    # Remove YAML frontmatter
    yaml_frontmatter_pattern = re.compile(r'^---\s*\n(.*?\n)?---\s*\n', 
                                          re.DOTALL)
    markdown_text = yaml_frontmatter_pattern.sub('', markdown_text)
    # Regular expression to match both syntaxes for level 1 headers
    h1_pattern = re.compile(r'^(# .+|.+\n=+)', re.MULTILINE)
    match = h1_pattern.search(markdown_text)
    if match:
        header = match.group(0)
        # Remove formatting
        if header.startswith('#'):
            return header.lstrip('# ').strip()
        else:
            return header.split('\n')[0].strip()
    return None



def get_tables(markdown_text:str) -> dict[pd.DataFrame]:
    """
    Convert markdown text to HTML, extract tables, 
    and convert them to dataframes.
    """
    html = markdown_to_html(markdown_text)
    dataframes = extract_tables_from_html(html, 
                                          formatter=style_dataframe)
    return dataframes



# ---------------------------
# OS Functions
# ---------------------------
def run_command(command, *args) -> subprocess.CompletedProcess:
    "Execute a command"
    full_command = [command] + list(args)
    return subprocess.run(full_command, capture_output=True, text=True)

def get_caller_directory():
    "Get the caller's directory name (to be called from a function)"
    # Get the current frame
    current_frame = inspect.currentframe()
    # Get the caller's frame
    caller_frame = inspect.getouterframes(current_frame, 2)
    # Get the file name of the caller
    caller_file = caller_frame[1].filename
    # Get the absolute path of the directory containing the caller file
    directory_abspath = os.path.abspath(os.path.dirname(caller_file))
    return directory_abspath