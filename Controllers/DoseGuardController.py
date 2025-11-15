from Models import Caregiver, Patient, Pill, Dose, Schedule, ScheduleDoses, CaregiverPatient, PatientSchedule, DoseHistory
from Utils.Helpers.DBHelpers import createInDB, hardDeleteLinkFromDB, updateInDB
from Utils.Types import ResponsePayload

### CREATE ###
def _createCaregiver(name: str, username: str, passwordHash: str) -> ResponsePayload:
    caregiver = Caregiver(
        name=name,
        username=username,
        passwordHash=passwordHash
    )
    caregiver = createInDB(caregiver)

    return caregiver.toDict(), 201
    
def _createPatient(name: str, contact: str = None, age: int = None,
                   weight: float = None, height: float = None) -> ResponsePayload:
    patient = Patient(
        name=name,
        contact=contact,
        age=age,
        weight=weight,
        height=height
    )
    patient = createInDB(patient)

    return patient.toDict(), 201
    
def _createPill(name: str, strength: float) -> ResponsePayload:
    pill = Pill(
        name=name,
        strength=strength
    )
    pill = createInDB(pill)

    return pill.toDict(), 201
    
def _createDose(pillId: int, interval: int, amount: int) -> ResponsePayload:
    dose = Dose(
        pillId=pillId,
        interval=interval,
        amount=amount
    )
    dose = createInDB(dose)

    return dose.toDict(), 201

def _createSchedule(name: str) -> ResponsePayload:
    schedule = Schedule(
        name=name
    )
    schedule = createInDB(schedule)

    return schedule.toDict(), 201
    
def _attachDoseToSchedule(scheduleId: int, doseId: int) -> ResponsePayload:
    link = ScheduleDoses(
        scheduleId=scheduleId,
        doseId=doseId
    )
    link = createInDB(link)

    return link.toDict(), 201
    
def _attachScheduleToPatient(patientId: int, scheduleId: int) -> ResponsePayload:
    link = PatientSchedule(
        patientId=patientId,
        scheduleId=scheduleId
    )
    link = createInDB(link)

    return link.toDict(), 201
    
def _attachPatientToCaregiver(caregiverId: int, patientId: int) -> ResponsePayload:
    link = CaregiverPatient(
        caregiverId=caregiverId,
        patientId=patientId
    )
    link = createInDB(link)

    return link.toDict(), 201
    
def _createDoseHistory(patientId: int, doseId: int, taken: bool) -> ResponsePayload:
    entry = DoseHistory(
        patientId=patientId,
        doseId=doseId,
        taken=taken
    )
    entry = createInDB(entry)

    return entry.toDict(), 201

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
    return updateInDB(Caregiver, caregiverId, updates, "Caregiver not found")

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