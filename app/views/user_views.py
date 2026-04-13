from flask import Blueprint, request, jsonify, session
from ..controllers.user_controller import register, login, get_users, get_user
from ..utils.auth import roles_required

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

@user_bp.route('/', methods=['GET'])
@roles_required('user', 'manager', 'admin')
def get_all():
    role = session.get('role')
    result, status = get_users(role)
    response = jsonify(result)
    response.status_code = status
    return response

@user_bp.route('/<int:id>', methods=['GET'])
@roles_required('user', 'manager', 'admin')
def get_one(id):
    role = session.get('role')
    result, status = get_user(id, role)
    response = jsonify(result)
    response.status_code = status
    return response

