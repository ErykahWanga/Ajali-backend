# /backend/tests/test_api.py
import json

def get_auth_token(test_client, email, password):
    """Helper function to get an auth token."""
    res = test_client.post('/auth/login', json={'email': email, 'password': password})
    return json.loads(res.data)['access_token']

def test_registration(test_client):
    """Test user registration."""
    res = test_client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert res.status_code == 201
    assert b"User created successfully" in res.data

def test_login(test_client):
    """Test user login and token generation."""
    res = test_client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert res.status_code == 200
    data = json.loads(res.data)
    assert 'access_token' in data

def test_create_incident(test_client):
    """Test incident creation."""
    token = get_auth_token(test_client, 'test@example.com', 'password123')
    headers = {'Authorization': f'Bearer {token}'}
    res = test_client.post('/incidents/', headers=headers, json={
        'title': 'Test Incident',
        'description': 'A test description.',
        'latitude': 1.2921,
        'longitude': 36.8219
    })
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['title'] == 'Test Incident'

def test_get_incidents(test_client):
    """Test fetching all incidents."""
    token = get_auth_token(test_client, 'test@example.com', 'password123')
    headers = {'Authorization': f'Bearer {token}'}
    res = test_client.get('/incidents/', headers=headers)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_update_own_incident(test_client):
    """Test a user updating their own incident."""
    token = get_auth_token(test_client, 'test@example.com', 'password123')
    headers = {'Authorization': f'Bearer {token}'}
    # Assumes incident with id=1 was created by testuser
    res = test_client.put('/incidents/1', headers=headers, json={'title': 'Updated Title'})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['title'] == 'Updated Title'

def test_admin_update_status(test_client):
    """Test an admin updating an incident status."""
    admin_token = get_auth_token(test_client, 'admin@example.com', 'password123')
    headers = {'Authorization': f'Bearer {admin_token}'}
    res = test_client.put('/admin/incidents/1/status', headers=headers, json={'status': 'resolved'})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == 'resolved'

def test_non_admin_update_status_fails(test_client):
    """Test that a non-admin cannot update status."""
    user_token = get_auth_token(test_client, 'test@example.com', 'password123')
    headers = {'Authorization': f'Bearer {user_token}'}
    res = test_client.put('/admin/incidents/1/status', headers=headers, json={'status': 'resolved'})
    assert res.status_code == 403
    assert b"Admins only!" in res.data