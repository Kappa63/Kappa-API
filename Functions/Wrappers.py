from Controllers.DBController import getSession
from flask import request, jsonify
from functools import wraps
from Models import User

def Authorize(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        apiKey = request.headers.get("X-API-KEY")
        if not apiKey:
            return jsonify(error="Missing API key"), 401

        with getSession() as session:
            exists = session.query(User).filter_by(apiKey=apiKey).first()
            if not exists:
                return jsonify(error="Invalid API key"), 401

        return f(*args, **kwargs)
    return decorated