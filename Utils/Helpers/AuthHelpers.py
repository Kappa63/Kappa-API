from Models import PatientSchedule, CaregiverPatient, Caregiver, Dose, ScheduleDoses, DoseHistory, Schedule, Pill
from Utils.Enums import Permissions
from Config import APIConfig
from flask import g
import bcrypt
import sqlalchemy as sa

def hashPass(passStr: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Parameters:
        ``passStr`` (``str``):
            The plaintext password.

    Returns:
        ``str``:
            The hashed password.
    """
    hashed = bcrypt.hashpw(passStr.encode(), bcrypt.gensalt())
    return hashed.decode()


def verifyPass(passStr: str, passHash: str) -> bool:
    """
    Verify a plaintext password against its stored hash.

    Parameters:
        ``passStr`` (``str``):
            The plaintext password.

        ``passHash`` (``str``):
            The stored bcrypt hash.

    Returns:
        ``bool``:
            True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(passStr.encode(), passHash.encode())


def getUserRatelimit() -> str:
    """
    Provide the rate limit for the current user based on their permissions.

    Returns:
        ``str``:
            The rate limit string applicable to the user.
    """
    user = getattr(g, "user", None)
    if not user:
        return APIConfig.NOT_USER_RATELIMIT

    if user.perms & Permissions.ADMIN:
        return APIConfig.ADMIN_RATELIMIT
    elif user.perms & Permissions.PRIVATE:
        return APIConfig.PRIVATE_RATELIMIT
    else:
        return APIConfig.GENERAL_RATELIMIT


def getCaregiverIdFromRequest():
    """
    Get the caregiver ID associated with the authenticated user from the request context.

    Returns:
        ``int | None``:
            The caregiver ID if found, None otherwise.
    """
    from Controllers.DBController import getSession
    
    if not (user := getattr(g, "user", None)):
        return None
    
    with getSession() as session:
        caregiver = session.query(Caregiver).filter_by(userId=user.id, active=True).first()
        return caregiver.id if caregiver else None


def verifyCaregiverOwnership(requestedCaregiverId: int) -> bool:
    """
    Verify that the authenticated user owns the requested caregiver profile.

    Parameters:
        ``requestedCaregiverId`` (``int``):
            The caregiver ID being requested.

    Returns:
        ``bool``:
            True if the user owns the caregiver profile, False otherwise.
    """
    authenticatedCaregiverId = getCaregiverIdFromRequest()
    return authenticatedCaregiverId == requestedCaregiverId


def verifyCaregiverPatientRelationship(patientId: int) -> bool:
    """
    Verify that the patient is under the care of the authenticated caregiver.

    Parameters:
        ``patientId`` (``int``):
            The patient ID to check.

    Returns:
        ``bool``:
            True if the patient is under the caregiver's care, False otherwise.
    """
    from Controllers.DBController import getSession
    
    if not (caregiverId := getCaregiverIdFromRequest()):
        return False
    
    with getSession() as session:
        relationship = session.query(CaregiverPatient).filter_by(
            caregiverId=caregiverId,
            patientId=patientId
        ).first()
        return relationship is not None


def verifyScheduleAccess(scheduleId: int) -> bool:
    """
    Verify that the authenticated caregiver owns the requested schedule.

    Parameters:
        ``scheduleId`` (``int``):
            The schedule ID to check.

    Returns:
        ``bool``:
            True if the caregiver owns the schedule, False otherwise.
    """    
    from Controllers.DBController import getSession
    
    if not (caregiverId := getCaregiverIdFromRequest()):
        return False
    
    with getSession() as session:
        schedule = session.get(Schedule, scheduleId)
        if not schedule or not schedule.active:
            return False
        return schedule.createdBy == caregiverId


def verifyPillAccess(pillId: int) -> bool:
    """
    Verify that the authenticated caregiver owns the requested pill.

    Parameters:
        ``pillId`` (``int``):
            The pill ID to check.

    Returns:
        ``bool``:
            True if the caregiver owns the pill, False otherwise.
    """   
    from Controllers.DBController import getSession
    
    if not (caregiverId := getCaregiverIdFromRequest()):
        return False
    
    with getSession() as session:
        pill = session.get(Pill, pillId)
        if not pill or not pill.active:
            return False
        return pill.createdBy == caregiverId


def verifyDoseAccess(doseId: int) -> bool:
    """
    Verify that the authenticated caregiver owns the requested dose.

    Parameters:
        ``doseId`` (``int``):
            The dose ID to check.

    Returns:
        ``bool``:
            True if the caregiver owns the dose, False otherwise.
    """
    from Controllers.DBController import getSession
    
    if not (caregiverId := getCaregiverIdFromRequest()):
        return False
    
    with getSession() as session:
        dose = session.get(Dose, doseId)
        if not dose or not dose.active:
            return False
        return dose.createdBy == caregiverId


def verifyDoseHistoryAccess(entryId: int) -> bool:
    """
    Verify that the authenticated caregiver has access to the requested dose history entry
    (i.e., the entry belongs to a patient under their care).

    Parameters:
        ``entryId`` (``int``):
            The dose history entry ID to check.

    Returns:
        ``bool``:
            True if the caregiver has access, False otherwise.
    """
    from Controllers.DBController import getSession
    
    if not (caregiverId := getCaregiverIdFromRequest()):
        return False
    
    with getSession() as session:
        entry = session.query(DoseHistory).filter_by(id=entryId, active=True).first()
        if not entry:
            return False
        
        return verifyCaregiverPatientRelationship(entry.patientId)