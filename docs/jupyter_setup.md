
## Set up of the jupyter front-end

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
