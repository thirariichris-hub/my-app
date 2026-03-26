from app import create_app
from app.extensions import db


import models.user_model
import models.product_model
import models.category_model
import models.supplier_model
import models.transaction_model

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
