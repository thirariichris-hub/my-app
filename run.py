from app import create_app
from app.extensions import db


import app.models.user_model
import app.models.product_model
import app.models.category_model
import app.models.supplier_model
import app.models.transaction_model

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
