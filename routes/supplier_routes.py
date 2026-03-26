from flask import Blueprint, request, jsonify
from models.supplier_model import Supplier
from app.extensions import db
from flask_jwt_extended import jwt_required
from utils.auth import roles_required

supplier_bp = Blueprint("suppliers", __name__)


@supplier_bp.route("/", methods=["POST"])
@jwt_required()
@roles_required("manager", "admin")
def create_supplier():
    data = request.get_json()

    supplier = Supplier(name=data.get("name"))
    db.session.add(supplier)
    db.session.commit()

    return jsonify({"message": "Supplier created"}), 201



@supplier_bp.route("/", methods=["GET"])
@jwt_required()
def get_suppliers():
    suppliers = Supplier.query.all()

    return jsonify([
        {"id": s.id, "name": s.name}
        for s in suppliers
    ]), 200