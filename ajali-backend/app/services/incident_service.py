from app import db, photos, videos
from app.models import Incident, Media
from datetime import datetime
import os

def create_incident(user_id, title, description, incident_type, latitude, longitude):
    incident = Incident(
        user_id=user_id,
        title=title,
        description=description,
        incident_type=incident_type,
        latitude=latitude,
        longitude=longitude
    )
    
    db.session.add(incident)
    db.session.commit()
    return incident

def update_incident(incident_id, user_id, update_data):
    incident = Incident.query.filter_by(id=incident_id, user_id=user_id).first()
    
    if not incident:
        return None
    
    for key, value in update_data.items():
        if hasattr(incident, key):
            setattr(incident, key, value)
    
    incident.updated_at = datetime.utcnow()
    db.session.commit()
    return incident

def delete_incident(incident_id, user_id):
    incident = Incident.query.filter_by(id=incident_id, user_id=user_id).first()
    
    if not incident:
        return False
    
    db.session.delete(incident)
    db.session.commit()
    return True

def add_media_to_incident(incident_id, user_id, file, media_type):
    incident = Incident.query.filter_by(id=incident_id, user_id=user_id).first()
    
    if not incident:
        return None
    
    if media_type == 'image':
        filename = photos.save(file)
    else:
        filename = videos.save(file)
    
    file_url = os.path.join('uploads', media_type + 's', filename)
    
    media = Media(
        incident_id=incident_id,
        file_url=file_url,
        media_type=media_type
    )
    
    db.session.add(media)
    db.session.commit()
    return media