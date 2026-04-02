from app.models.transaction_model import Transaction
from app.models.product_model import Product
from app.extensions import db

def check_role(role, allowed_roles):
    if role not in allowed_roles:
        return {'message': 'Access forbidden'}, 403
    return None

def stock_movement(role, data):
    role_error = check_role(role, ['manager', 'admin'])
    if role_error:
        return role_error

    if not all(k in data for k in ['product_id', 'type', 'quantity']):
        return {'message': 'product_id, type, quantity required'}, 400

    product = Product.query.get_or_404(data['product_id'])

    q = data['quantity']
    if data['type'] == 'in':
        product.quantity += q
    elif data['type'] == 'out':
        if product.quantity < q:
            return {'message': 'Insufficient stock'}, 400
        product.quantity -= q
    else:
        return {'message': 'Type must be in or out'}, 400

    transaction = Transaction(
        product_id=data['product_id'],
        type=data['type'],
        quantity=q
    )
    db.session.add(transaction)
    db.session.commit()
    return {'message': 'Transaction recorded'}, 201

