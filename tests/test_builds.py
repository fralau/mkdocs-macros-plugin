import pytest
import os
import shutil
import logging
from click.testing import CliRunner
from mkdocs.__main__ import build_command


def setup_clean_mkdocs_folder(mkdocs_yml_path, output_path):
    """
    Sets up a clean mkdocs directory
    
    outputpath/testproject
    ├── docs/
    └── mkdocs.yml
    
    Args:
        mkdocs_yml_path (Path): Path of mkdocs.yml file to use
        output_path (Path): Path of folder in which to create mkdocs project
        
    Returns:
        testproject_path (Path): Path to test project
    """

    testproject_path = output_path / "testproject"

    # Create empty 'testproject' folder
    if os.path.exists(testproject_path):
        logging.warning(
            """This command does not work on windows. 
        Refactor your test to use setup_clean_mkdocs_folder() only once"""
        )
        shutil.rmtree(testproject_path)

    # Copy correct mkdocs.yml file and our test 'docs/'
    shutil.copytree(
        os.path.join(os.path.dirname(mkdocs_yml_path), "docs"),
        testproject_path / "docs",
    )
    if os.path.exists(os.path.join(os.path.dirname(mkdocs_yml_path), "assets")):
        shutil.copytree(
            os.path.join(os.path.dirname(mkdocs_yml_path), "assets"),
            testproject_path / "assets",
        )
    shutil.copyfile(mkdocs_yml_path, testproject_path / "mkdocs.yml")

    return testproject_path


def build_docs_setup(testproject_path):
    """
    Runs the `mkdocs build` command
    
    Args:
        testproject_path (Path): Path to test project
    
    Returns:
        command: Object with results of command
    """

    cwd = os.getcwd()
    os.chdir(testproject_path)

    try:
        run = CliRunner().invoke(build_command)
        os.chdir(cwd)
        return run
    except:
        os.chdir(cwd)
        raise



SHOULD_SUCCEED = [
    "test/debug/mkdocs.yml",
    "test/new_syntax/mkdocs.yml",
    "test/no_module/mkdocs.yml",
    "test/opt-in/mkdocs.yml",
    "test/opt-out/mkdocs.yml",
    "test/simple/mkdocs.yml",
]

SHOULD_FAIL = [
    "test/module/mkdocs.yml",
    "test/module_dir/mkdocs.yml",
]



@pytest.mark.parametrize("mkdocs_yml_path", SHOULD_SUCCEED)
def test_builds_succeeding(mkdocs_yml_path, tmp_path):
    testproject_path = setup_clean_mkdocs_folder(mkdocs_yml_path, tmp_path)
    result = build_docs_setup(testproject_path)
    assert result.exit_code == 0, "'mkdocs build' did not succeed"

@pytest.mark.parametrize("mkdocs_yml_path", SHOULD_FAIL)
def test_builds_failing(mkdocs_yml_path, tmp_path):
    testproject_path = setup_clean_mkdocs_folder(mkdocs_yml_path, tmp_path)
    result = build_docs_setup(testproject_path)
    assert result.exit_code != 0, "'mkdocs build' did not fail"
