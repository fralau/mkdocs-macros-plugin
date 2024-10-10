"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest

from test.fixture import MacrosDocProject


from .hooks import MY_VARIABLES, MY_FUNCTIONS, MY_FILTERS, bar, scramble


def test_pages():
    project = MacrosDocProject(".")
    build_result = project.build(strict=True)
    # did not fail
    return_code = project.build_result.returncode
    assert not return_code, f"Build returned with {return_code} {build_result.args})" 

    # check the presence of variables in the environment
    print("Variables:", list(project.variables.keys()))
    for variable in MY_VARIABLES:
        assert variable in project.variables
        print(f"{variable}: {project.variables[variable]}")

    print("Macros:", list(project.macros.keys()))
    for macro in MY_FUNCTIONS:
        assert macro in project.macros
        print(f"{macro}: {project.macros[macro]}")

    print("Filters:", list(project.filters.keys()))
    for filter in MY_FILTERS:
        assert filter in project.filters
        print(f"{filter}: {project.filters[filter]}") 

    # ----------------
    # First page
    # ----------------


    page = project.get_page('index')
    assert page.is_markdown_rendered()
    # variable
    value = MY_VARIABLES['x2']
    print(f"Check if x2 ('{value}') is present")
    assert page.find(value, header="Variables")
    # macro
    print("Check macro: bar")
    assert page.find(bar(2, 5), header="Macros")
    # filter
    message = page.meta.message
    result = scramble(message)
    print(f"Check filter: scramble('{message}') --> '{result}'")
    assert page.find(result, header="Filters")
    
    
    

    # ----------------
    # Second page
    # ----------------
    # there is intentionally an error (`foo` does not exist)
    page = project.get_page('second')
    assert 'foo' not in project.config.extra
    assert page.is_markdown_rendered()
    assert not page.has_error()

