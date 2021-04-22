import json, requests, pytest, docker, sys

PYTHON_SUPPORTED_VERSION = 3
"""
Validate python major version is 3
"""
assert sys.version_info.major == PYTHON_SUPPORTED_VERSION

"""
Validate number of parameters
"""
NUMBER_OF_PARAMS = 3
assert len(sys.argv) == NUMBER_OF_PARAMS

"""
Convert json in dict object
"""
try:
  test_info = json.loads(sys.argv[2])
except:
    sys.exit(2)


"""
Validate if dictionary has required keys
"""

assert "container_name" in test_info
assert "http_scheme" in test_info
assert "host" in test_info
assert "port" in test_info
assert "url_path" in test_info

"""
Get keys from dict object
"""
container_name = test_info["container_name"]
http_scheme = test_info["http_scheme"]
host = test_info["host"]
port = test_info["port"]
url_path = test_info["url_path"]



"""
Pytest tests
"""
@pytest.mark.parametrize("url",[(http_scheme+"://"+host+":"+port)])
def test_connection_check(url):
    """
    Check connection with specific host and port
    """
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
    """
    Check status HTTP code of specific endpoint
    :param tomcat_url: endpoint to validate
    """
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
