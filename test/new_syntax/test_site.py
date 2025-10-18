"""
Testing the project

(C) Laurent Franceschetti 2025
"""
import pytest

from test.fixture import MacrosDocProject

CURRENT_PROJECT = '.'


def test_new_syntax():
    project = MacrosDocProject(CURRENT_PROJECT)
    project.build()
    # did not fail
    assert not project.build_result.returncode


    page = project.get_page('index')
    
    price = page.meta.unit_price
    print("Price found in the meta of the page:", price)
    assert page.find_text(f'{price} EUR')
    if price > 10:
        assert page.find_text('this is expensive')
    else:
        assert page.find_text('this is cheap')
        