from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Incident, Media
from app.services.incident_service import (
    create_incident,
    update_incident,
    delete_incident,
    add_media_to_incident
)
from app.utils.helpers import validate_coordinates

incident_bp = Blueprint('incidents', __name__)

@incident_bp.route('', methods=['POST'])
@jwt_required()
def report_incident():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'incident_type', 'latitude', 'longitude']
    if not all(key in data for key in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not validate_coordinates(data['latitude'], data['longitude']):
        return jsonify({'error': 'Invalid coordinates'}), 400
    
    incident = create_incident(
        user_id=user_id,
        title=data['title'],
        description=data['description'],
        incident_type=data['incident_type'],
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    
    return jsonify(incident.to_dict()), 201

@incident_bp.route('/<int:incident_id>', methods=['PUT'])
@jwt_required()
def update_incident_route(incident_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'latitude' in data and 'longitude' in data:
        if not validate_coordinates(data['latitude'], data['longitude']):
            return jsonify({'error': 'Invalid coordinates'}), 400
    
    updated_incident = update_incident(incident_id, user_id, data)
    
    if not updated_incident:
        return jsonify({'error': 'Incident not found or unauthorized'}), 404
    
    return jsonify(updated_incident.to_dict())

@incident_bp.route('/<int:incident_id>', methods=['DELETE'])
@jwt_required()
def delete_incident_route(incident_id):
    user_id = get_jwt_identity()
    success = delete_incident(incident_id, user_id)
    
    if not success:
        return jsonify({'error': 'Incident not found or unauthorized'}), 404
    
    return jsonify({'message': 'Incident deleted successfully'}), 200

@incident_bp.route('/<int:incident_id>/media', methods=['POST'])
@jwt_required()
def add_media(incident_id):
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    media_type = request.form.get('media_type', 'image')
    
    if media_type not in ['image', 'video']:
        return jsonify({'error': 'Invalid media type'}), 400
    
    media = add_media_to_incident(incident_id, user_id, file, media_type)
    
    if not media:
        return jsonify({'error': 'Failed to add media or unauthorized'}), 400
    
    return jsonify(media.to_dict()), 201