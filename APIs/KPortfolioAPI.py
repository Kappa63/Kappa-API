from Controllers.KPortfolioController import (_uploadImage, _listExperiences, _createExperience, _updateExperience, 
                                              _listSkills, _createSkill, _updateSkill, _listProjects, _createProject,
                                              _updateProject)
from Utils.Helpers.RequestHelpers import handleKwargsEndpoint
from flask import Blueprint, jsonify, request
from Utils.Decorators import Authorize
from Utils.Enums import Permissions
from Utils.Helpers.DBHelpers import softDeleteFromDB
from Models import Experience, Skill, Project
from datetime import date

kPortfolioBP = Blueprint("kportfolio", __name__)

@kPortfolioBP.route("/image", methods=["POST"])
@Authorize(Permissions.ADMIN)
def uploadImage():
    if not (img := request.files.get("image")):
        return jsonify({"error": "Missing required query parameter 'image'"}), 400
    
    response, code = _uploadImage(img)
    return jsonify(response), code

@kPortfolioBP.route("/content", methods=["GET"])
def getContent():
    experiences, _ = _listExperiences()
    skills, _ = _listSkills()
    projects, _ = _listProjects()
    return jsonify({"experiences": experiences, "skills": skills, "projects": projects}), 200

###
@kPortfolioBP.route("/experiences", methods=["POST"])
@Authorize(Permissions.ADMIN)
def createExperience(): 
    data = request.json or {}
    fields = [("role", str, True), ("company", str, True), ("startDate", date, True), ("endDate", date, False), ("highlights", str, True)]

    return handleKwargsEndpoint(data, fields, _createExperience)

@kPortfolioBP.route("/experiences/<int:pid>", methods=["PUT"])
@Authorize(Permissions.ADMIN)
def updateExperience(pid):
    data = request.json or {}
    fields = [("role", str, False), ("company", str, False), ("startDate", date, False), ("endDate", date, False), ("highlights", str, False)]
    
    return handleKwargsEndpoint(data, fields, lambda **upd: _updateExperience(pid, upd))

@kPortfolioBP.route("/experiences/<int:pid>", methods=["DELETE"])
@Authorize(Permissions.ADMIN)
def delExperience(pid):
    response, code = softDeleteFromDB(Experience, pid, "Experience not found")
    return jsonify(response), code

###
@kPortfolioBP.route("/skills", methods=["POST"])
@Authorize(Permissions.ADMIN)
def createSkill(): 
    data = request.json or {}
    fields = [("category", str, True), ("name", str, True), ("icon", str, True)]

    return handleKwargsEndpoint(data, fields, _createSkill)

@kPortfolioBP.route("/skills/<int:pid>", methods=["PUT"])
@Authorize(Permissions.ADMIN)
def updateSkill(pid):
    data = request.json or {}
    fields = [("category", str, False), ("name", str, False), ("icon", str, False)]
    
    return handleKwargsEndpoint(data, fields, lambda **upd: _updateSkill(pid, upd))

@kPortfolioBP.route("/skills/<int:pid>", methods=["DELETE"])
@Authorize(Permissions.ADMIN)
def delSkill(pid):
    response, code = softDeleteFromDB(Skill, pid, "Skill not found")
    return jsonify(response), code

###
@kPortfolioBP.route("/projects", methods=["POST"])
@Authorize(Permissions.ADMIN)
def createProject(): 
    data = request.json or {}
    fields = [("imageURL", str, True), ("title", str, True), ("description", str, True), ("link", str, False)]

    return handleKwargsEndpoint(data, fields, _createProject)

@kPortfolioBP.route("/projects/<int:pid>", methods=["PUT"])
@Authorize(Permissions.ADMIN)
def updateProject(pid):
    data = request.json or {}
    fields = [("imageURL", str, False), ("title", str, False), ("description", str, False), ("link", str, False)]
    
    return handleKwargsEndpoint(data, fields, lambda **upd: _updateProject(pid, upd))

@kPortfolioBP.route("/projects/<int:pid>", methods=["DELETE"])
@Authorize(Permissions.ADMIN)
def delProject(pid):
    response, code = softDeleteFromDB(Project, pid, "Project not found")
    return jsonify(response), code