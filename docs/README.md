
# BMCS development process

The BMCS tool suite consists of a packages
that are developed in coordinate way in parallel.
The  `bmcs_utils` is used by any other package.

It provides the following functionality:

 - Infrastructure for the definition and composition 
   of model components to quickly obtain an interactive 
   jupyter user interface.
 - Systematic mapping from symbolic expressions
   derived during the model construction using `sympy`
   to model classes
   
By using the `bmcs_utils` as the platform for the model
implementation, the BMCS model components provide 
a transparent mapping between their interactive features
as they appear in the user interface and their internal 
structure, implementation and theoretical background.

Seamless transition between the phase of development and 
usage is the principle followed within the team development
model. 

The developed models are accessible in the following perspective.

 - [Access #1 **Reader:**] via web browser by accessing a remote server.
   either in a `jupyterhub` or using  `binder` service. This
   mode is inteded for casual readers and student classes 
   that do not need to install anything on their local computer 
   and can directly start to interact with the models via 
   remote webapps.
   
 - [Access #2 **Student/Researcher:**](conda_env_setup.md) To perform intensive studies of the models, 
   model calibrations based on experimental data and 
   parametric studies the BMCS packages can be installed  
   locally. Included Jupyter notebooks provide the starting 
   point for modifications and processing of data.
   
 - [Access #3 **Developer:**](conda_env_setup.md) Development of Python code supporting the 
   Jupyter notebooks requires the developer setup with an access
   to the `github server` and a development environment. Currently
   `Pycharm` IDE is being used in the development 
   of BMCS tool suite.

# Setup of environment for a bmcs project

The setup of the environment using the `conda` 
manager is described in the document:

[Setup of bmcs_env environment]

# Jupyter setup

Hints to the setup and usage of jupyter are summarized here

[Jupyter setup](jupyter_setup.md)

