
# Python interface / Developer perspective

## Git

Install the git package. 
For linux use:

sudo apt-get install git

For windows use:

@todo: please add  

## PyCharm

register and pickup the professional academic free version
https://www.jetbrains.com/pycharm/download

Follow the instructions there to install it.

## Clone bmcs repositories 

Start pycharm. In the introductory window select 
- open from version control system. Register using the github.com
credentials. Clone the repository

bmcs-group/bmcs_utils

## Setup the development package

Each of the `bmcs` packages contains the  
`environment.yml` and the `setup.py` file 
in its root directory

By issuing the command
```
pip install -e .
```
your local source code package directory will 
be integrated into the `bmcs_env`
environment. 
Check to see that it is the case by issuing
```
import sys
print(sys.path)
```
The current package directory should be included in the list. 
This approach has the advantage that your workspace is 
treated in the same way as packages comming from pypi 
repository. This makes the import paths universally 
valid in differnt usage modes:
[Research access](jupyter_access.md), 
[Python access](python_access.md).

Moreover, it is used also in the deployed 
installation on a remote service like 
binder launched from the `github` repository.
This can be seen in the `environment.yml` which 
specifies the required
packages. Note the last entry in this dependency:
specifying `-e .`
```
name: bmcs_env
channels:
- conda-forge
dependencies:
# required conda packages
- pip:
  - -e .
```
The entry `-e .` means that 
The `environment.yml` specification is 
used if the repository is installed in remote services,
e.g. on `binder`.


# Configure Jupyter

To use and modify the jupyter notebooks in your installation
access setup the jupyter environment as described in 
[Jupyter access](jupyter_access.md)

# Configure Pycharm

- In PyCharm - the correct interpreter from `bmcs_env` must be taken -
  in File->Settings->Build->Interpreter

