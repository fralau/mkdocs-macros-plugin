"""
Testing the tester

(C) Laurent Franceschetti 2024
"""
import click
import os

try:
    from .fixture import (PROJECTS, get_tables, parse_log, h1, h2, h3,
                       std_print, DocProject, REF_DIR, list_markdown_files,
                       find_in_html)
except ImportError:
    from fixture import (PROJECTS, get_tables, parse_log, h1, h2, h3,
                        std_print, DocProject, REF_DIR, list_markdown_files,
                        find_in_html)



def test_low_level_fixtures():
    "Test the low level fixtures"

    h1("Unit tests")
    # Print the list of directories
    h2("Directories containing mkdocs.yml")
    for directory in PROJECTS:
        print(directory)
    print(PROJECTS)
    print()


    # Example usage
    h2("Parse tables")
    SOURCE_DOCUMENT = """
# Header 1
Some text.

## Table 1
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
| Value 3  | Value 4  |

## Table 2
| Column A | Column B |
|----------|----------|
| Value A  | Value B  |
| Value C  | Value D  |

## Another Section
Some more text.

| Column X | Column Y |
|----------|----------|
| Value X1 | Value Y1 |
| Value X2 | Value Y2 |
"""

    dfs = get_tables(SOURCE_DOCUMENT)

    # Print the list of directories
    print("Dataframes:")
    for header, df in dfs.items():
        print(f"Table under '{header}':")
        print(df)

    # --------------------
    # Test parsing
    # --------------------
    h2("Parsing logs")
    TEST_CODE = """
DEBUG   -  Running 1 `page_markdown` events
INFO    -  [macros] - Rendering source page: index.md
DEBUG   -  [macros] - Page title: Home
DEBUG   -  No translations found here: '(...)/mkdocs/themes/mkdocs/locales'
WARNING -  [macros] - ERROR # _Macro Rendering Error_

_File_: `second.md`

_UndefinedError_: 'foo' is undefined

```
Traceback (most recent call last):
File "snip/site-packages/mkdocs_macros/plugin.py", line 665, in render
DEBUG   -  Copying static assets.
FOOBAR  -  This is a title with a new severity

Payload here.
DEBUG   -  Copying static assets.
INFO    -  [macros - MAIN] - This means `on_post_build(env)` works
"""
    log = parse_log(TEST_CODE)
    print(log)




    h2("Search in HTML (advanced)")

    # Example usage
    html_doc = """
    <html><head><title>Example</title></head>
    <body>
    <h1>Main Header</h1>
    <p>This is some text under the main header.</p>
    <p>More text under the main header.</p>
    <h2>Sub Header</h2>
    <p>Text under the sub header.</p>
    <h1>Another Main Header</h1>
    <p>Text under another main header.</p>
    </body>
    </html>
    """

    
    print(find_in_html(html_doc, 'more text'))
    print(find_in_html(html_doc, 'MORE TEXT'))
    print(find_in_html(html_doc, 'under the main', header='Main header'))
    print(find_in_html(html_doc, 'under the main', header='Main header'))
    print(find_in_html(html_doc, 'under the', header='sub header'))


def test_high_level_fixtures():
    """
    Test a project
    """
    MYPROJECT = 'opt-in'
    # MYPROJECT = 'simple'
    h1(f"TESTING MKDOCS-MACROS PROJECT ({MYPROJECT})")

    h2("Config")
    myproject = DocProject(MYPROJECT)
    config = myproject.config
    print(config)



    h2("Build")
    result = myproject.build()
    assert result == myproject.build_result
    
    h2("Log")
    assert myproject.trace == result.stderr
    std_print(myproject.trace)




    h2("Filtering the log by severity")
    infos = myproject.find_entries(severity='INFO')
    print(f"There are {len(infos)} info items.")
    print('\n'.join(f"  {i} - {item.title}" for i, item in enumerate(infos)))


    h2("Filtering the log by source")
    infos = myproject.find_entries(source='macros')
    print(f"There are {len(infos)} `macros` items.")
    print('\n'.join(f"  {i} - {item.title}" for i, item in enumerate(infos)))



    h2("Testing the entries")
    print(myproject.find_entries('No default module'))
    print("No default module:", bool(myproject.find_entry('No default module')))
    print("Module:", myproject.find_entries('external Python module'))
    print("Module:", myproject.find_entry('external Python module'))
    print("From macros:", myproject.find_entry(title='post_build',
                                               source='macros'))

    h2("Smart properties")
    print("Modules found:", myproject.modules)

    h2("Variables")
    print(myproject.variables)

    h2("Test variables")
    print("Site name:", myproject.variables.config.site_name)

    h2("Macros")
    print(myproject.macros)

    h2("Filters")
    print(myproject.filters)

    


    h1("Reading the pages")
    h2("Check on pages")                          
    target_dir = os.path.join(REF_DIR, myproject.target_doc_dir)
    print("Official list:", list_markdown_files(target_dir))
    print("Objects target directory:", myproject.target_doc_dir)

    h2("Page objects")                          
    for page in myproject.pages:
        h3(f"PAGE: {page.filename}")
        print("- Main title:", page.h1)
        print("- Filename:", page.filename)
        print('- Error?', page.has_error)
        print("- Source frontmatter:", page.source_page.frontmatter)
        # print("- Frontmatter:", page.frontmatter)
        print("- Metadata:", page.metadata)
        print("- Location of the source file:", 
              page.source_page.full_filename)
        # print("- Markdown", page.markdown)
        # print("- Source Markdown", page.source_page.markdown)
        # print("- Diff (no):", len(page.diff_markdown))
        print("- Rendered?", page.is_rendered)
        # the metadata are identical
        assert page.metadata == page.source_page.metadata
        print('')



@click.command()
@click.option('--short', is_flag=True, 
              help='Test low-level fixtures only')
def command_line(short:bool):
    if short:
        test_low_level_fixtures()
    else:
        test_low_level_fixtures()
        test_high_level_fixtures()


if __name__ == '__main__':
    command_line()