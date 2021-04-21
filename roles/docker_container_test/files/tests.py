import requests, pytest, docker, sys

PYTHON_SUPPORTED_VERSION = 3
"""
Validate python major version is 3
"""
assert sys.version_info.major == PYTHON_SUPPORTED_VERSION

"""
Validate number of parameters
"""

NUMBER_OF_PARAMS = 7
assert len(sys.argv) == NUMBER_OF_PARAMS

container_name = sys.argv[2]
http_scheme = sys.argv[3]
host = sys.argv[4]
port = sys.argv[5]
url_path = sys.argv[6]

@pytest.mark.parametrize("url",[(http_scheme+"://"+host+":"+port)])
def test_connection_check(url):
    connection_error = False
    timeout_error = False

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as c:
        connection_error = True
    except requests.exceptions.Timeout as t:
        timeout_error = True

    assert connection_error != True
    assert timeout_error != True


@pytest.mark.parametrize("tomcat_url",[(http_scheme+"://"+host+":"+port+"/"+url_path)])
def test_status_code_check(tomcat_url):
    response = requests.get(tomcat_url)
    assert response.status_code == 200

@pytest.mark.parametrize("container_name",[(container_name)])
def test_container_running_check(container_name):
    """
    verify the status of a sniffer container by it's name
    :param container_name: the name of the container
    """
    DOCKER_CLIENT = docker.DockerClient(base_url='unix://var/run/docker.sock')
    container = DOCKER_CLIENT.containers.get(container_name)
    assert container.status == "running"
