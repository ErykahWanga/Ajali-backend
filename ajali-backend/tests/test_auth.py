# /tests/test_auth.py

import json

def test_register(client):
    res = client.post('/auth/register', data=json.dumps({
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }), content_type='application/json')
    assert res.status_code == 201
    assert 'User created successfully' in res.get_data(as_text=True)

def test_login(client):
    # First, register a user to log in with
    client.post('/auth/register', data=json.dumps({
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'password123'
    }), content_type='application/json')
    
    # Now, test login
    res = client.post('/auth/login', data=json.dumps({
        'username': 'loginuser',
        'password': 'password123'
    }), content_type='application/json')
    assert res.status_code == 200
    assert 'access_token' in res.get_json()