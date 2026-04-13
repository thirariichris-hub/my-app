from app.models.product_model import Product
from app.models.category_model import Category
from app.models.supplier_model import Supplier
from app.extensions import db

def check_role(role, allowed_roles):
    if not role or role not in allowed_roles:
        return {'message': 'Access forbidden'}, 403
    return None

def create_product(role, data):
    role_error = check_role(role, ['manager', 'admin'])
    if role_error:
        return role_error

    if not all(k in data for k in ['name', 'quantity', 'category_id']):
        return {'message': 'name, quantity, category_id required'}, 400

    category = Category.query.get(data.get('category_id'))
    if not category:
        return {'message': 'Invalid category_id'}, 400

    supplier_id = data.get('supplier_id')
    if supplier_id:
        supplier = Supplier.query.get(supplier_id)
        if not supplier:
            return {'message': 'Invalid supplier_id'}, 400

    product = Product(
        name=data['name'],
        quantity=data['quantity'],
        category_id=data['category_id'],
        supplier_id=supplier_id
    )
    db.session.add(product)
    db.session.commit()
    return {'message': 'Product created', 'id': product.id}, 201

def get_products(role):
    role_error = check_role(role, ['user', 'manager', 'admin'])
    if role_error:
        return role_error

    products = Product.query.all()
    return [
        {
            'id': p.id,
            'name': p.name,
            'quantity': p.quantity,
            'category_id': p.category_id,
            'supplier_id': p.supplier_id
        }
        for p in products
    ], 200

def update_product(id, role, data):
    role_error = check_role(role, ['manager', 'admin'])
    if role_error:
        return role_error

    product = Product.query.get_or_404(id)

    if 'name' in data:
        product.name = data['name']
    if 'quantity' in data:
        product.quantity = data['quantity']
    if 'category_id' in data:
        category = Category.query.get(data['category_id'])
        if not category:
            return {'message': 'Invalid category_id'}, 400
        product.category_id = data['category_id']
    if 'supplier_id' in data:
        supplier = Supplier.query.get(data['supplier_id'])
        if not supplier:
            return {'message': 'Invalid supplier_id'}, 400
        product.supplier_id = data['supplier_id']

    db.session.commit()
    return {'message': 'Product updated'}, 200

def delete_product(id, role):
    role_error = check_role(role, ['admin'])
    if role_error:
        return role_error

    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return {'message': 'Product deleted'}, 200
