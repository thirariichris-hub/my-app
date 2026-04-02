# Inventory API

## MVC Structure
- **Models**: models/*.py (SQLAlchemy db.Model)
- **Views**: JSON responses in routes
- **Controllers**: Blueprint routes/*.py

## Role-Based Access
- User: Read-only GET
- Manager/Admin: Create/Update (some DELETE for admin)



