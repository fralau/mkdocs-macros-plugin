"""
Testing the project

(C) Laurent Franceschetti 2024
"""
import pytest

from test.fixture import MacrosDocProject

CURRENT_PROJECT = 'opt_out'




def test_opt_in():
    PROJECT = MacrosDocProject(CURRENT_PROJECT)
    PROJECT.build()
    # did not fail
    assert not PROJECT.build_result.returncode
    


    # ---------------------------
    # which pages are rendered?
    # ---------------------------
    # test the config (this is the default anyway)
    macros = PROJECT.macros_plugin
    assert macros.render_by_default == True
    
    # opt-out:
    page = PROJECT.get_page('index')
    assert page.metadata.render_macros == False
    assert not page.is_rendered
    assert "macros_info" in page.markdown


    # Normal:
    page = PROJECT.get_page('rendered')
    assert "render_macros" not in page.metadata
    assert page.is_rendered
    assert page.metadata.signal in page.markdown

