from Controllers.AuthController import _registerUser, _loginUser
from flask import Blueprint, request, jsonify
from Utils.Decorators import Ratelimited
from Utils.Helpers.RequestHelpers import handleKwargsEndpoint

authBP = Blueprint("auth", __name__)

@authBP.route("/register", methods=["POST"])
@Ratelimited
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
    fields = [("username", str, True), ("password", str, True)]
    return handleKwargsEndpoint(data, fields, _registerUser)

@authBP.route("/login", methods=["POST"])
@Ratelimited
def loginUser():
    """
    Login user and get your user data
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
    fields = [("username", str, True), ("password", str, True)]
    
    return handleKwargsEndpoint(data, fields, _loginUser)