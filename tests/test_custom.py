import pytest
import requests

def test_custom_header():
    resp = requests.get(url="http://localhost:8000")
    assert "X-Test" in resp.headers
    assert resp.headers["X-Test"] == "value"

def test_custom_body():
    resp = requests.get(url="http://localhost:8000")
    assert "MY_BODY" in resp.text