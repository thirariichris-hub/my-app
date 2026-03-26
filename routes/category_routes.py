from flask import Blueprint, request, jsonify
from models.category_model import Category
from app.extensions import db
from flask_jwt_extended import jwt_required
from utils.auth import roles_required

category_bp = Blueprint("categories", __name__)

@category_bp.route("/", methods=["POST"])
@jwt_required()
@roles_required("manager", "admin")
def create_category():
    data = request.get_json()

    category = Category(name=data.get("name"))
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category created"}), 201


@category_bp.route("/", methods=["GET"])
@jwt_required()
def get_categories():
    categories = Category.query.all()

    return jsonify([
        {"id": c.id, "name": c.name}
        for c in categories
    ]), 200