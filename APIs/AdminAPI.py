from Controllers.AdminController import _patchUser, _listUsers
from Functions.Decorators import Authorize, Ratelimiter
from flask import Blueprint, jsonify, request
from Models import Permissions

adminBP = Blueprint("admin", __name__)

@adminBP.route("/admin/users", methods=["GET"])
@Authorize(Permissions.ADMIN)
def listUsers():
    response, code = _listUsers()
    return jsonify(response), code

@adminBP.route("/admin/users/<int:uid>", methods=["PATCH"])
@Authorize(Permissions.ADMIN)
def patchUser(uid: int):
    response, code = _patchUser(uid, request.json or {})
    return jsonify(response), code