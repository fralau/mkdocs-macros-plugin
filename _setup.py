# --------------------------------------------
# Setup file for the package
#
# Laurent Franceschetti (c) 2018-2020
# THIS IS THE OLD VERSION, kept for reference purposes
# --------------------------------------------

import os
from setuptools import setup, find_packages


# --------------------
# Initialization
# --------------------

VERSION_NUMBER = '1.3.7'

# required if you want to run document/test
# pip install 'mkdocs-macros-plugin[test]'
TEST_REQUIRE = ['mkdocs-macros-test', 'mkdocs-material>=6.2',
                'mkdocs-include-markdown-plugin', 'mkdocs-test']

# --------------------
# Setup
# --------------------


def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()


setup(
    name='mkdocs-macros-plugin',
    version=VERSION_NUMBER,
    description="Unleash the power of MkDocs with macros and variables",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown macros',
    url='https://github.com/fralau/mkdocs_macros_plugin',
    author='Laurent Franceschbetti',
    author_email='info@settlenext.com',
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'mkdocs>=0.17',
        'jinja2',
        'termcolor',
        'pyyaml',
        'hjson',
        'pathspec',
        'python-dateutil',
        'packaging',
        'super-collections'
    ],
    extras_require={
        'test': TEST_REQUIRE,
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'mkdocs.plugins': [
            'macros = mkdocs_macros.plugin:MacrosPlugin',
        ]
    }
)
