import requests
def test_connection():
    connection_error = False
    timeout_error = False

    try:
        response = requests.get("http://localhost/sample")
    except requests.exceptions.ConnectionError as c:
        connection_error = True
    except requests.exceptions.Timeout as t:
        timeout_error = True

    assert connection_error != True
    assert timeout_error != True

