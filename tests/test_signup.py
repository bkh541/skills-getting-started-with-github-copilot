"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_success(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds the participant to the activity."""
    email = "newstudent@mergington.edu"
    
    # Signup
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_participant(client):
    """Test that duplicate signup returns an error."""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity(client):
    """Test that signup to non-existent activity returns 404."""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_invalid_email_format_accepted(client):
    """Test that signup accepts any email format (validation is client-side)."""
    response = client.post(
        "/activities/Chess Club/signup?email=bademail@test"
    )
    
    # Backend accepts any string as email
    assert response.status_code == 200


def test_signup_multiple_activities_same_student(client):
    """Test that a student can sign up for multiple activities."""
    email = "newstudent@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(f"/activities/Programming Class/signup?email={email}")
    assert response2.status_code == 200
    
    # Verify participant is in both activities
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_signup_decreases_available_spots(client):
    """Test that signup decreases the available spot count."""
    email = "newstudent@mergington.edu"
    
    # Get initial state
    activities_response1 = client.get("/activities")
    activities1 = activities_response1.json()
    initial_participants = len(activities1["Chess Club"]["participants"])
    
    # Sign up
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    
    # Get updated state
    activities_response2 = client.get("/activities")
    activities2 = activities_response2.json()
    updated_participants = len(activities2["Chess Club"]["participants"])
    
    # Verify count increased by 1
    assert updated_participants == initial_participants + 1


def test_signup_with_url_encoded_activity_name(client):
    """Test that signup works with URL-encoded activity names."""
    response = client.post(
        "/activities/Basketball%20Team/signup?email=newstudent@mergington.edu"
    )
    
    # Should work with encoded space
    assert response.status_code == 200


def test_signup_response_format(client):
    """Test that signup response has correct format."""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Response should have a message field
    assert "message" in data
    assert isinstance(data["message"], str)
