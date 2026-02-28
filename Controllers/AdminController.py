from datetime import datetime
from .DBController import getSession
from Utils.Enums import Permissions
from Utils.Helpers.DBHelpers import listFromDB, updateInDB
from Models import User

def _patchUser(uid: int, newData: dict) -> tuple[dict, int]:
    """
    Update a user

    Parameters:
        ``uid`` (``int``):
            user's id
        ``newData`` (``dict``):
            containing the elements to modify

    Returns:
        ``tuple``:
            Containing:
            - dict keys: `id`, `apiKey`, `username`, `perms`, `createdOn`
            - int: HTTP status code
    """
    updates = {}
    
    if (dt := newData.get("username")):
        with getSession() as session:
            # Check if username exists and doesn't belong to current user
            exists = session.query(User).filter(User.username == dt, User.id != uid).first()
            if exists:
                return {"error": "Username already exists"}, 409
        updates["username"] = dt

    if (dt := newData.get("perms")):
        updates["perms"] = Permissions(int(dt)).value # type: ignore

    return updateInDB(User, uid, updates, "User does not exist")
    
def _listUsers() -> tuple[list[dict], int]:
    """
    Lists all users

    Returns:
        ``tuple``:
            Containing:
            - list[dict] keys: `id`, `apiKey`, `username`, `perms`, `createdOn`, `updatedOn`, `lastUse`
            - int: HTTP status code
    """
    return listFromDB(User)