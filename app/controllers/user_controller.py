from app.models.user_model import User
from app.extensions import db
import re
from sqlalchemy.exc import IntegrityError

def register(data):
    if not data:
        return {'message': 'No JSON data'}, 400

    if not all(k in data for k in ['first_name', 'last_name', 'email', 'password']):
        return {'message': 'Missing required fields'}, 400

    email_regex = r'^[^@]+@[^@]+\.[^@]+$'
    if not re.match(email_regex, data['email']):
        return {'message': 'Invalid email format'}, 400

    try:
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()
        return {
            **user.to_dict(),
            'email_status': 'okay',
            'role_status': 'okay',
            'session': False
        }, 201
    except IntegrityError:
        db.session.rollback()
        return {'message': 'Email already registered. Please use a different email or delete existing user.'}, 409
    except Exception as e:
        db.session.rollback()
        return {'message': f'Database error: {str(e)}'}, 500

def check_role(role, allowed_roles):
    if not role or role not in allowed_roles:
        return {'message': 'Access forbidden'}, 403
    return None

def login(data):
    try:
        user = User.query.filter_by(email=data.get('email')).first()

        if not user or not user.check_password(data.get('password', '')):
            return {'email_status': False, 'session': False, 'message': 'Invalid credentials'}, 401

        return {
            **user.to_dict(),
            'email_status': 'okay',
            'role_status': 'okay' if user.role in ['user', 'manager', 'admin'] else False,
            'session': True
        }, 200
    except Exception as e:
        db.session.rollback()
        return {'message': f'Database query error: {str(e)}'}, 500

def get_users(role):
    role_error = check_role(role, ['user', 'manager', 'admin'])
    if role_error:
        return role_error

    try:
        users = User.query.all()
        return [user.to_dict() for user in users], 200
    except Exception as e:
        db.session.rollback()
        return {'message': f'Database query error: {str(e)}'}, 500

def get_user(id, role):
    role_error = check_role(role, ['user', 'manager', 'admin'])
    if role_error:
        return role_error

    try:
        user = User.query.get_or_404(id)
        return user.to_dict(), 200
    except Exception as e:
        db.session.rollback()
        return {'message': f'Database query error: {str(e)}'}, 500
