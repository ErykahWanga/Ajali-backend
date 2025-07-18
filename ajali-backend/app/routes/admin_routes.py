# /app/routes/admin_routes.py

from flask import Blueprint, request, jsonify
from ..services import incident_service
from ..utils.helpers import admin_required

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/incidents/<int:id>/status', methods=['PUT'])
@admin_required()
def update_incident_status(id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({"msg": "Status is required"}), 400

    incident = incident_service.get_incident_by_id(id)
    if not incident:
        return jsonify({"msg": "Incident not found"}), 404

    updated_incident = incident_service.update_incident_status(incident, new_status)
    if not updated_incident:
        return jsonify({"msg": f"Invalid status provided. Must be one of: under_investigation, rejected, resolved"}), 400
        
    return jsonify(updated_incident.to_dict()), 200