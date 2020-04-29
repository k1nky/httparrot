import requests
import pytest

def test_status_code():
    resp = requests.get("http://localhost:8000")
    assert resp.status_code == 200

def test_echo_header():
    resp = requests.get(url="http://localhost:8000", headers={'X-Test': 'value'})
    assert "X-Test" in resp.text
    assert "value" in resp.text

def test_echo_body():
    resp = requests.post(url="http://localhost:8000", data={'_key_': '_value_'})
    assert "POST" in resp.text
    assert "_key_" in resp.text
    assert "_value_" in resp.text

