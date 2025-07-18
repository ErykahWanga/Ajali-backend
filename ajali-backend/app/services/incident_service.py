# /app/services/incident_service.py

from ..models import Incident
from ..utils.database import db
from .notification_service import send_status_update_notification

def create_incident(data, user_id):
    new_incident = Incident(
        title=data['title'],
        description=data['description'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        media_url=data.get('media_url'),
        video_url=data.get('video_url'),
        user_id=user_id
    )
    db.session.add(new_incident)
    db.session.commit()
    return new_incident

def get_all_incidents():
    return Incident.query.order_by(Incident.created_at.desc()).all()

def get_incident_by_id(incident_id):
    return Incident.query.get(incident_id)

def update_incident(incident, data):
    incident.title = data.get('title', incident.title)
    incident.description = data.get('description', incident.description)
    incident.latitude = data.get('latitude', incident.latitude)
    incident.longitude = data.get('longitude', incident.longitude)
    db.session.commit()
    return incident

def delete_incident(incident):
    db.session.delete(incident)
    db.session.commit()

def update_incident_status(incident, status):
    allowed_statuses = ['under_investigation', 'rejected', 'resolved']
    if status not in allowed_statuses:
        return None # Invalid status
        
    incident.status = status
    db.session.commit()
    # Send a notification about the status change
    send_status_update_notification(incident)
    return incident