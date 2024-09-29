"""
Testing the project

(C) Laurent Franceschetti 2024
"""
import pytest

from test.fixture import DocProject

CURRENT_PROJECT = 'opt_in'




def test_opt_in():
    PROJECT = DocProject(CURRENT_PROJECT)
    PROJECT.build()
    # did not fail
    assert not PROJECT.build_result.returncode
    


    # ---------------------------
    # which pages are rendered?
    # ---------------------------
    # test the config:
    macros = PROJECT.macros_plugin
    assert macros.render_by_default == False
    
    page = PROJECT.get_page('render_this_one')
    assert page.is_rendered
    assert page.find(page.metadata.signal), f"Did not find signal '{page.metadata.signal}'"

    print([page.filename for page in PROJECT.pages])
    page2 = PROJECT.get_page('rendered/noname')
    assert page2.filename == 'rendered/noname.md', f"is: {page2.filename}"
    assert page2.find("0: Hello world")
    assert page2.is_rendered


    assert not PROJECT.get_page('not_rendered/noname').is_rendered

    # exception in the metadata:
    exception_page = PROJECT.get_page('rendered/exception')
    assert exception_page.metadata.render_macros == False
    assert not exception_page.is_rendered
    assert exception_page.find('macros_info')
