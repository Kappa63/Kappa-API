from Controllers.DBController import getSession
from datetime import datetime, timezone
from Models import User, Permissions
from flask import request, jsonify
from functools import wraps

def Authorize(authPerms=Permissions.GENERAL):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not (apiKey := request.headers.get("X-API-KEY")):
                return jsonify(error="Missing API key"), 401

            with getSession() as session:
                if not (user := session.query(User).filter_by(apiKey=apiKey).first()):
                    return jsonify(error="Invalid API key"), 401
                
                user.lastUse = datetime.now(timezone.utc) # type: ignore
                
                if not (Permissions(user.perms) & authPerms):
                    return jsonify(error="Insufficient permissions"), 403

            return f(*args, **kwargs)
        return decorated
    return decorator