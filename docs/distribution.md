
# Distribution management

To be able to release versions and to upload
to the pypi and conda repositories 
following packages are required

 - twine - to upload to pypi 
    ```
    conda install -c conda-forge twine
    ```
 - conda-build - to provide tha package on the conda repository
 - anaconda-client - to be able to upload the package to anaconda cloud


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
