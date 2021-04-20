import requests
def test_status_code():
    response = requests.get("http://localhost:8080/sample")
    assert response.status_code == 200
