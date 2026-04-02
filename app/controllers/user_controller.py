from app.models.user_model import User
from app.extensions import db

def register(data):
    if not data:
        return {'message': 'No JSON data'}, 400

    existing_user = User.query.filter_by(email=data.get('email')).first()
    if existing_user:
        return {'message': 'Email already registered'}, 409

    if not all(k in data for k in ['first_name', 'last_name', 'email', 'password']):
        return {'message': 'Missing required fields'}, 400

    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        role=data.get('role', 'user')
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()
    return {'message': 'User created'}, 201

def login(data):
    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not user.check_password(data.get('password', '')):
        return {'message': 'Invalid credentials'}, 401

    return {'message': 'Logged in', 'role': user.role}, 200

