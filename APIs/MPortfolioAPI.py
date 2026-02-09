from Controllers.MPortfolioController import (_uploadImage, _listPosts, _createPost, _updatePost, 
                                            _deletePost, _reorderPosts, _getGeneral, _updateGeneral)
from Utils.Helpers.RequestHelpers import handleKwargsEndpoint
from flask import Blueprint, jsonify, request
from Utils.Decorators import Ratelimited
from Utils.Types import FileStorage

mPortfolioBP = Blueprint("mportfolio", __name__)

@mPortfolioBP.route("/image", methods=["POST"])
def uploadImage():
    if not (img := request.files.get("image")):
        return jsonify({"error": "Missing required query parameter 'image'"}), 400
    
    response, code = _uploadImage(img)
    return jsonify(response), code

@mPortfolioBP.route("/posts", methods=["POST"])
def createPost(): 
    data = request.json or {}
    fields = [("imageURL", str, True), ("title", str, True), ("description", str, True), ("category", str, True)]

    return handleKwargsEndpoint(data, fields, _createPost)

@mPortfolioBP.route("/content", methods=["GET"])
def getContent():
    posts, _ = _listPosts()
    general, _ = _getGeneral()
    return jsonify({"posts": posts, "general": general}), 200

@mPortfolioBP.route("/general", methods=["POST"])
def updateGeneral():
    data = request.json or {}
    response, code = _updateGeneral(data)
    return jsonify(response), code

@mPortfolioBP.route("/posts/reorder", methods=["POST"])
def reorderPosts():
    data = request.json or {}
    # Expecting {"order_map": {id: order}}
    if not (order_map := data.get("order_map")):
         return jsonify({"error": "Missing 'order_map'"}), 400
    response, code = _reorderPosts(order_map)
    return jsonify(response), code

@mPortfolioBP.route("/posts/<int:pid>", methods=["PUT"])
def updatePost(pid):
    data = request.json or {}
    # Fields: iURL, ttl, desc, cat, ordr
    response, code = _updatePost(pid, 
                                 iURL=data.get("imageURL"), 
                                 ttl=data.get("title"), 
                                 desc=data.get("description"), 
                                 cat=data.get("category"), 
                                 ordr=data.get("order"))
    return jsonify(response), code

@mPortfolioBP.route("/posts/<int:pid>", methods=["DELETE"])
def deletePost(pid):
    response, code = _deletePost(pid)
    return jsonify(response), code
