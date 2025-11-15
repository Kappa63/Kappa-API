from Controllers.AdminController import _patchUser, _listUsers
from flask import Blueprint, jsonify, request
from Utils.Decorators import Authorize
from Models import Permissions

adminBP = Blueprint("admin", __name__)

@adminBP.route("/users", methods=["GET"])
@Authorize(Permissions.ADMIN)
def adminListUsers():
    response, code = _listUsers()
    return jsonify(response), code

@adminBP.route("/users/<int:uid>", methods=["PATCH"])
@Authorize(Permissions.ADMIN)
def adminPatchUser(uid: int):
    response, code = _patchUser(uid, request.json or {})
    return jsonify(response), code