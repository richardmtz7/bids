from flask import Blueprint, request, jsonify
from services.operation_services import OperationService

operation_bp = Blueprint('operation_bp', __name__)

@operation_bp.route('/create', methods=['POST'])
def create_operation():
    data = request.get_json()

    required_fields = ["amount_required", "annual_interest", "deadline"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required data"}), 400
    
    try:
        response, status = OperationService.create_operation(
            amount_required=data['amount_required'],
            annual_interest=data['annual_interest'],
            deadline=data['deadline']
        )
        return jsonify(response), status
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@operation_bp.route('/list', methods=['GET'])
def list_operations():
    response, status = OperationService.list_active_operations()
    return jsonify(response), status
