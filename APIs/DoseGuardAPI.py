from Controllers.DoseGuardController import (_createCaregiver, _createPatient, _createPill, _createDose, 
                                            _createSchedule, _attachDoseToSchedule, _attachScheduleToPatient, 
                                            _attachPatientToCaregiver, _createDoseHistory, _deleteDoseFromSchedule,
                                            _deleteScheduleFromPatient, _deletePatientFromCaregiver, _updateCaregiver,
                                            _updateDoseHistory, _updateSchedule, _updateDose, _updatePill, _updatePatient)
from Models import Caregiver, Patient, Pill, Dose, Schedule, DoseHistory
from flask import Blueprint, request, jsonify
from Utils.Decorators import Ratelimited
from Utils.Helpers.RequestHelpers import handleKwargsEndpoint, handleDictEndpoint
from Utils.Helpers.DBHelpers import getFromDB, softDeleteFromDB, listFromDB, listRelatedFromDB, listNestedRelatedFromDB

doseGuardBP = Blueprint("doseguard", __name__)

### POST ###
@doseGuardBP.route("/caregivers", methods=["POST"])
def createCaregiver():
    data = request.json or {}
    fields = [("name", str, True), ("username", str, True), ("passwordHash", str, True)]

    return handleKwargsEndpoint(data, fields, _createCaregiver)

@doseGuardBP.route("/patients", methods=["POST"])
def createPatient():
    data = request.json or {}
    fields = [("name", str, True), ("age", int, False), ("weight", float, False), ("height", float, False), ("contact", str, False)]

    return handleKwargsEndpoint(data, fields, _createPatient)

@doseGuardBP.route("/pills", methods=["POST"])
def createPill():
    data = request.json or {}
    fields = [("name", str, True), ("strength", float, True)]

    return handleKwargsEndpoint(data, fields, _createPill)

@doseGuardBP.route("/doses", methods=["POST"])
def createDose():
    data = request.json or {}
    fields = [("pillId", int, True), ("interval", int, True), ("amount", int, True)]

    return handleKwargsEndpoint(data, fields, _createDose)

@doseGuardBP.route("/schedules", methods=["POST"])
def createSchedule():
    data = request.json or {}
    fields = [("name", str, True)]

    return handleKwargsEndpoint(data, fields, _createSchedule)

@doseGuardBP.route("/schedules/doses", methods=["POST"])
def attachDoseToSchedule():
    data = request.json or {}
    fields = [("scheduleId", int, True), ("doseId", int, True)]

    return handleKwargsEndpoint(data, fields, _attachDoseToSchedule)

@doseGuardBP.route("/patients/schedules", methods=["POST"])
def attachScheduleToPatient():
    data = request.json or {}
    fields = [("patientId", int, True), ("scheduleId", int, True)]

    return handleKwargsEndpoint(data, fields, _attachScheduleToPatient)

@doseGuardBP.route("/caregivers/patients", methods=["POST"])
def attachPatientToCaregiver():
    data = request.json or {}
    fields = [("caregiverId", int, True), ("patientId", int, True)]

    return handleKwargsEndpoint(data, fields, _attachPatientToCaregiver)

@doseGuardBP.route("/dose-history", methods=["POST"])
def createDoseHistory():
    data = request.json or {}
    fields = [("patientId", int, True), ("doseId", int, True), ("taken", bool, True)]

    return handleKwargsEndpoint(data, fields, _createDoseHistory)

### GET ###
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

### DELETE ###
@doseGuardBP.route("/caregivers/<int:caregiverId>", methods=["DELETE"])
def deleteCaregiver(caregiverId):
    response, code = softDeleteFromDB(Caregiver, caregiverId, "Caregiver not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>", methods=["DELETE"])
def deletePatient(patientId):
    response, code = softDeleteFromDB(Patient, patientId, "Patient not found")
    return jsonify(response), code

@doseGuardBP.route("/pills/<int:pillId>", methods=["DELETE"])
def deletePill(pillId):
    response, code = softDeleteFromDB(Pill, pillId, "Pill not found")
    return jsonify(response), code

@doseGuardBP.route("/doses/<int:doseId>", methods=["DELETE"])
def deleteDose(doseId):
    response, code = softDeleteFromDB(Dose, doseId, "Dose not found")
    return jsonify(response), code

@doseGuardBP.route("/schedules/<int:scheduleId>", methods=["DELETE"])
def deleteSchedule(scheduleId):
    response, code = softDeleteFromDB(Schedule, scheduleId, "Schedule not found")
    return jsonify(response), code

@doseGuardBP.route("/dose-history/<int:entryId>", methods=["DELETE"])
def deleteDoseHistory(entryId):
    response, code = softDeleteFromDB(DoseHistory, entryId, "Dose history not found")
    return jsonify(response), code

