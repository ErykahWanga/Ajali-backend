# /backend/routes/admin_routes.py
from flask import jsonify, Blueprint, request
from models import db, Incident, IncidentStatus
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__)

# Custom decorator to check for admin role
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("is_admin"):
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403
        return decorator
    return wrapper


@admin_bp.route('/incidents/<int:id>/status', methods=['PUT'])
@jwt_required()
@admin_required()
def update_incident_status(id):
    incident = Incident.query.get_or_404(id)
    data = request.get_json()
    new_status_str = data.get('status')

    if not new_status_str:
        return jsonify({"msg": "Missing status field"}), 400

    try:
        # Validate that the new status is a valid member of the IncidentStatus enum
        new_status_enum = IncidentStatus(new_status_str)
    except ValueError:
        valid_statuses = [s.value for s in IncidentStatus]
        return jsonify({"msg": f"Invalid status. Must be one of: {valid_statuses}"}), 400

    incident.status = new_status_enum
    db.session.commit()

    return jsonify(incident.to_dict()), 200