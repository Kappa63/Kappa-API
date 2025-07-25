from Functions.Decorators import Authorize, Ratelimited
from Controllers.NewsController import _getRoyaNews
from flask import Blueprint, request, jsonify
from Models import Permissions

newsBP = Blueprint("news", __name__)

@newsBP.route("", methods=["GET"])
@Authorize(Permissions.GENERAL)
@Ratelimited
def getRoyaNews():
    """
    News from "https://en.royanews.tv"
    ---
    tags:
      - News
    parameters:
      - name: q
        in: query
        type: string
        required: false
        description: Optional search keyword.
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