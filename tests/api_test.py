from flask.testing import FlaskClient


def test_handle_user_event_missing_data(client: FlaskClient) -> None:
    """Test API returns 415 when no JSON data is provided"""
    response = client.post("/event")
    assert response.status_code == 415
    assert response.json == None

def test_handle_user_event_missing_required_field(client: FlaskClient) -> None:
    """Test API returns 400 when required field is missing"""
    response = client.post("/event", json={
        "amount": 100,
        "user_id": 1,
        "time": 1000
        # Missing 'type' field
    })
    assert response.status_code == 400
    assert "Missing required field: type" in response.json["error"]


def test_handle_user_event_invalid_event_type(client: FlaskClient) -> None:
    """Test API returns 400 when event type is invalid"""
    response = client.post("/event", json={
        "type": "invalid_type",
        "amount": 100,
        "user_id": 1,
        "time": 1000
    })
    assert response.status_code == 400
    assert response.json == {"error": "type must be 'deposit' or 'withdraw'"}


def test_handle_user_event_valid_deposit(client: FlaskClient) -> None:
    """Test valid deposit request returns 200 with empty alert codes"""
    response = client.post("/event", json={
        "type": "deposit",
        "amount": 50,
        "user_id": 1,
        "time": 1000
    })
    assert response.status_code == 200
    assert response.json == {"alert_codes": []}


def test_handle_user_event_withdrawal_over_100(client: FlaskClient) -> None:
    """Test withdrawal over 100 triggers alert code 1100"""
    response = client.post("/event", json={
        "type": "withdraw",
        "amount": 150,
        "user_id": 2,
        "time": 1000
    })
    assert response.status_code == 200
    assert response.json == {"alert_codes": [1100]}


def test_handle_user_event_withdrawal_exactly_100(client: FlaskClient) -> None:
    """Test withdrawal of exactly 100 does NOT trigger alert"""
    response = client.post("/event", json={
        "type": "withdraw",
        "amount": 100,
        "user_id": 3,
        "time": 1000
    })
    assert response.status_code == 200
    assert response.json == {"alert_codes": []}