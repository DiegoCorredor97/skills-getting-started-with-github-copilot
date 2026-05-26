"""
Test suite for Mergington High School Activities API
Uses AAA (Arrange-Act-Assert) pattern for test structure
"""


def test_get_activities(client):
    """
    Test GET /activities endpoint
    Arrange: Client ready
    Act: Send GET request to /activities
    Assert: Status 200, response contains activities dictionary
    """
    # Arrange
    # (client fixture is ready)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]
    assert "max_participants" in activities["Chess Club"]


def test_signup_for_activity(client):
    """
    Test POST /activities/{activity}/signup endpoint
    Arrange: Valid email and activity name
    Act: Send POST request to signup endpoint
    Assert: Status 200, participant added to activity
    """
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Science Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    
    # Verify participant was added by checking activities endpoint
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity]["participants"]


def test_unregister_from_activity(client):
    """
    Test DELETE /activities/{activity}/unregister endpoint
    Arrange: Existing participant from initial data
    Act: Send DELETE request to unregister endpoint
    Assert: Status 200, participant removed from activity
    """
    # Arrange
    email = "michael@mergington.edu"  # From initial data
    activity = "Chess Club"
    
    # Get initial participant count
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity]["participants"]
    initial_count = len(initial_participants)
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    
    # Verify participant was removed
    final_response = client.get("/activities")
    final_participants = final_response.json()[activity]["participants"]
    assert len(final_participants) == initial_count - 1
    assert email not in final_participants
