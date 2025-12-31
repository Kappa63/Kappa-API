from Controllers.DoseGuardController import (_registerCaregiver, _loginCaregiver, _createPatient, _createPill, _createDose, 
                                            _createSchedule, _attachDoseToSchedule, _attachScheduleToPatient, 
                                            _attachPatientToCaregiver, _createDoseHistory, _deleteDoseFromSchedule,
                                            _deleteScheduleFromPatient, _deletePatientFromCaregiver, _updateCaregiver,
                                            _updateDoseHistory, _updateSchedule, _updateDose, _updatePill, _updatePatient)
from Utils.Helpers.DBHelpers import getFromDB, softDeleteFromDB, listFromDB, listRelatedFromDB, listNestedRelatedFromDB
from Utils.Helpers.RequestHelpers import handleKwargsEndpoint, handleDictEndpoint
from Utils.Helpers.AuthHelpers import (verifyCaregiverOwnership, verifyCaregiverPatientRelationship, 
                                       verifyScheduleAccess, verifyPillAccess, verifyDoseAccess, 
                                       verifyDoseHistoryAccess, getCaregiverIdFromRequest)
from Models import Caregiver, Patient, Pill, Dose, Schedule, DoseHistory
from flask import Blueprint, request, jsonify
from Utils.Decorators import Ratelimited, Authorize
from Utils.Enums import Permissions

doseGuardBP = Blueprint("doseguard", __name__)

### POST ###
@doseGuardBP.route("/caregivers/register", methods=["POST"])
@Ratelimited
def registerCaregiver():
    data = request.json or {}
    fields = [("name", str, True), ("username", str, True), ("password", str, True)]

    return handleKwargsEndpoint(data, fields, _registerCaregiver)

@doseGuardBP.route("/caregivers/login", methods=["POST"])
@Ratelimited
def loginCaregiver():
    data = request.json or {}
    fields = [("username", str, True), ("password", str, True)]

    return handleKwargsEndpoint(data, fields, _loginCaregiver)

