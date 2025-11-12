"""
Testing the module configurations 
"""

import os
import sys

import pytest



from .fixture import MacrosDocProject
from typing import List, Dict


# -------------------------------------
# Parameters
# -------------------------------------
DIR_NAME = '_temp'
UNIT_PRICE = 50
QUANTITY = 20
CONTENT =  f"""
                nav:
                    - Home: index.md

                extra:
                    unit_price: {UNIT_PRICE}
                    quantity: {QUANTITY}
                """


MODULE = '''
def define_env(env):
    """
    This is the hook for the variables, macros and filters.
    """

    @env.macro
    def price(unit_price, no):
        "Calculate price"
        return unit_price * no
'''

FIRST_PAGE = """
             # First page

             The total cost is {{ price(unit_price, quantity) }} euros.
             """


def prepare_site(site_name:str='My Test', 
                 plugins:List=['macros']) -> MacrosDocProject:
    "Basic content"
    if not isinstance(plugins, list):
        raise TypeError("plugins given are not a list")
    # create the path
    path = os.path.join(DIR_NAME, site_name).replace(' ', '_').lower()
    p = MacrosDocProject(path, new=True)
    p.clear()
    p.make_config(site_name=site_name,
                  content=CONTENT,
                  plugins = ['search', 'test'] + plugins
                  )
    return p


def config_with_module(name:str, module_position: str, config:Dict=None):
    """
    Create a site with module as directory 
    """
    if config is not None:
        p = prepare_site(site_name=name, plugins=[{'macros':config}])
    else:
        p = prepare_site(site_name=name)
    p.clear()
    p.add_source_page("index.md", FIRST_PAGE)
    p.add_file(module_position, MODULE)
    p.build(strict=True)
    assert p.success

    # first page
    page = p.get_page('index')
    assert page is not None, "Page not found"
    cost = UNIT_PRICE*QUANTITY
    assert page.find_text(f'{cost} euros'), f"Could not find expected cost ({cost}):\n{page.plain_text}" 



# -------------------------------------
# Tests with modules
# -------------------------------------

def test_module_simple():
    """
    Create a site with simple module
    """
    config_with_module('Simple', 'main.py')

def test_module_simple_other():
    """
    Create a site with simple module, different name
    """
    config_with_module('Simple Other', 'foo.py', config={'module_name': 'foo'})

def test_module_simple_other_sub():
    """
    Create a site with simple module, different name
    """
    config_with_module('Simple Other Sub', 'docs/macros/mymodule.py', 
                       config={'module_name': 'docs/macros/mymodule'})

def test_module_package():
    """
    Create a site with module as directory 
    """
    config_with_module('Package', 'main/__init__.py')

def test_module_package_other():
    """
    Create a site with module as directory 
    """
    config_with_module('Package Other', 'foo/__init__.py',
                       config={'module_name': 'foo'})

def test_module_package_other_error():
    """
    Create a site with module as directory, 
    with config error (bar instead of foo)
    """
    # Unfortunately MkdocsTest doesn't fail in error, if the build fails
    with pytest.raises((ImportError, AssertionError)):
        config_with_module('Package Other Error', 'foo/__init__.py', 
                           config={'module_name': 'bar'})

def test_module_package_other_sub():
    """
    Create a site with simple module, different name
    """
    config_with_module('Package Other Sub', 'docs/macros/mymodule/__init__.py',
                       config={'module_name': 'docs/macros/mymodule'})









   