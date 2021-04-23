Playbook Description
=========
The aim of this playbook is to build and deploy a Docker container. In order to do so, the Ansible playbook will follow the following steps:
1. Validate the container is not already running. If so, the Ansible playbook will skip the rest of tasks.
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

The playbook supports using a non-root user, as long as this one is a sudoer. In order to do this set `ansible_user` variable in path `inventories/docker_server/group_vars/all`.

In order to achieve this, two Ansible roles have been developed:
- docker_container_builder_deployer. This role was developed to encapsulate the functionality of build and deploy Docker containers. It does only support Docker containers, not Podman, either Crio, or others.
- docker_container_test. This role was developed to encapsulate the functionality of executing a pytest script to validate certain checks. The role will create a fact `pytest_result` with the return code of the execution of the pytest script.

All of the roles have their own documentation which can be found in the folder of each role.

This playbook was tested with Ansible version Ansible 2.10.8 and Python version 3.6.8.

The playbook has been tested with the following environments: Fedora 30, RHEL 7, CentOS 7. At this very moment the playbook does not support Debian based distributions neither Windows neither RHEL based distributions higher than 7. 

It is important to highlight that the playbook does not work with CentOS 8 or RHEL 8 because the Docker package of this distribution is based on Podman containers. The playbook has been tested with docker-1.13.1 package in which there are no Podman containers, there is docker daemon and privileged socket "unix://var/run/docker.sock". Therefore, the playbook is not expected to work with rootless containers, athough it could be an interesting improvement.   

Playbook Variables
--------------
The variables can be set in the following files:

Variable file:
- **$PROJECT_ROOT/vars/vars_dependencies.yml**

In this file the variables specified are the following: 
- `python3_dependencies`:
This variable sets the list of pip3 dependencies to install. It is OPTIONAL to specify it. 
- `system_dependencies`:
This variable sets the list of system dependencies to install. It is OPTIONAL to specify it.

Variable file:
- **$PROJECT_ROOT/vars/vars_pytest.yml**

In this file the variables specified are the following:
- `tomcat_script_test_name`:
This variable sets the name of the pytest script to be run. It is MANDATORY to specify it. 
- `tomcat_container_test_params`:
This variable is the dictionary in which the required parameters for the pytest script will be specified. The idea of using a dictionary object is because depending on the test the parameters can be different. 
	
Variable file:
- **$PROJECT_ROOT/vars/vars_tomcat_docker_container.yml**

In this file the variables specified are the following:
- `tomcat_dockerfile_name`:
This variable is the name of the Dockerfile file. It is MANDATORY to specify it.
- `tomcat_docker_image_name`:
This variable is the name of the image to build. It is MANDATORY to specify it.
- `tomcat_docker_image_tag`:
This variable is the tag of the image to build. It is MANDATORY to specify it.
- `tomcat_docker_image_args`:
This variable is a dictionary which sets the differents ARG that will be passed on to the Docker build. It is OPTIONAL to specify it.
- `tomcat_docker_container_name`:
This variable sets the name that will be used to run the Docker container. It is MANDATORY to specify it. 
- `tomcat_docker_container_port`:
This variable sets the port of the Tomcat application to run. It is MANDATORY to specify it.
- `tomcat_docker_container_host_map_port`:
This variable sets the host's port in which the container port Tomcat application will be mapped. It is MANDATORY to specify it.
- `tomcat_docker_container_env`:
This variable sets the environment variables that will be passed on to the container. It is OPTIONAL to specify it.

Group Variables file:
The following variable would specify variables hosts beloning to the group "all".

- **inventories/docker_server/group_vars/all**
- `project_path`:
This variable must not be modified, it parameterizes the root of the project
- `ansible_python_interpreter`:
This variable sets the python interpreter that Ansible will use. In my case I specified `/usr/bin/python3` 
- `ansible_user`:
The playbook supports connecting with a user diferent from root. Nevertheless this user must be sudoer. 

The playbook will also accept the following variables:
- `playbook_serial`: 
Ansible serial for the play in which the tasks to validate, build, run and validate again, will be run. This variable is OPTIONAL. 

Requirements and Dependencies
=========
Before running the playbook one must meet the following requirements:

The following command will install the Ansible dependencies for the Ansible playbook to run:
	$ ansible-galaxy install -r requirements.yml

The following command must run successfully:
	$ ansible docker_host -m ping 

If one of the Ansible managed nodes is CentOS 7, the following command must be executed in that host before running the playbook:

	$ openssl s_client -showcerts -servername registry.access.redhat.com -connect registry.access.redhat.com:443 </dev/null 2>/dev/null | openssl x509 -text > /etc/rhsm/ca/redhat-uep.pem
	
This command is required in CentOS 7 so Docker can pull images from the public Red Hat registry. In my case, the base image of the Tomcat Docker container is ubi8-minimal so this step would be required.
For more information: https://github.com/CentOS/sig-atomic-buildscripts/issues/329

How to run it:
=========
The playbook must always be ran from the root of the project.

	$ ansible-playbook playbooks/deploy_docker_container.yaml -e playbook_serial=1


	$ ansible-playbook playbooks/deploy_docker_container.yaml

To make the Ansible playbook  works: 
- The Dockerfile must be in the path `<project_root>/roles/docker_container_builder_deployer/files`
- The Pytest script must be in the path `<project_root>/roles/docker_container_test/files`
- The playbook must be in the path `<project_root>/playbooks`

Delivery files:
----------------
**Dockerfile:**

You will find the Dockerfile in the path: `<PROJECT_ROOT>/roles/docker_container_builder_deployer/files/Dockerfile.tomcat.ubi8-minimal`
The Dockerfile is based on ubi8-minimal image.

The package tzdata had to be reinstalled in the Dockerfile because of the following bug:
- https://bugzilla.redhat.com/show_bug.cgi?id=1668185
- https://bugzilla.redhat.com/show_bug.cgi?id=1674495
- https://bugzilla.redhat.com/show_bug.cgi?id=1903219

It seems that the files /usr/share/zoneinfo were missing in the ubi8-minimal container image.

**Pytest Scripts:**

You will find the pytest script in the path: `<PROJECT_ROOT/roles/docker_container_test/files`
The pytest script consists of two files:
- wrap_tests.py: 
This python script executes the pytest script. First it validates that the parameters are fine. Afterwards, it executes the pytest script and then collects the result. Depending on the result the script will return a return code.

- test_my_tomcat_docker_container.py
This is the pytest script. This script will always receive a parameter that is going to be a json object with the information the parameters the test needs to run, so this way it can be more generic.

**Ansible Playbook:**

You will find the playbook in the path: `<PROJECT_ROOT>/playbooks`

Project Structure
----------------
```bash
. <project_root>
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

TODO Improvements:
----------------
Tests:
- Support indicating to the wrap_tests.py more than one test to execute with the respective parameters for such test.

Docker build and deploy role:
- The docker_build_and_deploy role will not remove the docker image even if it detects the Dockerfile has changed. Even though it could be controlled I prefer the removal of Docker images to be manual and not performed by this automation mechanism.

- Support for detecting and running Podman containers

- Support for RHEL 8, CentOS 8, CentOS Stream, Debian based Linux distros

- Parametrize logging configuration for Docker containers and may other settings

Very likely there may be many other things to improve :)
