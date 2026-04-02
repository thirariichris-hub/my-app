from functools import wraps
from flask import session, jsonify

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not session.get("role") or session.get("role") not in roles:
                return jsonify({"message": "Access forbidden - login with role"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

