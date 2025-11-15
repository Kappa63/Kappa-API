from Utils.Decorators import Authorize, Ratelimited
from Controllers.WebController import _getRoyaNews, _find1337xTorrents
from flask import Blueprint, request, jsonify
from Models import Permissions
from Utils.Helpers.RequestHelpers import handleKwargsEndpoint
from Utils.Enums import SortOrder

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
    data = request.args
    fields = [("q", str, True)]
    
    return handleKwargsEndpoint(data, fields, _getRoyaNews)

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
    data = request.args
    fields = [("q", str, True), ("tsort", SortOrder, False)]

    return handleKwargsEndpoint(data, fields, _find1337xTorrents)