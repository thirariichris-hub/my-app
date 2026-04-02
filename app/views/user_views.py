from flask import Blueprint, request, jsonify, session
from ..controllers.user_controller import register, login

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/register', methods=['POST'])
def register_view():
    data = request.get_json()
    result, status = register(data)
    response = jsonify(result)
    response.status_code = status
    return response

@user_bp.route('/login', methods=['POST'])
def login_view():
    data = request.get_json()
    result, status = login(data)
    if status == 200:
        session['role'] = result['role']
    response = jsonify(result)
    response.status_code = status
    return response

