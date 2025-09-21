"""
Various tests
"""

import pytest

# ----------------------
# is_on_pypi
# ----------------------

from mkdocs_macros.util import is_on_pypi  # Replace with actual import path

def test_known_package_exists():
    # requires connection
    assert is_on_pypi("requests", fail_silently=True) is True

def test_nonexistent_package():
    assert is_on_pypi("this_package_does_not_exist_123456", fail_silently=True) is False

def test_network_failure(monkeypatch):
    # Simulate network failure by patching requests.get to raise a RequestException
    import requests

    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Simulated network failure")

    monkeypatch.setattr(requests, "get", mock_get)

    assert is_on_pypi("requests", fail_silently=True) is False

    with pytest.raises(RuntimeError):
        is_on_pypi("requests", fail_silently=False)
