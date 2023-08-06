### Test & Build
    Install your intended package by typing in this command.
        $ python3 setup.py install
        
    Build distributions package
        $ python3 setup.py sdist bdist_wheel
        
### Publish the package
    twine is a library that helps you upload your package distributions
    to pypi. Before executing the following command, make sure you have an account on PyPI
   
    $ twine upload dist/*


### Install the package
    pip install uc_model_creator
    

### Install from github
    pip install git+https://github.com/ulevon/model_creation.git#egg=uc-model-creator    
    
    
### How to run script from command line

    $ uc_model_creator -output=/home/levon/Pictures/ -images_folder=/home/levon/Pictures/