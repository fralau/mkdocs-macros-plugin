"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest

from test.fixture import DocProject

CURRENT_PROJECT = 'simple'



def test_pages():
    PROJECT = DocProject(CURRENT_PROJECT)
    build_result = PROJECT.build(strict=False)
    # did not fail
    return_code = PROJECT.build_result.returncode
    assert not return_code, f"Build returned with {return_code} {build_result.args})" 

    # ----------------
    # First page
    # ----------------
    VARIABLE_NAME = 'greeting'

    # it is defined in the config file (extra)
    assert VARIABLE_NAME in PROJECT.config.extra

    page = PROJECT.get_page('index')
    assert page.is_rendered
    
    # check that the `greeting` variable is rendered:
    assert VARIABLE_NAME in PROJECT.variables
    assert PROJECT.variables[VARIABLE_NAME] in page.markdown
    

    # ----------------
    # Second page
    # ----------------
    # there is intentionally an error (`foo` does not exist)
    page = PROJECT.get_page('second')
    assert 'foo' not in PROJECT.config.extra
    assert page.is_rendered
    assert page.has_error
    
def test_strict():
    "This project must fail"
    PROJECT = DocProject(CURRENT_PROJECT)

    # it must fail with the --strict option,
    # because the second page contains an error
    PROJECT.build(strict=True)
    assert PROJECT.build_result.returncode
    warning = PROJECT.find_entry("Macro Rendering", 
                              severity='warning')
    assert warning, "No warning found"



    