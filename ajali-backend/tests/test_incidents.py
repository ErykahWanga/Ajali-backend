# /tests/test_incidents.py

import json

def get_auth_token(client, username='testincidentuser', password='password123', email='incident@test.com'):
    """Helper to register and login a user to get a token."""
    client.post('/auth/register', data=json.dumps(dict(username=username, email=email, password=password)), content_type='application/json')
    res = client.post('/auth/login', data=json.dumps(dict(username=username, password=password)), content_type='application/json')
    return res.get_json()['access_token']

def test_create_incident(client):
    token = get_auth_token(client)
    headers = {'Authorization': f'Bearer {token}'}
    incident_data = {
        'title': 'Test Incident',
        'description': 'A test incident description.',
        'latitude': 1.23,
        'longitude': 4.56
    }
    res = client.post('/api/incidents', data=json.dumps(incident_data), headers=headers, content_type='application/json')
    assert res.status_code == 201
    assert res.get_json()['title'] == 'Test Incident'

def test_get_all_incidents(client):
    res = client.get('/api/incidents')
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_update_own_incident(client):
    token = get_auth_token(client, username="owner", email="owner@test.com")
    headers = {'Authorization': f'Bearer {token}'}
    # Create an incident
    incident_res = client.post('/api/incidents', data=json.dumps({
        'title': 'Original Title', 'description': 'desc', 'latitude': 1, 'longitude': 1
    }), headers=headers, content_type='application/json')
    incident_id = incident_res.get_json()['id']

    # Update it
    update_res = client.put(f'/api/incidents/{incident_id}', data=json.dumps({
        'title': 'Updated Title'
    }), headers=headers, content_type='application/json')
    assert update_res.status_code == 200
    assert update_res.get_json()['title'] == 'Updated Title'