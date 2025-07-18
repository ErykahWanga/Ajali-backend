# /app/routes/incident_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import incident_service

incident_bp = Blueprint('incident_bp', __name__)

@incident_bp.route('/incidents', methods=['POST'])
@jwt_required()
def create_incident():
    data = request.get_json()
    # Basic validation
    required_fields = ['title', 'description', 'latitude', 'longitude']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    user_id = get_jwt_identity()
    incident = incident_service.create_incident(data, user_id)
    return jsonify(incident.to_dict()), 201

@incident_bp.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = incident_service.get_all_incidents()
    return jsonify([incident.to_dict() for incident in incidents]), 200

@incident_bp.route('/incidents/<int:id>', methods=['GET'])
def get_incident(id):
    incident = incident_service.get_incident_by_id(id)
    if not incident:
        return jsonify({"msg": "Incident not found"}), 404
    return jsonify(incident.to_dict()), 200

@incident_bp.route('/incidents/<int:id>', methods=['PUT'])
@jwt_required()
def update_incident(id):
    user_id = get_jwt_identity()
    incident = incident_service.get_incident_by_id(id)

    if not incident:
        return jsonify({"msg": "Incident not found"}), 404
    if incident.user_id != user_id:
        return jsonify({"msg": "Forbidden: You can only edit your own incidents"}), 403

    data = request.get_json()
    updated_incident = incident_service.update_incident(incident, data)
    return jsonify(updated_incident.to_dict()), 200

@incident_bp.route('/incidents/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_incident(id):
    user_id = get_jwt_identity()
    incident = incident_service.get_incident_by_id(id)

    if not incident:
        return jsonify({"msg": "Incident not found"}), 404
    if incident.user_id != user_id:
        return jsonify({"msg": "Forbidden: You can only delete your own incidents"}), 403

    incident_service.delete_incident(incident)
    return jsonify({"msg": "Incident deleted successfully"}), 200