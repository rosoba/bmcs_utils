
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

The developed models are accessible in three perspectives.
The aim is to provide a seamless transition between the 
individual perspectives to the code. The first perspective
 provides a simple interaction with the model 
via the webapp interface. It presents the functionality and 
features of the model to a (Visitor/Reader/User). 

Deeper explanation of the model features in presented in
form of jupyter notebooks accompanying every 
model component. These notebooks demonstrate the model
functionality and  can be modfied and extended by the 
user to get deeper insight into the model behavior, into the 
modeled phenomena. Then, they can be used to interpret
expermental data and to perform parameteric studies.

To develop own model components the open source code can be
cloned using the git versioning control system. The repositories
are available on `github` in the organization 
named `bmcs-group`. 

Summary of access perspective, interfaces and roles:

 - [**Webapp (student/reader interface):**](webapp_access.md) via web browser by accessing a remote server.
   either in a `jupyterhub` or using  `binder` service. This
   mode is inteded for casual readers and student classes 
   that do not need to install anything on their local computer 
   and can directly start to interact with the models via 
   remote webapps.
   
 - [**Jupyter (researcher interface)**](jupyter_access.md) To perform intensive studies of the models, 
   model calibrations based on experimental data and 
   parametric studies the BMCS packages can be installed  
   locally. Included Jupyter notebooks provide the starting 
   point for modifications and processing of data.
   
 - [**Python (developer interface)**](python_access.md) Development of Python code supporting the 
   Jupyter notebooks requires the developer setup with an access
   to the `github server` and a development environment. Currently
   `Pycharm` IDE is being used in the development 
   of BMCS tool suite.

 - [**Distribution (manager interface)**](distribution.md) 
   Build and upload packages to repositories 
   (pypi, conda)
