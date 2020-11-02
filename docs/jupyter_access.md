
# Jupyter interface / Researcher perspective

##1 Install miniconda

The packages used in the development of the BMCS tool 
suite can be conveniently accessed from within the 
miniconda minimal setup. The installation of miniconda for 
all platforms is provided here:

https://docs.conda.io/en/latest/miniconda.html

##2 Install the BMCS packages with dependencies 
 
Download the package specification file
`environment.yml` 
TODO: I will put it at the root of bmcs-group

Run the setup of the environment by issuing
```
conda env create -f environment.yml
```
If you wish to update your environment later you can issue
```
conda env update -f environment.yml --prune^C
```

##3 Activate the environment 

The list of available environments can be obtained by issuing
```
conda env list
```
Activate the new environment using
```
conda activate bmcs_env
```

The package(s) specified in the `environment.yml`
are now installed locally in the `bmcs_env` and
can be imported if this environment is active.
This can be checked by starting the `python` interpreter
with the `bmcs_env` environment active and testing
```
import bmcs_utils.api as bu
```

##4 Setup the jupyter notebook

To be able to import them, the runtime configuration in Jupyter and Pycharm
projects have to be configured with this environment.

1) get the ipykernel 
    ```
    conda install -c conda-forge ipykernel
    ```
2) create a kernel for the new environment

    ```
    python -m ipykernel install --user --name bmcs_env
    ```
3) start the jupyter notebook, navigate to
   the menu `Kernel -> Change kernel` and select 
   the `bmcs_env` kernel as the active kernel. The 
   kernel name will be displaed at the top right corner
   of the notebook

# Access the jupyter notebooks

It is important to note, that only python files are installed
in the bmcs_env  - no jupyter notebooks. Thus, they
are provided just like `numpy` or `matplotlib` for
further use in the development of further packages.
In this way, the deployment of the webapps
on jupyterhub or binder is solved - since it is possible
to define the environment which automatically
installed all the required packages on demand
from the global conda and pypi repos.

Packaging of jupyter notebooks is a separate problem.
We use them for several different purposes: 

- prototyping code (Phase 1)
- verification code for python modules - that's what (Phase 2)
- documentation with interactive examples (Phase 3)
- presentations - RISE package (Phase 3)
- webapps - appmode (Phase 3)

Thus, in Phases 1 and 2 the notebooks are
within the development directory. The phase 3
is the dissemination of the implemented functionality
in three different ways.

## Set up of the jupyter front-end

## Jupyter in the `bmcs_env` environment

To ensure that your jupyter notebook starts
with an environment configured for bmcs packages
activate the environment
```
conda activate bmcs_env
```
and install jupyter
```
conda install -c conda-forge jupyter
```
Install the tool generating the kernel for jupyter execution
```
conda install -c anaconda ipykernel
```
Construct a jupyter kernel using the `bmcs_env` environment
```
python -m ipykernel install --user --name bmcs_env
```
Execute
```
jupyter notebook
```
To have all the packages included in the `bmcs_env` 
ensure that the kernel `bmcs_env` is active when running 
the nobetook. The kernel can be set in the menu
**Kernel -> Change kernel**


## Notebook extensions 
It is recommended to use the notebook extensions that 
include useful features, like

- table of contents which is useful for long 
  noteboks explaining the model derivation
- RISE: which can convert the notebook to a slide 
  presentation
- appmode: that converts the notebook to an interactive
  web application

## Plotting using matplotlib

Matplotlib provides a front end that can be 
combined with the `ipywidgets` to integrate the 
figures within a layout of widgets. To use this 
feature, the notebook must start with the magic command
```
%matplotlib widget
```
This feature is implemented in the `ipympl` package
which is automatically included in the environment 
after the setup. Further instructions to this package 
are included here:
https://github.com/matplotlib/ipympl

## Version control for jupyter notebooks 

Stripping Jupyter output cells and execution 
count out while pushing to Git

In Anaconda command prompt execute the following commands
1. Install `nbstripout` tool:\
`conda install -c conda-forge nbstripout`

2. Activate the tool on global Git configuration so it work on all your local repositories using
   * **Windows**\
`mkdir %USERPROFILE%\.config\git`\
`nbstripout --install --global --attributes=%USERPROFILE%\.config\git\attributes`

   * **Linux**\
`mkdir -p ~/.config/git`\
`nbstripout --install --global --attributes=~/.config/git/attributes`

Now, when you **push** a Jupyter Notebook file, the `nbstripout` tool will tell Git to ignore the output cells and the execution count numbers, leaving your local Jupyter file unchanged. It will enable you to push a clean Jupyter file to the repository.

How does it work?

The tool adds a Git filter to these files\
`USER_HOME_DIRECTORY\.config\git\attributes`\
`USER_HOME_DIRECTORY\.gitconfig`\
which strips output cells and execution count out for Jupyter files.

For more info: https://github.com/kynan/nbstripout
