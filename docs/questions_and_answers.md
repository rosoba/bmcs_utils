
# How is the dependency between bmcs packages resolved?

This question is solved differently for development 
installation and for application installation.

In case of development installation, the import 
path must be set within the current conda environment.

In case of application installation, the pip dependency
management is used to install the required 
packages on demand.   

