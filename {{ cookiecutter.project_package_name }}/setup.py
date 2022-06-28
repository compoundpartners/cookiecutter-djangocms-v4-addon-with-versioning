# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from {{ cookiecutter.project_slug }} import __version__


setup(
    name='{{ cookiecutter.project_package_name }}',
    version=__version__,
    description=open('README.rst').read(),
    author='Compound Partners Ltd',
    author_email='hello@compoundpartners.co.uk',
    packages=find_packages(),
    platforms=['OS Independent'],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
