# --------------------------------------------
# Setup file for the package
#
# Laurent Franceschetti (c) 2018
# --------------------------------------------

import os
from setuptools import setup, find_packages


def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mkdocs-macros-plugin',
    version='0.2.2',
    description="Unleash the power of MkDocs with macros and variables",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    keywords='mkdocs python markdown macros',
    url='https://github.com/Useurmind/mkdocs_macros_plugin',
    author='Laurent Franceschetti <info@settlenext.com>, Jochen Grün <jochen.gruen@googlemail.com>',
    author_email='jochen.gruen@googlemail.com',
    license='MIT',
    python_requires='>=3.7',
    install_requires=[
        'mkdocs>=1.0.2',
        'repackage',
        'jinja2',
        'mkdocs'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['*.tests']),
    entry_points={
        'mkdocs.plugins': [
            'macros = macros.plugin:MacrosPlugin'
        ]
    }
)
