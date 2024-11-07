"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest

from mkdocs_test import DocProject





def test_pages():
    project = DocProject(".")
    build_result = project.build(strict=False)
    # did not fail
    return_code = project.build_result.returncode
    assert not return_code, f"Build returned with {return_code} {build_result.args})" 

    # ----------------
    # First page
    # ----------------
    VARIABLE_NAME = 'greeting'

    # it is defined in the config file (extra)
    assert VARIABLE_NAME in project.config.extra

    page = project.get_page('index')
    assert page.is_markdown_rendered()
    
    # check that the `greeting` variable (defined under 'extra') is rendered:
    variables = project.config.extra
    assert VARIABLE_NAME in variables
    assert variables.greeting in page.markdown

    # test built-in filters (#253)
    header = 'built-in filters'
    assert page.find_text("result", header)
    assert page.find_text("result is: 17.5", header) # abs
    assert page.find_text("saying: HELLO WORLD", header) # upper
    assert page.find_text("length is: 12", header) # length
    
    

    # ----------------
    # Second page
    # ----------------
    # there is intentionally an error (`foo` does not exist)
    page = project.get_page('second')
    assert 'foo' not in project.config.extra
    assert page.is_markdown_rendered()
    assert page.find_text('Macro Rendering Error')
    
def test_strict():
    "This project must fail"
    project = DocProject(".")

    # it must fail with the --strict option,
    # because the second page contains an error
    project.build(strict=True)
    assert project.build_result.returncode
    warning = project.find_entry("Macro Rendering", 
                              severity='warning')
    assert warning, "No warning found"
    print(warning)



    