# API Testing Guide

## Postman Collection
1. Import `postman_collection.json`
2. Set collection variable `base_url` = `http://127.0.0.1:5000`
3. Run requests in order - tokens auto-saved.

## VSCode REST Client (.http files in /requests/)
1. Install 'REST Client' extension.
2. Click 'Send Request' above ### headers in each .http file.
3. Paste your Bearer token from login.

## Start Server
```bash
source venv/bin/activate
python3 run.py
```

## Role Permissions
- **User**: GET products/categories/suppliers
- **Manager**: GET + POST/PUT products/transactions
- **Admin**: All + DELETE

Test JWT/role enforcement by swapping tokens!
