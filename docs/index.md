
# BMCS development process

The BMCS tool suite consists of several packages
that are developed in coordinate way in parallel.
The  `bmcs_utils` is used by any other package.
It provides the convenience of mapping from the 
model classes to an interactive jupyter user interface.
As a result, functionality implemented in the BMCS models 
is accessible in a multitude of ways.
 - in a local installation using standard browsers
 - in a remote server, either a private `jupyterhub` 
   server or the  `binder` service that can execute     
   the code directly from the `github` repository.
 - via an `api` (application programming interface) 
   in further packages.

# Setup of environment for a bmcs project

The setup of the environment using the `conda` 
manager is described in the document:

[Setup of bmcs_env environment](conda_env_setup.md)

# Jupyter setup

Hints to the setup and usage of jupyter are summarized here

[Jupyter setup](jupyter_setup.md)



[]
