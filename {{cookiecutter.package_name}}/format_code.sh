#!/bin/sh

echo RUN ISORT
isort {{cookiecutter.package_name}} test
echo RUN BLACK
black {{cookiecutter.package_name}} test
