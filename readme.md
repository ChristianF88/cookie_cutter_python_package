# {{cookiecutter.package_name}}

## Description

...

## Installation

Assuming you have python installed on your computer, all we have to do is install this package with `pip`.  

> Attention: On linux and mac you might have to use `pip3` instead `pip`. 
> Try:
> ```sh
> pip3 --help
> ```
> If that does not cause any error, use `pip3`!

### Git

If you have git installed and access to the this repository:

**via https**
```sh
pip install git+https://gitlab.switch.ch/christian.foerster/{{cookiecutter.package_name}}.git
```

**via ssh** (ssh key required)
```sh
pip install git+git@gitlab.switch.ch/christian.foerster/{{cookiecutter.package_name}}.git
```

### No Git

In case you do not have git installed.

 - 1. download the repository
 - 2. unpack the downloaded repo
 - 3. install with pip:
 
 ```sh
pip install <path-to-unpacked-repo>
 ```

 > **PS:**
 > Use `./` as `<path-to-unpacked-repo>` if your console's working directory is the unpacked datapool folder.


 ## Usage

 ```python
 import {{cookiecutter.package_name}}
 
 
 ```
