from flask import Blueprint, request, jsonify
from Controllers.AuthController import registerUser

authBP = Blueprint("auth", __name__)

@authBP.route("/register", methods=["POST"])
def regUser():
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
        default:
            description: Error from website
    """
    data = request.json or {}
    username = data.get("username")
    if not username:
        return jsonify({"error": "username required"}), 400
    data = request.json or {}
    password = data.get("password")
    if not password:
        return jsonify({"error": "usepasswordrname required"}), 400

    response, code = registerUser(username, password)
    return jsonify(response), code