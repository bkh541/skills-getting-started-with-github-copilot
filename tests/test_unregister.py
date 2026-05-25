"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
"""

import pytest


def test_unregister_success(client):
    """Test successful unregistration from an activity."""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.delete(
        f"/activities/Chess Club/participants/{email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant."""
    email = "michael@mergington.edu"
    
    # Verify participant is initially there
    activities_response1 = client.get("/activities")
    activities1 = activities_response1.json()
    assert email in activities1["Chess Club"]["participants"]
    
    # Unregister
    response = client.delete(f"/activities/Chess Club/participants/{email}")
    assert response.status_code == 200
    
    # Verify participant was removed
    activities_response2 = client.get("/activities")
    activities2 = activities_response2.json()
    assert email not in activities2["Chess Club"]["participants"]


def test_unregister_nonexistent_activity(client):
    """Test that unregister from non-existent activity returns 404."""
    response = client.delete(
        "/activities/Nonexistent Activity/participants/student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_participant_not_signed_up(client):
    """Test that unregistering non-participant returns error."""
    response = client.delete(
        "/activities/Chess Club/participants/notstudent@mergington.edu"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_increases_available_spots(client):
    """Test that unregister increases available spot count."""
    email = "michael@mergington.edu"
    
    # Get initial state
    activities_response1 = client.get("/activities")
    activities1 = activities_response1.json()
    initial_participants = len(activities1["Chess Club"]["participants"])
    
    # Unregister
    response = client.delete(f"/activities/Chess Club/participants/{email}")
    assert response.status_code == 200
    
    # Get updated state
    activities_response2 = client.get("/activities")
    activities2 = activities_response2.json()
    updated_participants = len(activities2["Chess Club"]["participants"])
    
    # Verify count decreased by 1
    assert updated_participants == initial_participants - 1


def test_unregister_multiple_times_same_participant(client):
    """Test that unregistering twice fails on second attempt."""
    email = "michael@mergington.edu"
    
    # First unregister should succeed
    response1 = client.delete(f"/activities/Chess Club/participants/{email}")
    assert response1.status_code == 200
    
    # Second unregister should fail
    response2 = client.delete(f"/activities/Chess Club/participants/{email}")
    assert response2.status_code == 400


def test_unregister_with_url_encoded_email(client):
    """Test that unregister works with URL-encoded email."""
    email = "michael@mergington.edu"
    encoded_email = "michael%40mergington.edu"
    
    response = client.delete(
        f"/activities/Chess Club/participants/{encoded_email}"
    )
    
    assert response.status_code == 200


def test_unregister_other_participants_unaffected(client):
    """Test that unregistering one participant doesn't affect others."""
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    
    # Get initial state
    activities_response1 = client.get("/activities")
    activities1 = activities_response1.json()
    assert email_to_keep in activities1["Chess Club"]["participants"]
    
    # Unregister one participant
    response = client.delete(
        f"/activities/Chess Club/participants/{email_to_remove}"
    )
    assert response.status_code == 200
    
    # Verify other participant is still there
    activities_response2 = client.get("/activities")
    activities2 = activities_response2.json()
    assert email_to_keep in activities2["Chess Club"]["participants"]
    assert email_to_remove not in activities2["Chess Club"]["participants"]


def test_unregister_response_format(client):
    """Test that unregister response has correct format."""
    email = "michael@mergington.edu"
    
    response = client.delete(
        f"/activities/Chess Club/participants/{email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Response should have a message field
    assert "message" in data
    assert isinstance(data["message"], str)
