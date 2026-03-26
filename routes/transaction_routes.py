from flask import Blueprint, request, jsonify
from models.transaction_model import Transaction
from models.product_model import Product
from app.extensions import db
from flask_jwt_extended import jwt_required
from utils.auth import roles_required

transaction_bp = Blueprint("transactions", __name__)

@transaction_bp.route("/", methods=["POST"])
@jwt_required()
@roles_required("manager", "admin")
def stock_movement():
    data = request.get_json()

    product = Product.query.get_or_404(data.get("product_id"))

    if data.get("type") == "in":
        product.quantity += data.get("quantity", 0)
    else:
        product.quantity -= data.get("quantity", 0)

    transaction = Transaction(
        product_id=data.get("product_id"),
        type=data.get("type"),
        quantity=data.get("quantity", 0)
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction recorded"}), 201