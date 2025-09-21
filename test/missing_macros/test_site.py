"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest

from mkdocs_test import DocProject





def test_build():
    project = DocProject(".")
    # did not fail

    print("building website...")
    build_result = project.build(strict=True)
    result = build_result.stderr
    print("Result:", result)
    # fails, declaring that the pluglet exists and must be installed.
    assert build_result.returncode != 0 # failure 
    assert "pluglet" in result
    assert "pip install" in result

    