from Controllers.DoseGuardController import (_createCaregiver, _createPatient, _createPill, _createDose, 
                                            _createSchedule, _attachDoseToSchedule, _attachScheduleToPatient, 
                                            _attachPatientToCaregiver, _createDoseHistory)
from Models import Caregiver, Patient, Pill, Dose, Schedule, ScheduleDoses, CaregiverPatient, PatientSchedule, DoseHistory
from flask import Blueprint, request, jsonify
from Utils.Decorators import Ratelimited
from Utils.Helpers.RequestHelpers import handleEndpoint
from Utils.Helpers.DBHelpers import getFromDB

doseGuardBP = Blueprint("doseguard", __name__)

@doseGuardBP.route("/caregivers", methods=["POST"])
def createCaregiver():
    data = request.json or {}
    fields = [("name", str, True), ("username", str, True), ("passwordHash", str, True)]

    return handleEndpoint(data, fields, _createCaregiver)

@doseGuardBP.route("/patients", methods=["POST"])
def createPatient():
    data = request.json or {}
    fields = [("name", str, True), ("age", int, False), ("weight", float, False), ("height", float, False), ("contact", str, False)]

    return handleEndpoint(data, fields, _createPatient)

@doseGuardBP.route("/pills", methods=["POST"])
def createPill():
    data = request.json or {}
    fields = [("name", str, True), ("strength", float, True)]

    return handleEndpoint(data, fields, _createPill)

@doseGuardBP.route("/doses", methods=["POST"])
def createDose():
    data = request.json or {}
    fields = [("pillId", int, True), ("interval", int, True), ("amount", int, True)]

    return handleEndpoint(data, fields, _createDose)

@doseGuardBP.route("/schedules", methods=["POST"])
def createSchedule():
    data = request.json or {}
    fields = [("name", str, True)]

    return handleEndpoint(data, fields, _createSchedule)

@doseGuardBP.route("/schedules/doses", methods=["POST"])
def attachDoseToSchedule():
    data = request.json or {}
    fields = [("scheduleId", int, True), ("doseId", int, True)]

    return handleEndpoint(data, fields, _attachDoseToSchedule)

@doseGuardBP.route("/patients/schedules", methods=["POST"])
def attachScheduleToPatient():
    data = request.json or {}
    fields = [("patientId", int, True), ("scheduleId", int, True)]

    return handleEndpoint(data, fields, _attachScheduleToPatient)

@doseGuardBP.route("/caregivers/patients", methods=["POST"])
def attachPatientToCaregiver():
    data = request.json or {}
    fields = [("caregiverId", int, True), ("patientId", int, True)]

    return handleEndpoint(data, fields, _attachPatientToCaregiver)

@doseGuardBP.route("/dose-history", methods=["POST"])
def createDoseHistory():
    data = request.json or {}
    fields = [("patientId", int, True), ("doseId", int, True), ("taken", bool, True)]

    return handleEndpoint(data, fields, _createDoseHistory)

@doseGuardBP.route("/caregivers/<int:caregiverId>", methods=["GET"])
def getCaregiver(caregiverId):
    response, code = getFromDB(Caregiver, caregiverId, "Caregiver not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>", methods=["GET"])
def getPatient(patientId):
    response, code = getFromDB(Patient, patientId, "Patient not found")
    return jsonify(response), code

@doseGuardBP.route("/pills/<int:pillId>", methods=["GET"])
def getPill(pillId):
    response, code = getFromDB(Pill, pillId, "Pill not found")
    return jsonify(response), code

@doseGuardBP.route("/doses/<int:doseId>", methods=["GET"])
def getDose(doseId):
    response, code = getFromDB(Dose, doseId, "Dose not found")
    return jsonify(response), code

@doseGuardBP.route("/schedules/<int:scheduleId>", methods=["GET"])
def getSchedule(scheduleId):
    response, code = getFromDB(Schedule, scheduleId, "Schedule not found")
    return jsonify(response), code

@doseGuardBP.route("/dose-history/<int:entryId>", methods=["GET"])
def getDoseHistory(entryId):
    response, code = getFromDB(DoseHistory, entryId, "Dose history not found")
    return jsonify(response), code