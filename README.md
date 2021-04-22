Playbook Description
=========
The aim of this playbook is to build and deploy a Docker container. In order to do so, the Ansible playbook will follow the following steps:
1. Validate the container is not already running. If so, the Ansible playbook will not continue.
2. Build the Docker image and deploy it.
3. Validate the container was successfully deployed and print its status. 

The playbook is idempotent, so it can be run multiple times without failure.

This playbook is parameterized to offer extensibility when it comes to the following aspects:
- Dependencies to install before running:
	- python3 dependencies
	- system dependencies
- Pytest variables. Variables to run the test, as it is parameterized:
	- name of pytest script to execute
	- dictionary containing information required by the test to run. The parameters for the test to run will be specified in a YAML dictionary. 
- Docker image and Docker container variables. The following variables correspond to the parameters to build and deploy the container:
	- Dockerfile name. The name of the Dockerfile file.
	- Container name. Name of the Docker container to deploy.
	- Container port. Port that the container is going to use to expose the application.
	- Port to map in host. Port of the host machine in which container's exposed port will be mapped.
	- Dockerfile image args. Will translate in "ARG" command in Dockerfile. A dictionary will be used to pass on the ARGs to build the Docker image.
	- Docker container environment variables. Will translate in "ENV" command in Dockerfile. A dictionary will be used to pass on the ENVs.


The playbook supports using a non-root user, as long as this one is a sudoer. In order to do this set 'ansible_user' variable in path inventories/docker_server/group_vars/all.

This playbook was tested with Ansible version ansible 2.10.8 and Python version 3.6.8.

The playbook has been tested with the following environments: Fedora 30, RHEL 7, CentOS 7. At this very moment the playbook does not support Debian based distributions neither Windows neither RHEL based distributions higher than 7. 
It is important to highlight that the playbook does not work with CentOS 8 or RHEL 8 because the Docker package of this distribution is based on Podman containers. The playbook has been tested with docker-1.13.1 package in which there are no Podman containers, there is docker daemon and privileged socket "unix://var/run/docker.sock". Therefore, the playbook is not expected to work with rootless containers, athough it could be an interesting improvement.   


Requirements
=========
Before running the playbook one must meet the following requirements:

	The following command will install the Ansible dependencies for the Ansible playbook to run:
	$ ansible-galaxy install -r requirements.yml

	The following command must run successfully:
	$ ansible docker_host -m ping 

	If one of the ansible managed nodes is CentOS 7, the following command must be executed in that host before running the playbook:
	$ openssl s_client -showcerts -servername registry.access.redhat.com -connect registry.access.redhat.com:443 </dev/null 2>/dev/null | openssl x509 -text > /etc/rhsm/ca/redhat-uep.pem
	This command is required in CentOS 7 so Docker can pull images from the public Red Hat registry. In my case, the base image of the Tomcat Docker container is ubi8-minimal so this step would be required.
	For more information: https://github.com/CentOS/sig-atomic-buildscripts/issues/329


Playbook Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

ansible_user
project_path

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Project Structure
----------------
```bash
.
├── ansible.cfg
├── inventories/
│   └── docker_server/
│       ├── group_vars/
│       │   └── all
│       └── host
├── playbooks/
│   └── deploy_docker_container.yaml
├── README.md
├── requirements.yml
├── roles/
│   ├── docker_container_builder_deployer/
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   │   └── Dockerfile.tomcat.ubi8-minimal
│   │   ├── README.md
│   │   └── tasks/
│   │       ├── 00_assert_required_vars.yml
│   │       ├── 01_build_container_image.yml
│   │       ├── 02_run_container_image.yml
│   │       └── main.yml
│   └── docker_container_test/
│       ├── files/
│       │   ├── test_my_tomcat_docker_container.py
│       │   └── wrap_tests.py
│       ├── README.md
│       ├── tasks/
│       │   ├── 00_assert_required_vars.yml
│       │   ├── 01_install_dependencies.yml
│       │   ├── 02_copy_test_files.yml
│       │   ├── 03_do_test.yml
│       │   └── main.yml
│       └── vars/
│           └── main.yml
└── vars/
    ├── vars_dependencies.yml
    ├── vars_pytest.yml
    └── vars_tomcat_docker_container.yml
```


How to run it:
----------------

	$ ansible-playbook playbooks/deploy_docker_container.yaml -e playbook_serial=1
	$ ansible-playbook playbooks/deploy_docker_container.yaml

TODO Improvements:
----------------
Tests:
- Support indicating to the wrap_tests.py more than one test to execute with the respective parameters for such test.

*) continuar comentando 
*) README principal, readme roles
