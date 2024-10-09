"""
Testing the project

(C) Laurent Franceschetti 2024
"""
import pytest

from mkdocs_test.common import h1
from test.fixture import MacrosDocProject






def test_opt_in():
    project = MacrosDocProject('.')
    project.build()
    # did not fail
    assert not project.build_result.returncode
    


    # ---------------------------
    # which pages are rendered?
    # ---------------------------
    # test the config (this is the default anyway)
    macros = project.macros_plugin
    assert macros.render_by_default == True

    h1("Pages")
    print("Pages:", len(project.pages))
    for page in project.pages.values():
        print(page.file.src_uri, page.title)
    print("---")
    # opt-out:
    page = project.get_page('index')
    assert page.meta.render_macros == False
    assert not page.is_markdown_rendered()
    assert "macros_info" in page.markdown


    # Normal:
    page = project.get_page('rendered')
    assert page
    assert "render_macros" not in page.meta
    assert page.is_markdown_rendered()
    assert page.meta.signal in page.markdown

