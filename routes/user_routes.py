from flask import Blueprint, request, jsonify
from services.user_services import UserService

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not all(k in data for k in ("username", "password", "role")):
        return jsonify({"message": "Missing data"}), 400
    
    response, status = UserService.register_user(data['username'], data['password'], data['role'])
    
    return jsonify(response), status

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not all(k in data for k in ("username", "password")):
        return jsonify({"message": "Missing data"}), 400
    
    response, status = UserService.login_user(data['username'], data['password'])
    
    return jsonify(response), status
