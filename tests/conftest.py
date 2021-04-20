import pytest

@pytest.fixture
def container_name_1():
    return "testtomcat"

@pytest.fixture
def container_name_2():
    return "testtomcat2"

@pytest.fixture
def container_name_3():
    return "testtomcat3"

@pytest.fixture
def tomcat_url_2():
    tomcat="http://localhost:8080/test_failed"
    return tomcat

@pytest.fixture
def tomcat_url_3():
    tomcat="http://localhost:8082/sample"
    return tomcat