@doseGuardBP.route("/patients", methods=["POST"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def createPatient():
    data = request.json or {}
    fields = [("name", str, True), ("dob", str, False), ("weight", float, False), ("height", float, False), ("contact", str, False)]

    return handleKwargsEndpoint(data, fields, _createPatient)

@doseGuardBP.route("/pills", methods=["POST"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def createPill():
    data = request.json or {}
    fields = [("name", str, True), ("strength", float, True)]

    return handleKwargsEndpoint(data, fields, _createPill)

@doseGuardBP.route("/doses", methods=["POST"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def createDose():
    data = request.json or {}
    fields = [("pillId", int, True), ("interval", int, True), ("amount", int, True)]

    return handleKwargsEndpoint(data, fields, _createDose)

@doseGuardBP.route("/schedules", methods=["POST"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def createSchedule():
    data = request.json or {}
    fields = [("name", str, True)]

    return handleKwargsEndpoint(data, fields, _createSchedule)

@doseGuardBP.route("/schedules/doses", methods=["POST"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def attachDoseToSchedule():
    data = request.json or {}
    fields = [("scheduleId", int, True), ("doseId", int, True)]
    
    # Verify access to the schedule
    if not verifyScheduleAccess(data.get("scheduleId")):
        return jsonify(error="Forbidden: You can only modify schedules for patients under your care"), 403

    return handleKwargsEndpoint(data, fields, _attachDoseToSchedule)

@doseGuardBP.route("/patients/schedules", methods=["POST"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def attachScheduleToPatient():
    data = request.json or {}
    fields = [("patientId", int, True), ("scheduleId", int, True)]
    
    # Verify access to the patient
    if not verifyCaregiverPatientRelationship(data.get("patientId")):
        return jsonify(error="Forbidden: You can only modify schedules for patients under your care"), 403

    return handleKwargsEndpoint(data, fields, _attachScheduleToPatient)

@doseGuardBP.route("/caregivers/patients", methods=["POST"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def attachPatientToCaregiver():
    data = request.json or {}
    fields = [("caregiverId", int, True), ("patientId", int, True)]
    
    # Verify the caregiver owns the caregiverId being modified
    if not verifyCaregiverOwnership(data.get("caregiverId")):
        return jsonify(error="Forbidden: You can only attach patients to your own caregiver profile"), 403

    return handleKwargsEndpoint(data, fields, _attachPatientToCaregiver)

@doseGuardBP.route("/dose-history", methods=["POST"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def createDoseHistory():
    data = request.json or {}
    fields = [("patientId", int, True), ("doseId", int, True), ("taken", bool, True)]
    
    # Verify the patient is under the caregiver's care
    if not verifyCaregiverPatientRelationship(data.get("patientId")):
        return jsonify(error="Forbidden: You can only create dose history for patients under your care"), 403

    return handleKwargsEndpoint(data, fields, _createDoseHistory)

### GET ###
@doseGuardBP.route("/caregivers/<int:caregiverId>", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def getCaregiver(caregiverId):
    if not verifyCaregiverOwnership(caregiverId):
        return jsonify(error="Forbidden: You can only access your own caregiver profile"), 403
    
    response, code = getFromDB(Caregiver, caregiverId, "Caregiver not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def getPatient(patientId):
    if not verifyCaregiverPatientRelationship(patientId):
        return jsonify(error="Forbidden: You can only access patients under your care"), 403
    
    response, code = getFromDB(Patient, patientId, "Patient not found")
    return jsonify(response), code

@doseGuardBP.route("/pills/<int:pillId>", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def getPill(pillId):
    if not verifyPillAccess(pillId):
        return jsonify(error="Forbidden: You can only access pills prescribed to your patients"), 403
    
    response, code = getFromDB(Pill, pillId, "Pill not found")
    return jsonify(response), code

@doseGuardBP.route("/doses/<int:doseId>", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def getDose(doseId):
    if not verifyDoseAccess(doseId):
        return jsonify(error="Forbidden: You can only access doses for patients under your care"), 403
    
    response, code = getFromDB(Dose, doseId, "Dose not found")
    return jsonify(response), code

@doseGuardBP.route("/schedules/<int:scheduleId>", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def getSchedule(scheduleId):
    if not verifyScheduleAccess(scheduleId):
        return jsonify(error="Forbidden: You can only access schedules for patients under your care"), 403
    
    response, code = getFromDB(Schedule, scheduleId, "Schedule not found")
    return jsonify(response), code

@doseGuardBP.route("/dose-history/<int:entryId>", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def getDoseHistory(entryId):
    if not verifyDoseHistoryAccess(entryId):
        return jsonify(error="Forbidden: You can only access dose history for patients under your care"), 403
    
    response, code = getFromDB(DoseHistory, entryId, "Dose history not found")
    return jsonify(response), code

### DELETE ###
@doseGuardBP.route("/caregivers/<int:caregiverId>", methods=["DELETE"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def deleteCaregiver(caregiverId):
    if not verifyCaregiverOwnership(caregiverId):
        return jsonify(error="Forbidden: You can only delete your own caregiver profile"), 403
    
    response, code = softDeleteFromDB(Caregiver, caregiverId, "Caregiver not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>", methods=["DELETE"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def deletePatient(patientId):
    if not verifyCaregiverPatientRelationship(patientId):
        return jsonify(error="Forbidden: You can only delete patients under your care"), 403
    
    response, code = softDeleteFromDB(Patient, patientId, "Patient not found")
    return jsonify(response), code

@doseGuardBP.route("/pills/<int:pillId>", methods=["DELETE"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def deletePill(pillId):
    if not verifyPillAccess(pillId):
        return jsonify(error="Forbidden: You can only delete pills prescribed to your patients"), 403
    
    response, code = softDeleteFromDB(Pill, pillId, "Pill not found")
    return jsonify(response), code

@doseGuardBP.route("/doses/<int:doseId>", methods=["DELETE"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def deleteDose(doseId):
    if not verifyDoseAccess(doseId):
        return jsonify(error="Forbidden: You can only delete doses for patients under your care"), 403
    
    response, code = softDeleteFromDB(Dose, doseId, "Dose not found")
    return jsonify(response), code

@doseGuardBP.route("/schedules/<int:scheduleId>", methods=["DELETE"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def deleteSchedule(scheduleId):
    if not verifyScheduleAccess(scheduleId):
        return jsonify(error="Forbidden: You can only delete schedules for patients under your care"), 403
    
    response, code = softDeleteFromDB(Schedule, scheduleId, "Schedule not found")
    return jsonify(response), code

@doseGuardBP.route("/dose-history/<int:entryId>", methods=["DELETE"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def deleteDoseHistory(entryId):
    if not verifyDoseHistoryAccess(entryId):
        return jsonify(error="Forbidden: You can only delete dose history for patients under your care"), 403
    
    response, code = softDeleteFromDB(DoseHistory, entryId, "Dose history not found")
    return jsonify(response), code

@doseGuardBP.route("/schedules/doses", methods=["DELETE"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def deleteDoseFromSchedule():
    data = request.args
    fields = [("scheduleId", int, True), ("doseId", int, True)]
    
    # Verify access to the schedule
    if not verifyScheduleAccess(int(data.get("scheduleId"))):
        return jsonify(error="Forbidden: You can only modify schedules for patients under your care"), 403

    return handleDictEndpoint(data, fields, _deleteDoseFromSchedule)

@doseGuardBP.route("/patients/schedules", methods=["DELETE"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def deleteScheduleFromPatient():
    data = request.args
    fields = [("patientId", int, True), ("scheduleId", int, True)]
    
    # Verify access to the patient
    if not verifyCaregiverPatientRelationship(int(data.get("patientId"))):
        return jsonify(error="Forbidden: You can only modify schedules for patients under your care"), 403

    return handleDictEndpoint(data, fields, _deleteScheduleFromPatient)

@doseGuardBP.route("/caregivers/patients", methods=["DELETE"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def deletePatientFromCaregiver():
    data = request.args
    fields = [("caregiverId", int, True), ("patientId", int, True)]
    
    # Verify the caregiver owns the caregiverId being modified
    if not verifyCaregiverOwnership(int(data.get("caregiverId"))):
        return jsonify(error="Forbidden: You can only detach patients from your own caregiver profile"), 403

    return handleDictEndpoint(data, fields, _deletePatientFromCaregiver)

### GET FOR ###
@doseGuardBP.route("/caregivers/<int:caregiverId>/patients", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listPatientsForCaregiver(caregiverId):
    if not verifyCaregiverOwnership(caregiverId):
        return jsonify(error="Forbidden: You can only access your own patients"), 403
    
    response, code = listRelatedFromDB(Caregiver, caregiverId, "patients", "Caregiver not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>/caregivers", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listCaregiversForPatient(patientId):
    if not verifyCaregiverPatientRelationship(patientId):
        return jsonify(error="Forbidden: You can only access patients under your care"), 403
    
    response, code = listRelatedFromDB(Patient, patientId, "caregivers", "Patient not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>/schedules", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listSchedulesForPatient(patientId):
    if not verifyCaregiverPatientRelationship(patientId):
        return jsonify(error="Forbidden: You can only access patients under your care"), 403
    
    response, code = listRelatedFromDB(Patient, patientId, "schedules", "Patient not found")
    return jsonify(response), code

@doseGuardBP.route("/schedules/<int:scheduleId>/doses", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listDosesForSchedule(scheduleId):
    if not verifyScheduleAccess(scheduleId):
        return jsonify(error="Forbidden: You can only access schedules for patients under your care"), 403
    
    response, code = listRelatedFromDB(Schedule, scheduleId, "doses", "Schedule not found")
    return jsonify(response), code

@doseGuardBP.route("/pills/<int:pillId>/dose-history", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def getPillDoseHistory(pillId):
    if not verifyPillAccess(pillId):
        return jsonify(error="Forbidden: You can only access pills prescribed to your patients"), 403
    
    response, code = listNestedRelatedFromDB(Pill, pillId, ["doses", "history"], "Pill not found")
    return jsonify(response), code

@doseGuardBP.route("/patients/<int:patientId>/all-doses", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def getPatientSchedulesDoses(patientId):
    if not verifyCaregiverPatientRelationship(patientId):
        return jsonify(error="Forbidden: You can only access patients under your care"), 403
    
    response, code = listNestedRelatedFromDB(Patient, patientId, ["schedules", "doses"], "Patient not found")
    return jsonify(response), code

### GET ALL ###
@doseGuardBP.route("/caregivers", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listCaregivers():
    response, code = listFromDB(Caregiver)
    return jsonify(response), code

@doseGuardBP.route("/patients", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listPatients():
    response, code = listFromDB(Patient)
    return jsonify(response), code

@doseGuardBP.route("/pills", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listPills():
    response, code = listFromDB(Pill)
    return jsonify(response), code

@doseGuardBP.route("/doses", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listDoses():
    response, code = listFromDB(Dose)
    return jsonify(response), code

@doseGuardBP.route("/schedules", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listSchedules():
    response, code = listFromDB(Schedule)
    return jsonify(response), code

@doseGuardBP.route("/dose-history", methods=["GET"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def listDoseHistory():
    response, code = listFromDB(DoseHistory)
    return jsonify(response), code

### PATCH ###
@doseGuardBP.route("/caregivers/<int:caregiverId>", methods=["PATCH"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def updateCaregiver(caregiverId):
    if not verifyCaregiverOwnership(caregiverId):
        return jsonify(error="Forbidden: You can only update your own caregiver profile"), 403
    
    data = request.json or {}
    fields = [("name", str, False), ("username", str, False), ("passwordHash", str, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updateCaregiver(caregiverId, upd))

@doseGuardBP.route("/patients/<int:patientId>", methods=["PATCH"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def updatePatient(patientId):
    if not verifyCaregiverPatientRelationship(patientId):
        return jsonify(error="Forbidden: You can only update patients under your care"), 403
    
    data = request.json or {}
    fields = [("name", str, False), ("contact", str, False), ("dob", str, False), ("weight", float, False), ("height", float, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updatePatient(patientId, upd))

@doseGuardBP.route("/pills/<int:pillId>", methods=["PATCH"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def updatePill(pillId):
    if not verifyPillAccess(pillId):
        return jsonify(error="Forbidden: You can only update pills prescribed to your patients"), 403
    
    data = request.json or {}
    fields = [("name", str, False), ("strength", float, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updatePill(pillId, upd))

@doseGuardBP.route("/doses/<int:doseId>", methods=["PATCH"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def updateDose(doseId):
    if not verifyDoseAccess(doseId):
        return jsonify(error="Forbidden: You can only update doses for patients under your care"), 403
    
    data = request.json or {}
    fields = [("pillId", int, False), ("interval", int, False), ("amount", int, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updateDose(doseId, upd))

@doseGuardBP.route("/schedules/<int:scheduleId>", methods=["PATCH"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def updateSchedule(scheduleId):
    if not verifyScheduleAccess(scheduleId):
        return jsonify(error="Forbidden: You can only update schedules for patients under your care"), 403
    
    data = request.json or {}
    fields = [("name", str, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updateSchedule(scheduleId, upd))

@doseGuardBP.route("/dose-history/<int:entryId>", methods=["PATCH"])
@Authorize(Permissions.PRIVATE)
@Ratelimited
def updateDoseHistory(entryId):
    if not verifyDoseHistoryAccess(entryId):
        return jsonify(error="Forbidden: You can only update dose history for patients under your care"), 403
    
    data = request.json or {}
    fields = [("taken", bool, False), ("doseId", int, False), ("patientId", int, False)]

    return handleKwargsEndpoint(data, fields, lambda **upd: _updateDoseHistory(entryId, upd))