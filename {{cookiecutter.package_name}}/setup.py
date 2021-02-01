#!/usr/bin/env python
"""
-------------------------------------------------------
2021-02-01 -- Christian Foerster
christian.foerster@eawag.ch
-------------------------------------------------------
"""
from setuptools import setup, find_packages

setup(name='{{cookiecutter.package_name}}',
      version='{{cookiecutter.version}}',
      description='',
      long_description='',
      classifiers=[
        'Development Status :: early stage',
        'Programming Language :: Python :: 3',
      ],
      install_requires=["sqlalchemy"],
      keywords='{{cookiecutter.package_name}}',
      packages=find_packages(),
      author='{{cookiecutter.author}}',
      author_email='{{cookiecutter.email}}',
      license='MIT',
      include_package_data=True,
      package_data={'': ['data/*']})
