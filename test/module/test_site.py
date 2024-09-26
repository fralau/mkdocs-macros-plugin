"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest

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



    