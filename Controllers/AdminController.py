from datetime import datetime, timezone
from .DBController import getSession
from Utils.Enums import Permissions
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
    with getSession() as session:
        if not (user := session.query(User).filter_by(id=uid).first()):
            return {"error": "User does not exist"}, 404
        
        if (dt := newData.get("username")):
            exists = session.query(User).filter_by(username=dt).first()
            if exists:
                return {"error": "Username already exists"}, 409
            user.username = dt

        if (dt := newData.get("perms")):
            user.perms = Permissions(int(dt)).value # type: ignore
        user.updatedOn = datetime.now(timezone.utc) # type: ignore

        return {"id": user.id, "apiKey": user.apiKey, 
                "username": user.username, "perms": user.perms,
                "createdOn": user.createdOn}, 200
    
def _listUsers() -> tuple[list[dict], int]:
    """
    Lists all users

    Returns:
        ``tuple``:
            Containing:
            - list[dict] keys: `id`, `apiKey`, `username`, `perms`, `createdOn`, `updatedOn`, `lastUse`
            - int: HTTP status code
    """
    with getSession() as session:
        users = session.query(User).all()
        return [{
                    "id": user.id,
                    "apiKey": user.apiKey,
                    "username": user.username,
                    "perms": user.perms,
                    "createdOn": user.createdOn,
                    "updatedOn": user.updatedOn,
                    "lastUse": user.lastUse
                } for user in users], 200