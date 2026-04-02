from app.models.category_model import Category
from app.extensions import db

def check_role(role, allowed_roles):
    if role not in allowed_roles:
        return {'message': 'Access forbidden'}, 403
    return None

def create_category(role, data):
    role_error = check_role(role, ['manager', 'admin'])
    if role_error:
        return role_error

    if not data.get('name'):
        return {'message': 'Name required'}, 400

    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return {'message': 'Category created', 'id': category.id}, 201

def get_categories(role):
    role_error = check_role(role, ['user', 'manager', 'admin'])
    if role_error:
        return role_error

    categories = Category.query.all()
    return [
        {'id': c.id, 'name': c.name}
        for c in categories
    ], 200

