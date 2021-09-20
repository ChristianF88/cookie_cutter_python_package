#!/bin/sh

echo INIT GIT
git init
echo 
echo CREATE VENV
python -m venv venv
echo 
echo INSTALLING PACKAGE
pip install -e .
echo 
echo INSTALLING DEV DEPENDENCIES
pip install -r requirements_dev.txt
echo 
echo CREATE HOOK
echo "#!/bin/sh" > .git/hooks/pre-commit 
echo "pytest -sv" >> .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
