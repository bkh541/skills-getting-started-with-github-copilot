"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all 9 activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Should have 9 activities
    assert len(activities) == 9
    
    # Verify specific activities are present
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    assert "Soccer Club" in activities
    assert "Basketball Team" in activities
    assert "Drama Club" in activities
    assert "Art Club" in activities
    assert "Debate Team" in activities
    assert "Science Club" in activities


def test_get_activities_includes_required_fields(client):
    """Test that each activity includes all required fields."""
    response = client.get("/activities")
    activities = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict), f"{activity_name} should be a dict"
        assert required_fields.issubset(
            activity_data.keys()
        ), f"{activity_name} missing required fields"
        
        # Validate field types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_participants_are_strings(client):
    """Test that participant lists contain only email strings."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str), \
                f"Participant in {activity_name} should be a string"
            assert "@" in participant, \
                f"Participant in {activity_name} should be an email"


def test_get_activities_initial_state(client):
    """Test that activities have correct initial participant counts."""
    response = client.get("/activities")
    activities = response.json()
    
    # Verify some known initial states
    assert len(activities["Chess Club"]["participants"]) == 2
    assert len(activities["Programming Class"]["participants"]) == 2
    assert len(activities["Soccer Club"]["participants"]) == 1
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    assert "emma@mergington.edu" in activities["Programming Class"]["participants"]
