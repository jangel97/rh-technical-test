Ansible Role docker_container_builder_deployer
=========
The aim of this role is to encapsulate the functionality of building and deploying Docker containers. 

In case exists a Docker image with the name and tag specified in the role variables. The role will not delete the existing Docker image to replace it with the one to build, even if Ansible detects that the Dockerfile has changed.

The role only supports Docker containers, as it interacts with the docker server to build and deploy the container.

Requirements
------------
There should be a Dockerfile ubicated under the `files/` directory.

Docker service must be runnning. 

The role has been tested in Fedora 30, RHEL 7 and CentOS7. It does not support Windows environments, Debian based distributions nor RHEL 8 nor CentOS 8.

Role Variables
--------------
- `dockerfile_name`: This variable indicates the name of the Dockerfile file. Remember it must be located under the `files/` directory. This variable is MANDATORY.
- `docker_image_args`: This variable is a dictionary which specifies the Docker ARG passed on to the Docker build. This variable is OPTIONAL. (By default empty dictionary).
- `image_name`: This variable indicates the name of the Docker image to build. It is MANDATORY.
- `image_tag`: This variable indicates the name of the Docker tag to build. It is MANDATORY.
- `container_name`: This variable indicates the name of the Docker container to run. It is MANDATORY.
- `container_port`: This variable indicates the port exposed by the Docker container. It is MANDATORY.
- `host_map_port`: This variable indicates the host's port in which the container port will be mapped. It is MANDATORY.
- `container_env`: This variable is a dictionary which specifies the Docker ENV passed on to the Docker container. This variable is optional. (By default empty dictionary).
- `container_run_detach`: This variable specifies if the container is going to be run with the `detach` option. It is optional. (By default is yes).
- `container_cleanup`: Use with detach=false to remove the container after successful execution. (By default is yes).
- `container_default_behaviour`:  Various module options used to have default values. This causes problems with containers which use different values for these options.
The default value is compatibility, which will ensure that the default values are used when the values are not explicitly specified by the user.
From community.docker 2.0.0 on, the default value will switch to no_defaults.
(By default is no_defaults).
For more information about this option check on this link: https://docs.ansible.com/ansible/latest/collections/community/docker/docker_container_module.html#parameter-container_default_behavior

Dependencies
------------

The role depends on the collection `community.docker`. Before using it run the following command:
    $ ansible-galaxy collection install community.docker
