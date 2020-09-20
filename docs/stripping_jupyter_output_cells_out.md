
## Stripping Jupyter output cells and execution count out while pushing to Git

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
