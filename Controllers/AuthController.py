from Utils.Helpers.AuthHelpers import hashPass, verifyPass
from .DBController import getSession
from Models import User

def _registerUser(uname: str, pwd: str) -> tuple[dict, int]:
    """
    Creates a new user

    Parameters:
        ``uname`` (``str``):
            username
        ``pwd`` (``str``):
            password
    Returns:
        ``tuple``:
            Containing:
            - dict keys: `id`, `apiKey`, `username`, `perms`, `createdOn`
            - int: HTTP status code
    """
    with getSession() as session:
        if session.query(User).filter_by(username=uname).first():
            return {"error": "User already exists"}, 409
        newUser = User(username=uname, passwordHash=hashPass(pwd))
        session.add(newUser)
        session.flush()
        return {"id": newUser.id, "apiKey": newUser.apiKey, 
                "username": newUser.username, "perms": newUser.perms,
                "createdOn": newUser.createdOn}, 201
    
def _loginUser(uname: str, pwd: str) -> tuple[dict, int]:
    """
    Returns user data

    Parameters:
        ``uname`` (``str``):
            username
        ``pwd`` (``str``):
            password
    Returns:
        ``tuple``:
            Containing:
            - dict keys: `id`, `apiKey`, `username`, `perms`, `createdOn`, `updatedOn`, `lastUse`
            - int: HTTP status code
    """
    with getSession() as session:
        if not (user := session.query(User).filter_by(username=uname).first()):
            return {"error": "User does not exist"}, 404
        if (verifyPass(pwd, user.passwordHash)): # type: ignore
            return {"id": user.id, "apiKey": user.apiKey, 
                    "username": user.username, "perms": user.perms,
                    "createdOn": user.createdOn, "updatedOn": user.updatedOn,
                    "lastUse": user.lastUse}, 200
        return {"error": "Invalid credentials"}, 401