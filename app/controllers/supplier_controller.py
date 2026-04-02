from app.models.supplier_model import Supplier
from app.extensions import db

def check_role(role, allowed_roles):
    if role not in allowed_roles:
        return {'message': 'Access forbidden'}, 403
    return None

def create_supplier(role, data):
    role_error = check_role(role, ['manager', 'admin'])
    if role_error:
        return role_error

    if not data.get('name'):
        return {'message': 'Name required'}, 400

    supplier = Supplier(name=data['name'])
    db.session.add(supplier)
    db.session.commit()
    return {'message': 'Supplier created', 'id': supplier.id}, 201

def get_suppliers(role):
    role_error = check_role(role, ['user', 'manager', 'admin'])
    if role_error:
        return role_error

    suppliers = Supplier.query.all()
    return [
        {'id': s.id, 'name': s.name}
        for s in suppliers
    ], 200

