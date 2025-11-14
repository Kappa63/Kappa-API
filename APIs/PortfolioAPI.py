from Controllers.PortfolioController import _uploadImage, _listPosts, _createPost
from flask import Blueprint, jsonify, request
from Functions.Decorators import Ratelimited

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
    if not (imageURL := data.get("imageURL")):
        return jsonify({"error": "imageUrl required"}), 400
    if not (title := data.get("title")):
        return jsonify({"error": "title required"}), 400
    if not (description := data.get("description")):
        return jsonify({"error": "description required"}), 400
    if not (category := data.get("category")):
        return jsonify({"error": "category required"}), 400
    
    response, code = _createPost(imageURL, title, description, category)
    return jsonify(response), code

@portfolioBP.route("/posts", methods=["GET"])
def listPosts():
    response, code = _listPosts()
    return jsonify(response), code