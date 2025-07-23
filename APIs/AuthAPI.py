from Controllers.AuthController import _registerUser, _loginUser
from flask import Blueprint, request, jsonify
from Functions.Decorators import Ratelimiter

authBP = Blueprint("auth", __name__)

@authBP.route("/register", methods=["POST"])
def registerUser():
    """
    Register user and get your API-Key
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                username:
                    type: string
                    description: The username
                password:
                    type: string
                    description: The password
            required:
              - username
              - password
    responses:
        201:
            description: Successfully registered
        400:
            description: Missing required parameter
        409:
            description: Already exists
    """
    data = request.json or {}
    if not (username := data.get("username")):
        return jsonify({"error": "username required"}), 400
    if not (password := data.get("password")):
        return jsonify({"error": "password required"}), 400

    response, code = _registerUser(username, password)
    return jsonify(response), code

@authBP.route("/login", methods=["POST"])
def loginUser():
    """
    Login user and get your User Data
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
                username:
                    type: string
                    description: The username
                password:
                    type: string
                    description: The password
            required:
              - username
              - password
    responses:
        200:
            description: Successful request
        400:
            description: Missing required parameter
        401:
            description: Invalid credentials
        404:
            description: User does not exist
    """
    data = request.json or {}
    if not (username := data.get("username")):
        return jsonify({"error": "username required"}), 400
    if not (password := data.get("password")):
        return jsonify({"error": "password required"}), 400

    response, code = _loginUser(username, password)
    return jsonify(response), code