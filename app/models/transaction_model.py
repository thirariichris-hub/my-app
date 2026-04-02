from app.extensions import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    type = db.Column(db.String(10))  
    quantity = db.Column(db.Integer)