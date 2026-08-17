import pytest
from fastapi import HTTPException
from app.utils.security import validate_url_security

def test_ssrf_blocking_localhost():
    with pytest.raises(HTTPException) as exc_info:
        validate_url_security("http://localhost:8000/admin")
    assert exc_info.value.status_code == 400
    assert "restricted" in exc_info.value.detail or "blocked" in exc_info.value.detail

def test_ssrf_blocking_private_ip():
    with pytest.raises(HTTPException) as exc_info:
        validate_url_security("http://192.168.1.1/secret")
    assert exc_info.value.status_code == 400

def test_ssrf_blocking_invalid_scheme():
    with pytest.raises(HTTPException) as exc_info:
        validate_url_security("file:///etc/passwd")
    assert exc_info.value.status_code == 400
