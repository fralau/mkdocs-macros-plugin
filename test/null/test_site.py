"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest


import test
from test.fixture import MacrosDocProject



def test_pages():
    PROJECT = MacrosDocProject()
    build_result = PROJECT.build(strict=False)
    # did not fail
    return_code = PROJECT.build_result.returncode
    assert not return_code, "Failed when it should not" 


    # ----------------
    # First page
    # ----------------


    page = PROJECT.get_page('index')
    print("Has error:", page.has_error)
    assert not page.has_error()
    ERROR_MSG = f"Is rendered!:\n{page.markdown}\n---SOURCE:\n{page.source.markdown}\n---"
    assert not page.is_markdown_rendered(), ERROR_MSG

    


    # ----------------
    # Second page
    # ----------------
    # there is intentionally an error (`foo` does not exist)
    page = PROJECT.get_page('second')

    assert not page.is_markdown_rendered()
    
def test_strict():
    "This project must fail"
    PROJECT = MacrosDocProject()

    # it must not fail with the --strict option,
    PROJECT.build(strict=True)
    assert not PROJECT.build_result.returncode, "Failed when it should not"



    