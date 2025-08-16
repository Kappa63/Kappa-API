from Functions.Decorators import Authorize, Ratelimited
from Controllers.WebController import _getRoyaNews, _find1337xTorrents
from flask import Blueprint, request, jsonify
from Models import Permissions

webBP = Blueprint("web", __name__)

@webBP.route("/news", methods=["GET"])
@Authorize(Permissions.GENERAL)
@Ratelimited
def getRoyaNews():
    """
    News from "https://en.royanews.tv"
    ---
    tags:
      - Web
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Requried search keyword.
      - name: X-API-Key
        in: header
        type: string
        required: true
        description: Your API Key for authorization.
    responses:
        200:
            description: Successful response
        204:
            description: Empty response
        400:
            description: Missing required parameter
        default:
            description: Error from website
    """
    if not (query := request.args.get("q")):
        return jsonify({"error": "Missing required query parameter 'q'"}), 400

    response, code = _getRoyaNews(query)
    return jsonify(response), code

@webBP.route("/torrent", methods=["GET"])
@Authorize(Permissions.GENERAL)
@Ratelimited
def find1337xTorrents():
    """
    Torrents from "https://1337x.to"
    ---
    tags:
      - Web
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Required search keyword.
      - name: tsort
        in: query
        type: string
        required: false
        description: Can be 'asc' or 'desc'. Can also be left empty for default sorting.
      - name: X-API-Key
        in: header
        type: string
        required: true
        description: Your API Key for authorization.
    responses:
        200:
            description: Successful response
        204:
            description: Empty response
        400:
            description: Missing required parameter
        default:
            description: Error from website
    """
    if not (query := request.args.get("q")):
        return jsonify({"error": "Missing required query parameter 'q'"}), 400
    
    sorting = request.args.get("tsort")
    if sorting:
        sorting = sorting.lower()

    response, code = _find1337xTorrents(query, sorting if sorting in ("asc", "desc") else None)
    return jsonify(response), code