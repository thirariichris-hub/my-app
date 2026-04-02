from flask import Blueprint, request, jsonify, session
from ..utils.auth import roles_required
from ..controllers.product_controller import create_product, get_products, update_product, delete_product

product_bp = Blueprint('products', __name__, url_prefix='/api/products')

@product_bp.route('/', methods=['POST'])
@roles_required('admin', 'manager')
def create():
    data = request.get_json()
    role = session.get('role')
    result, status = create_product(role, data)
    response = jsonify(result)
    response.status_code = status
    return response

@product_bp.route('/', methods=['GET'])
@roles_required('admin', 'manager', 'user')
def get_all():
    result, status = get_products(session.get('role'))
    response = jsonify(result)
    response.status_code = status
    return response

@product_bp.route('/<int:id>', methods=['PUT'])
@roles_required('manager', 'admin')
def update(id):
    data = request.get_json()
    role = session.get('role')
    result, status = update_product(id, role, data)
    response = jsonify(result)
    response.status_code = status
    return response

@product_bp.route('/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete(id):
    role = session.get('role')
    result, status = delete_product(id, role)
    response = jsonify(result)
    response.status_code = status
    return response