@doseGuardBP.route("/schedules/doses", methods=["DELETE"])
def deleteDoseFromSchedule():
    data = request.args
    fields = [("scheduleId", int, True), ("doseId", int, True)]

    return handleDictEndpoint(data, fields, _deleteDoseFromSchedule)

@doseGuardBP.route("/patients/schedules", methods=["DELETE"])
def deleteScheduleFromPatient():
    data = request.args
    fields = [("patientId", int, True), ("scheduleId", int, True)]

    return handleDictEndpoint(data, fields, _deleteScheduleFromPatient)

@doseGuardBP.route("/caregivers/patients", methods=["DELETE"])
def deletePatientFromCaregiver():
    data = request.args
    fields = [("caregiverId", int, True), ("patientId", int, True)]

    return handleDictEndpoint(data, fields, _deletePatientFromCaregiver)

### GET FOR ###
@doseGuardBP.route("/caregivers/<int:caregiverId>/patients", methods=["GET"])
def listPatientsForCaregiver(caregiverId):
    response, code = listRelatedFromDB(Caregiver, caregiverId, "patients", "Caregiver not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>/caregivers", methods=["GET"])
def listCaregiversForPatient(patientId):
    response, code = listRelatedFromDB(Patient, patientId, "caregivers", "Patient not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>/schedules", methods=["GET"])
def listSchedulesForPatient(patientId):
    response, code = listRelatedFromDB(Patient, patientId, "schedules", "Patient not found")
    return jsonify(response), code

@doseGuardBP.route("/schedules/<int:scheduleId>/doses", methods=["GET"])
def listDosesForSchedule(scheduleId):
    response, code = listRelatedFromDB(Schedule, scheduleId, "doses", "Schedule not found")
    return jsonify(response), code

@doseGuardBP.route("/pills/<int:pillId>/dose-history", methods=["GET"])
def getPillDoseHistory(pillId):
    response, code = listNestedRelatedFromDB(Pill, pillId, ["doses", "history"], "Pill not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>/all-doses", methods=["GET"])
def getPatientSchedulesDoses(patientId):
    response, code = listNestedRelatedFromDB(Patient, patientId, ["schedules", "doses"], "Patient not found")
    return jsonify(response), code

### GET ALL ###
@doseGuardBP.route("/caregivers", methods=["GET"])
def listCaregivers():
    response, code = listFromDB(Caregiver)
    return jsonify(response), code

@doseGuardBP.route("/patients", methods=["GET"])
def listPatients():
    response, code = listFromDB(Patient)
    return jsonify(response), code

@doseGuardBP.route("/pills", methods=["GET"])
def listPills():
    response, code = listFromDB(Pill)
    return jsonify(response), code

@doseGuardBP.route("/doses", methods=["GET"])
def listDoses():
    response, code = listFromDB(Dose)
    return jsonify(response), code

@doseGuardBP.route("/schedules", methods=["GET"])
def listSchedules():
    response, code = listFromDB(Schedule)
    return jsonify(response), code

@doseGuardBP.route("/dose-history", methods=["GET"])
def listDoseHistory():
    response, code = listFromDB(DoseHistory)
    return jsonify(response), code

### PATCH ###
@doseGuardBP.route("/caregivers/<int:caregiverId>", methods=["PATCH"])
def updateCaregiver(caregiverId):
    data = request.json or {}
    fields = [("name", str, False), ("username", str, False), ("passwordHash", str, False)]

    return handleKwargsEndpoint(
        data, fields,
        lambda **upd: _updateCaregiver(caregiverId, upd)
    )

@doseGuardBP.route("/patients/<int:patientId>", methods=["PATCH"])
def updatePatient(patientId):
    data = request.json or {}
    fields = [("name", str, False), ("contact", str, False), ("age", int, False), ("weight", float, False), ("height", float, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updatePatient(patientId, upd))

@doseGuardBP.route("/pills/<int:pillId>", methods=["PATCH"])
def updatePill(pillId):
    data = request.json or {}
    fields = [("name", str, False), ("strength", float, False)]

    return handleKwargsEndpoint(
        data, fields,
        lambda **upd: _updatePill(pillId, upd)
    )

@doseGuardBP.route("/doses/<int:doseId>", methods=["PATCH"])
def updateDose(doseId):
    data = request.json or {}
    fields = [("pillId", int, False), ("interval", int, False), ("amount", int, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updateDose(doseId, upd))

@doseGuardBP.route("/schedules/<int:scheduleId>", methods=["PATCH"])
def updateSchedule(scheduleId):
    data = request.json or {}
    fields = [("name", str, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updateSchedule(scheduleId, upd))

@doseGuardBP.route("/dose-history/<int:entryId>", methods=["PATCH"])
def updateDoseHistory(entryId):
    data = request.json or {}
    fields = [("taken", bool, False), ("doseId", int, False), ("patientId", int, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updateDoseHistory(entryId, upd))