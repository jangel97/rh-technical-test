Ansible Role pytest_tester 
=========

The aim of this role is to encapsulate the functionality of carrying out Pytest tests. The role will generate an Ansible fact, the name of which, is `pytest_result`.
- If `pytest_result` value is '0' means the last tests executed ran all successfully.
- If `pytest_result` value is '1' means that at least one test failed. 
- If `pytest_result` value is '2' means that at some point the Pytest script has crashed.

As the pytest script will receive the required parameters in form of a JSON object. In order to do that the _pytest_tester_ role has a python script that wraps the execution of the Pytest script, enablig the possibility of passing on parameters to the Pytest script and ensuring that the JSON object is pareseable into a Python dict object.


Requirements
------------

The role requires Python3 in the machine and Pytest installed. 
The role has been tested in Fedora 30, RHEL 7 and CentOS7. It does not support Windows environments, Debian based distributions nor RHEL 8 nor CentOS 8.
The role has been tested with Python 3.6.8 and Python 3.7.7

Role Variables
--------------
- `script_test_name`: The name of the Pytest script to run. It is MANDATORY.
- `test_params`: This variable is a dictionary which provides the different parameters that the Pytest script requires. The role converts it into a JSON object and passes it on to the wrapper script, which validates if it is parseable. If everything is okay the JSON object will be passed on to the Pytest script. This variable is OPTIONAL and by default its value is an empty dictionary.

In the file `vars/main.yml` there are the following variables:
- `python_dependencies`: This variable is a list with the different pip3 packages to install so the test to execute can run successfully.

Dependencies
------------
The role requires Python3 in the machine and Pytest installed. 
