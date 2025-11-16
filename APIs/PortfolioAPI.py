from Controllers.PortfolioController import _uploadImage, _listPosts, _createPost
from Utils.Helpers.RequestHelpers import handleKwargsEndpoint
from flask import Blueprint, jsonify, request
from Utils.Decorators import Ratelimited
from Utils.Types import FileStorage

portfolioBP = Blueprint("portfolio", __name__)

@portfolioBP.route("/image", methods=["POST"])
def uploadImage():
    if not (img := request.files.get("image")):
        return jsonify({"error": "Missing required query parameter 'image'"}), 400
    
    response, code = _uploadImage(img)
    return jsonify(response), code

@portfolioBP.route("/posts", methods=["POST"])
def createPost(): 
    data = request.json or {}
    fields = [("imageURL", str, True), ("title", str, True), ("description", str, True), ("category", str, True)]

    return handleKwargsEndpoint(data, fields, _createPost)

@portfolioBP.route("/posts", methods=["GET"])
def listPosts():
    response, code = _listPosts()
    return jsonify(response), code