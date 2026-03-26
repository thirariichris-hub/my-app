from flask import Blueprint, request, jsonify
from models.user_model import User
from app.extensions import db
from flask_jwt_extended import create_access_token

user_bp = Blueprint("users", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON data"}), 400
    
    existing_user = User.query.filter_by(email=data.get("email")).first()
    if existing_user:
        return jsonify({"message": "Email already registered"}), 409

    user = User(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        role=data.get("role", "user")
    )
    user.set_password(data.get("password", ""))
    
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({"token": token}), 200