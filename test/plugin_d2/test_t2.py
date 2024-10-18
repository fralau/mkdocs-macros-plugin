"""
Testing the d2 project

There was an incompatibility:
Error: The current file is not set for the '!relative' tag. It cannot be used in this context; the intended usage is within `markdown_extensions`.

see https://github.com/fralau/mkdocs-macros-plugin/issues/249 

Requires d2

(C) Laurent Franceschetti 2024
"""

REQUIRED = "d2"

import pytest
import subprocess

def is_d2_installed():
    try:
        subprocess.run(["brew", "list", REQUIRED], check=True, 
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


import test
from test.fixture import MacrosDocProject


@pytest.mark.skipif(not is_d2_installed(), reason="d2 is not installed")
def test_d2():
    """
    This test will run only if d2 library is installed;
    otherwise the d2 plugin will not run
    https://d2lang.com/tour/install/
    """
    project = MacrosDocProject()
    project.build(strict=False)
    # did not fail
    print(project.build_result.stderr)
    assert not project.build_result.returncode, "Failed when it should not" 