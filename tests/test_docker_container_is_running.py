import docker
def is_running(container_name):
    """
    verify the status of a sniffer container by it's name
    :param container_name: the name of the container
    :return: Boolean if the status is ok
    """
    DOCKER_CLIENT = docker.DockerClient(base_url='unix://var/run/docker.sock')
    container = DOCKER_CLIENT.containers.get(container_name)
    assert container.status != "running"

