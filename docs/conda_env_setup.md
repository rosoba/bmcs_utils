
# Setup the BMCS development environment

## Miniconda / Anaconda

The packages used in the development of the BMCS tool suite can be conveniently 
accessed from within the miniconda minimal setup. The installation for 
all platforms is provided here:

https://docs.conda.io/en/latest/miniconda.html

## Git

Install the git package. 
For linux use:

sudo apt-get install git

For windows usd:

## PyCharm

register and pickup the professional academic free version
https://www.jetbrains.com/pycharm/download

Follow the instructions there to install it.

## Clone bmcs repositories 

Start pycharm. In the introductory window select 
- open from version control system. Register using the github.com
credentials. Clone the repository

bmcs-group/bmcs_utils

## Setup your environment 

In the root directory of this package, there is the environment.yml 
file specifying all packages required for the execution and development
of bmcs packages. Issue the command:

```
conda env create -f environment.yml
```

which will install the scientific computing environment called bmcs.
You can activate the individual conda environments using the commands

```
conda env list
conda activate bmcs_env
```

In all your bmcs pycharm projects define the Python interpreter from choose the 
the bmcs_env conda environment. This will set up all the other dependencies 
correspondingly.

## Setup the import path for bmcs packages

Since the environment definition file `environment.yml`
contains the entry `-e .`
```
name: bmcs_env
channels:
- conda-forge
dependencies:
# required conda packages
- pip:
  - -e .
```
you setup complete. The entry `-e .`
uses the `setup.py` file in your root directory 
to register the developed packages directly in the 
`bmcs_env` environment

This entry is equivalent to the command
```
pip install -e .
```
You can check the
setting by starting the python interpreter and issuing
```
import sys
print(sys.path)
```
The current directory should be included in the list. 
This approach has the advantage that your workspace is 
treated in the same way as packages comming from pypi 
repository. 

# Uploading and releasing your package

@todo: this requires an access to the pypi
account - a bmcs-group pypi account needs to be setup.

# Installation of a pypi package in your environment 

Released package can be installed in the 
 current environment. using the command
```
pip install my_bmcs_package
```
The old package will be uninstalled 
from the environment and replaced by the released package.
