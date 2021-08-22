# --------------------------------------------
# Setup file for the package
#
# Laurent Franceschetti (c) 2018-2020
# --------------------------------------------

import os
from setuptools import setup, find_packages


# --------------------
# Initialization
# --------------------

VERSION_NUMBER = '0.6.0'

# required if you want to run document/test
# pip install 'mkdocs-macros-plugin[test]'
TEST_REQUIRE = ['mkdocs-macros-test', 'mkdocs-material>=6.2',
                'mkdocs-include-markdown-plugin']

# --------------------
# Setup
# --------------------


def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mkdocs-macros-plugin',
    version=VERSION_NUMBER,
    description="Unleash the power of MkDocs with macros and variables",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown macros',
    url='https://github.com/fralau/mkdocs_macros_plugin',
    author='Laurent Franceschetti',
    author_email='info@settlenext.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs>=0.17',
        'jinja2',
        'termcolor',
        'pyyaml',
        'python-dateutil',
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
            'macros = mkdocs_macros.plugin:MacrosPlugin'
        ]
    }
)
