# kcliutils

![PyPI - package version](https://img.shields.io/pypi/v/kcliutils?logo=pypi&style=flat-square)
![PyPI - license](https://img.shields.io/pypi/l/kcliutils?label=package%20license&style=flat-square)
![PyPI - python version](https://img.shields.io/pypi/pyversions/kcliutils?logo=pypi&style=flat-square)
![PyPI - downloads](https://img.shields.io/pypi/dm/kcliutils?logo=pypi&style=flat-square)

![GitHub - last commit](https://img.shields.io/github/last-commit/kkristof200/py_cli_utils?style=flat-square)
![GitHub - commit activity](https://img.shields.io/github/commit-activity/m/kkristof200/py_cli_utils?style=flat-square)

![GitHub - code size in bytes](https://img.shields.io/github/languages/code-size/kkristof200/py_cli_utils?style=flat-square)
![GitHub - repo size](https://img.shields.io/github/repo-size/kkristof200/py_cli_utils?style=flat-square)
![GitHub - lines of code](https://img.shields.io/tokei/lines/github/kkristof200/py_cli_utils?style=flat-square)

![GitHub - license](https://img.shields.io/github/license/kkristof200/py_cli_utils?label=repo%20license&style=flat-square)

## Description

Python cli utils for faster development

## Install

~~~~bash
pip install kcliutils
# or
pip3 install kcliutils
~~~~

## How to use

### 1. Package related

####  npp/new_python_package
  - Run in an empty folder with git checked out
  - Creates a new empty package, with default files, such as .gitignore, README.md, setup.py, demo.py, LICENSE, etc.

~~~~shell
# cd to desired folder with .git in it

npp package_name
# or
new_python_package package_name
~~~~

`npp test_package_name` will generate

![npp result](https://i.imgur.com/3UUMDjY.png)

####  upp/upgrade_python_package
  - Run in an already existing project folder
  - Updates setup.py with dependencies, bumps version number
  - Updates install_dependencies.sh and requirements.txt
  - Updates readme with dependencies, copies the contents of 'demo.py' to the usage section of the reeadme
  - NOTE: to make this work properly, the packege had to be created with npp.

~~~~shell
# cd to desired folder with .git in it

upp
# or
upgrade_python_package
~~~~

####  ppp/publish_python_package
  - Calls upp, publishes to pypi and installs the new version

~~~~shell
# cd to desired folder with .git in it

ppp "Optional commit message"
# or
publish_python_package "Optional commit message"
~~~~

####  prpipush/upgrade_push_install
  - Same as ppp, but without publishing on pypi (for private, github-hosted packages)

~~~~shell
# cd to desired folder with .git in it

prpipush "Optional commit message"
# or
upgrade_push_install "Optional commit message"
~~~~


### 2. Formatting

####  cl/clean_lines
  - Cleans the ending useless spaces from every line

~~~~shell
# cd to desired folder

cl
# or
clean_lines
~~~~


####  migrate_comment_line_len
  - Updates the lengh of each separator comment line generated with the file generators from this package.

~~~~shell
# cd to desired folder

migrate_comment_line_len Optional_length_which_defaults_to_your_settings
~~~~


### 3. Git

####  psh/push
  - stages/commits everything and pushes to github

~~~~shell
# cd to desired folder

psh "Optional commit message"
# or
push "Optional commit message"
~~~~


####  ftch/fetch
  - git fetch

~~~~shell
# cd to desired folder

ftch
# or
fetch
~~~~


####  pll/pull
  - git pull

~~~~shell
# cd to desired folder

pll
# or
pull
~~~~


### 4. Pip


####  pipu/pip_uninstall
  - pip uninstall

~~~~shell
pipu PACKAGE_NAME
# or
pip_uninstall PACKAGE_NAME
~~~~


####  pipi/pipiu/pip_install
  - pip install -U

~~~~shell
pipi PACKAGE_NAME
# or
pipiu PACKAGE_NAME
# or
pip_install PACKAGE_NAME
~~~~


####  pipir/pip_reinstall
  - pip uninstall && pip install

~~~~shell
pipir PACKAGE_NAME
# or
pip_reinstall PACKAGE_NAME
~~~~


### 5. New files

####  pyreqs/python_requirements
   - creates a requirements.txt file with all the used dependencies

~~~~shell
pyreqs
# creates 'requirements.txt'
# or
python_requirements
~~~~


####  pif/create_python_install_file
   - creates an install_dependencies.sh file with all the used dependencies

~~~~shell
pif
# creates 'install_dependencies.sh'
# or
create_python_install_file
~~~~


####  npc/new_python_class
   - creates a python file with a class-like formatting

~~~~shell
npc file_name
# creates 'file_name.py' class 'FileName' in it
# also accepts relative path 'relative/path/to/file_name'

# or
new_python_class file_name
~~~~
generated file contents
~~~~python
# ------------------------------------------- Imports ------------------------------------------ #

# System


# Pip


# Local


# ---------------------------------------------------------------------------------------------- #



# -------------------------------------- class: TestClass -------------------------------------- #

class TestClass:

    # ---------------------------------------- Init ---------------------------------------- #

    def __init__(
        self
    ):
        return


    # ---------------------------------- Public properties --------------------------------- #




    # ----------------------------------- Public methods ----------------------------------- #




    # --------------------------------- Private properties --------------------------------- #




    # ----------------------------------- Private methods ---------------------------------- #




# ---------------------------------------------------------------------------------------------- #
~~~~


####  npa/new_python_api
   - creates a python file with a api-like formatting (conforming [ksimpleapi](https://github.com/kkristof200/py_simpleapi))

~~~~shell
npa file_name
# creates 'file_name.py' class 'FileName' in it
# also accepts relative path 'relative/path/to/file_name'

# or
new_python_api file_name
~~~~
generated file contents
~~~~python
# ------------------------------------------- Imports ------------------------------------------ #

# System
from typing import Optional, Dict

# Pip
from ksimpleapi import Api

# Local


# ---------------------------------------------------------------------------------------------- #



# --------------------------------------- class: FileName -------------------------------------- #

class FileName(Api):

# -------------------------------------- Overrides ------------------------------------- #

    @classmethod
    def extra_headers(cls) -> Optional[Dict[str, any]]:
        return {

        }


    # ---------------------------------- Public properties --------------------------------- #




    # ----------------------------------- Public methods ----------------------------------- #




    # --------------------------------- Private properties --------------------------------- #




    # ----------------------------------- Private methods ---------------------------------- #




# ---------------------------------------------------------------------------------------------- #
~~~~


####  npe/new_python_enum
   - creates a python file with a enum-like formatting

~~~~shell
npe file_name
# creates 'file_name.py' enum 'FileName' in it
# also accepts relative path 'relative/path/to/file_name'

# or
new_python_enum file_name
~~~~
generated file contents
~~~~python
# ------------------------------------------- Imports ------------------------------------------ #

# System
from enum import Enum

# ---------------------------------------------------------------------------------------------- #



# --------------------------------------- enum: FileName --------------------------------------- #

class FileName(Enum):
    Template = 0


# ---------------------------------------------------------------------------------------------- #
~~~~


####  npf/new_python_file
   - creates a python file with a default file formatting

~~~~shell
npf file_name
# creates 'file_name.py'
# also accepts relative path 'relative/path/to/file_name'

# or
new_python_file file_name
~~~~
generated file contents
~~~~python
# ------------------------------------------- Imports ------------------------------------------ #

# System


# Pip


# Local


# ---------------------------------------------------------------------------------------------- #



# ----------------------------------------- Public vars ---------------------------------------- #




# ---------------------------------------- Private vars ---------------------------------------- #




# ---------------------------------------- Private vars ---------------------------------------- #




# ---------------------------------------- Private vars ---------------------------------------- #




# ---------------------------------------------------------------------------------------------- #
~~~~


####  npfl/new_python_flow
   - creates a python file with a flow-like formatting (check example)

~~~~shell
npfl file_name
# creates 'file_name.py'
# also accepts relative path 'relative/path/to/file_name'

# or
new_python_flow file_name
~~~~
generated file contents
~~~~python
# ------------------------------------------- Imports ------------------------------------------ #

# System


# Pip


# Local


# ---------------------------------------------------------------------------------------------- #



# ------------------------------------------- Methods ------------------------------------------ #



# -------------------------------------------- Paths ------------------------------------------- #




# -------------------------------------------- Vars -------------------------------------------- #




# -------------------------------------------- Flow -------------------------------------------- #



# ---------------------------------------------------------------------------------------------- #
~~~~


####  nps/new_python_subpackage
  - creates a new subpackage at the desired relative path

~~~~shell
nps SUB_PACKAGE_NAME_OR_RELATIVE_PATH
# or
new_python_subpackage SUB_PACKAGE_NAME_OR_RELATIVE_PATH
~~~~

`nps test_subpackage` will generate

![nps result](https://i.imgur.com/xNOBPPg.png)

## Dependencies

[bullet](https://pypi.org/project/bullet), [jsoncodable](https://pypi.org/project/jsoncodable), [kcu](https://pypi.org/project/kcu), [kdependencies](https://pypi.org/project/kdependencies)