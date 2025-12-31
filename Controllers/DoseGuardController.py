from Models import (User, Caregiver, Patient, Pill, Dose, Schedule, ScheduleDoses,
                    CaregiverPatient, PatientSchedule, DoseHistory)
from Utils.Helpers.DBHelpers import createInDB, hardDeleteLinkFromDB, updateInDB, getFromDB
from Controllers.DBController import getSession
from Utils.Types import ResponsePayload
from Utils.Enums import Permissions
from Utils.Helpers.AuthHelpers import hashPass, verifyPass
from datetime import datetime

### CREATE ###
def _registerCaregiver(name: str, username: str, password: str) -> ResponsePayload:
    user = createInDB(User(
        username=username, 
        passwordHash=hashPass(password), 
        perms=Permissions.PRIVATE
    ))

    return createInDB(Caregiver(
        name=name, 
        userId=user["id"]
    )), 201

def _loginCaregiver(username: str, password: str) -> tuple[dict, int]:
    with getSession() as session:
        caregiver = session.query(Caregiver).join(User).filter(User.username == username).first()
        
        if not caregiver:
            return {"error": "Caregiver does not exist"}, 404
        
        user = caregiver.user
        
        if verifyPass(password, user.passwordHash): # type: ignore
            return {
                "id": caregiver.id,
                "name": caregiver.name,
                "apiKey": user.apiKey,
                "username": user.username,
                "perms": user.perms,
                "createdOn": user.createdOn,
                "updatedOn": user.updatedOn,
                "lastUse": user.lastUse
            }, 200
        
        return {"error": "Invalid credentials"}, 401

def _createPatient(name: str, contact: str = None, dob: str = None,
                   weight: float = None, height: float = None) -> ResponsePayload:
    return createInDB(Patient(
        name=name,
        contact=contact,
        dob=datetime.fromisoformat(dob).date() if dob else None,
        weight=weight,
        height=height
    )), 201
    
def _createPill(name: str, strength: float) -> ResponsePayload:
    return createInDB(Pill(
        name=name,
        strength=strength
    )), 201
    
def _createDose(pillId: int, interval: int, amount: int) -> ResponsePayload:
    return createInDB(Dose(
        pillId=pillId,
        interval=interval,
        amount=amount
    )), 201

def _createSchedule(name: str) -> ResponsePayload:
    return createInDB(Schedule(
        name=name
    )), 201
    
def _attachDoseToSchedule(scheduleId: int, doseId: int) -> ResponsePayload:
    return createInDB(ScheduleDoses(
        scheduleId=scheduleId,
        doseId=doseId
    )), 201
    
def _attachScheduleToPatient(patientId: int, scheduleId: int) -> ResponsePayload:
    return createInDB(PatientSchedule(
        patientId=patientId,
        scheduleId=scheduleId
    )), 201
    
def _attachPatientToCaregiver(caregiverId: int, patientId: int) -> ResponsePayload:
    return createInDB(CaregiverPatient(
        caregiverId=caregiverId,
        patientId=patientId
    )), 201
    
def _createDoseHistory(patientId: int, doseId: int, taken: bool) -> ResponsePayload:
    return createInDB(DoseHistory(
        patientId=patientId,
        doseId=doseId,
        taken=taken
    )), 201

### DELETE ###
def _deleteDoseFromSchedule(payload: dict):
    return hardDeleteLinkFromDB(
        ScheduleDoses,
        {"scheduleId": payload["scheduleId"], "doseId": payload["doseId"]},
        "Schedule-dose link not found"
    )

def _deleteScheduleFromPatient(payload: dict):
    return hardDeleteLinkFromDB(
        PatientSchedule,
        {"patientId": payload["patientId"], "scheduleId": payload["scheduleId"]},
        "Patient-schedule link not found"
    )

def _deletePatientFromCaregiver(payload: dict):
    return hardDeleteLinkFromDB(
        CaregiverPatient,
        {"caregiverId": payload["caregiverId"], "patientId": payload["patientId"]},
        "Caregiver-patient link not found"
    )

### UPDATE ###
def _updateCaregiver(caregiverId: int, updates: dict):
    with getSession() as session:
        caregiver = session.get(Caregiver, caregiverId)

        if not caregiver or not caregiver.active:
            return {"error": "Caregiver not found"}, 404

        if "name" in updates:
            caregiver.name = updates["name"]

        user = caregiver.user

        if "username" in updates:
            user.username = updates["username"]

        if "passwordHash" in updates:
            user.passwordHash = updates["passwordHash"]

        session.flush()
        return caregiver.toDict(), 200


def _updatePatient(patientId: int, updates: dict):
    return updateInDB(Patient, patientId, updates, "Patient not found")

def _updatePill(pillId: int, updates: dict):
    return updateInDB(Pill, pillId, updates, "Pill not found")

def _updateDose(doseId: int, updates: dict):
    return updateInDB(Dose, doseId, updates, "Dose not found")

def _updateSchedule(scheduleId: int, updates: dict):
    return updateInDB(Schedule, scheduleId, updates, "Schedule not found")

def _updateDoseHistory(entryId: int, updates: dict):
    return updateInDB(DoseHistory, entryId, updates, "Dose history not found")