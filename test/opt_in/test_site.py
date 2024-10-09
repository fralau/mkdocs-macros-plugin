"""
Testing the project

(C) Laurent Franceschetti 2024
"""
import pytest

from test.fixture import MacrosDocProject

CURRENT_project = '.'




def test_opt_in():
    project = MacrosDocProject(CURRENT_project)
    project.build()
    # did not fail
    assert not project.build_result.returncode
    


    # ---------------------------
    # which pages are rendered?
    # ---------------------------
    # test the config:
    macros = project.macros_plugin
    assert macros.render_by_default == False
    
    page = project.get_page('render_this_one')
    assert page.title == "Render (by name)"
    assert page.is_markdown_rendered()
    assert page.find(page.meta.signal), f"Did not find signal '{page.meta.signal}'"

    print([page.source.markdown for page in project.pages.values()])
    page2 = project.get_page('rendered/noname')
    assert page2.file.src_uri == 'rendered/noname.md', f"is: {page2.file.src_uri}"
    assert page2.find("0: Hello world")
    assert page2.is_markdown_rendered()


    assert not project.get_page('not_rendered/noname').is_markdown_rendered()

    # exception in the meta:
    exception_page = project.get_page('rendered/exception')
    assert exception_page.meta.render_macros == False
    assert not exception_page.is_markdown_rendered()
    assert exception_page.find('macros_info')
