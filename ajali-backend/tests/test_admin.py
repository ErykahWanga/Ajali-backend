# /tests/test_admin.py

import json
from app.models import User
from app.utils.database import db

def get_token(client, username, password, is_admin=False):
    """Helper to create user and get token."""
    user = User(username=username, email=f"{username}@test.com", is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    res = client.post('/auth/login', data=json.dumps(dict(username=username, password=password)), content_type='application/json')
    return res.get_json()['access_token']

def test_admin_update_status(client):
    # 1. Create a regular user and an incident
    user_token = get_token(client, 'regularuser', 'pw123')
    user_headers = {'Authorization': f'Bearer {user_token}'}
    incident_res = client.post('/api/incidents', data=json.dumps({
        'title': 'Incident to test admin', 'description': 'desc', 'latitude': 1, 'longitude': 1
    }), headers=user_headers, content_type='application/json')
    incident_id = incident_res.get_json()['id']

    # 2. Try to update status as a regular user (should fail)
    fail_res = client.put(f'/api/admin/incidents/{incident_id}/status', data=json.dumps({'status': 'resolved'}), headers=user_headers, content_type='application/json')
    assert fail_res.status_code == 403

    # 3. Create an admin user and get token
    admin_token = get_token(client, 'adminuser', 'pw123', is_admin=True)
    admin_headers = {'Authorization': f'Bearer {admin_token}'}
    
    # 4. Update status as admin (should succeed)
    success_res = client.put(f'/api/admin/incidents/{incident_id}/status', data=json.dumps({'status': 'resolved'}), headers=admin_headers, content_type='application/json')
    assert success_res.status_code == 200
    assert success_res.get_json()['status'] == 'resolved'