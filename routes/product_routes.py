from flask import Blueprint, request, jsonify
from models.product_model import Product
from app.extensions import db
from flask_jwt_extended import jwt_required
from utils.auth import roles_required

product_bp = Blueprint("products", __name__)

# CREATE
@product_bp.route("/", methods=["POST"])
@jwt_required()
@roles_required("manager", "admin")
def create_product():
    data = request.get_json()

    product = Product(
        name=data.get("name"),
        quantity=data.get("quantity")
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product created"}), 201



@product_bp.route("/", methods=["GET"])
@jwt_required()
def get_products():
    products = Product.query.all()

    return jsonify([
        {"id": p.id, "name": p.name, "quantity": p.quantity}
        for p in products
    ]), 200



@product_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@roles_required("manager", "admin")
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    product.name = data.get("name", product.name)
    product.quantity = data.get("quantity", product.quantity)
    product.category_id = data.get("category_id")
    product.supplier_id = data.get("supplier_id")

    db.session.commit()

    return jsonify({"message": "Updated"}), 200



@product_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@roles_required("admin")
def delete_product(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Deleted"}), 200