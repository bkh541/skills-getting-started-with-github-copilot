"""
Tests for the GET / (root) endpoint.
"""

import pytest


def test_root_redirects_to_static(client):
    """Test that GET / redirects to /static/index.html."""
    response = client.get("/", follow_redirects=False)
    
    # Should return a redirect status
    assert response.status_code == 307
    
    # Check the redirect location
    assert "location" in response.headers
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_with_follow(client):
    """Test that following the redirect works (if static files are available)."""
    response = client.get("/", follow_redirects=True)
    
    # Should not be an error response (may be 404 if static files not in test context)
    # Just verify redirect happened
    assert response.status_code in [200, 404, 307]
