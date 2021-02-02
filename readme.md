# {{cookiecutter.package_name}}

## Description

...

## Setup

**Set up a virtual environment with python**
```sh
python -m venv venv
```

**Activate the virtual environment**
(Windows)
```sh
cd venv/Scripts/
activate.bat
cd .. && cd ..
```

(Linux)
```sh
source venv/bin/activate
```
### Get package with Git
**Clone git repo!**
(https)
```sh
git clone https://gitlab.switch.ch/christian.foerster/chriesbach.git
```
(ssh)
```sh
git clone git@gitlab.switch.ch:christian.foerster/chriesbach.git
```

**Install python package!**
```sh
pip install -e chriesbach
```

### Get package without Git

In case you do not have git installed.

 - 1. download the repository
 - 2. unpack the downloaded repo
 - 3. install with pip:
 
 **Install python package!**
 ```sh
pip install <path-to-unpacked-repo>
 ```

## Usage

 ```python
 import {{cookiecutter.package_name}}
 
 
 ```
