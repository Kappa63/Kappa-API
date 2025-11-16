from Controllers.UsersController import _getUser, _deleteUser
from Utils.Decorators import Ratelimited, Authorize
from flask import Blueprint, jsonify, g
from Utils.Enums import Permissions

userBP = Blueprint("user", __name__)

@userBP.route("", methods=["GET"])
@Authorize(Permissions.GENERAL|Permissions.PRIVATE|Permissions.ADMIN)
@Ratelimited
def getUser():
    """
    Get your user data
    ---
    tags:
      - User
    parameters:
      - name: X-API-Key
        in: header
        type: string
        required: true
        description: Your API Key for authorization.
    responses:
        200:
            description: Successful request
    """
    response, code = _getUser(g.user)
    return jsonify(response), code

@userBP.route("", methods=["DELETE"])
@Authorize(Permissions.GENERAL|Permissions.PRIVATE|Permissions.ADMIN)
@Ratelimited
def deleteUser():
    """
    Delete your user data
    ---
    tags:
      - User
    parameters:
      - name: X-API-Key
        in: header
        type: string
        required: true
        description: Your API Key for authorization.
    responses:
        200:
            description: Successful request
    """
    return jsonify({}), _deleteUser(g.user)