"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest
import re

from test.fixture import DocProject, find_after

CURRENT_PROJECT = 'module'



def test_pages():
    PROJECT = DocProject(CURRENT_PROJECT)
    PROJECT.build()
    # did not fail
    assert not PROJECT.build_result.returncode

    # ----------------
    # Check that the chatter works
    # ----------------
    entries = PROJECT.find_entries(source='main')
    assert len(entries) > 0
    # the post-built worked:
    assert PROJECT.find_entry(source='main', title='post_build')

    # ----------------
    # First page
    # ----------------
    page = PROJECT.get_page('index')
    assert page.is_rendered

    VARIABLE_NAME = 'unit_price'

    # it is defined in the config file (extra)
    assert VARIABLE_NAME in PROJECT.config.extra
    price = PROJECT.config.extra.unit_price


    # check the page metadata
    # those metadata are not in the config file
    metadata = page.metadata
    assert 'user' in metadata
    assert 'bottles' in metadata
    assert 'announcement' in metadata

    assert metadata.user == 'Joe'
    assert page.find(metadata.user, header='Installed', header_level=4)
    assert page.find(metadata.announcement, header='Accessing meta')
    assert page.find(metadata.bottles.lemonade, header='Dot notation')
    assert not page.find(metadata.user * 2, header='Macro') # negative test

    assert 'bottles' not in PROJECT.config.extra
    assert 'bottles' not in PROJECT.variables

    # check that the `greeting` variable is rendered:
    assert VARIABLE_NAME in PROJECT.variables
    assert f"{price} euros" in page.markdown

    assert f"{PROJECT.macros_plugin.include_dir}" in page.markdown

    # check that both on_pre/post_page_macro() worked
    assert "Added Footer (Pre-macro)" in page.markdown, f"Not in {page.markdown}"
    assert page.find(r'is \d{4}-\d{2}-\d{2}', header='Pre-macro')

    assert "Added Footer (Post-macro)" in page.markdown
    assert find_after(page.plain_text, 'name of the page', 'home')
    assert page.find('Home', header='Post-macro')
    # ----------------
    # Environment page
    # ----------------
    page = PROJECT.get_page('environment')

    # read a few things that are in the tables
    assert page.find('unit_price = 50', header='General list')
    # there are two headers containing 'Macros':
    assert page.find('say_hello', header='Macros$') 


    # test the `include_file()` method (used for the mkdocs.yaml file)
    HEADER = r"^mkdocs.*portion"
    assert page.find('site_name:', header=HEADER)
    assert page.find('name: material', header=HEADER)
    assert not page.find('foobar 417', header=HEADER) # negative control

    # ----------------
    # Literal page
    # ----------------
    page = PROJECT.get_page('literal')
    # instruction not to render:
    assert page.metadata.render_macros == False

    assert page.is_rendered == False, f"Target: {page.markdown}, \nSource:{page.source_page.markdown}"

    # Latex is not interpreted:
    latex = re.escape(r"\begin{tabular}{|ccc|}")
    assert page.find(latex, header='Offending Latex')

    # Footer is processed (but not rendered)
    assert page.find(r'now()', header='Pre-macro')
    assert page.find('Not interpreted', header='Post-macro')


def test_strict():
    "This project must fail"
    PROJECT = DocProject(CURRENT_PROJECT)

    # it must fail with the --strict option,
    # because the second page contains an error
    PROJECT.build(strict=True)
    assert not PROJECT.build_result.returncode
    warning = PROJECT.find_entry("Macro Rendering", 
                              severity='warning')
    assert not warning, "Warning found, shouldn't!"



    