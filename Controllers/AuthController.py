from Utils.Helpers.AuthHelpers import hashPass, verifyPass
from .DBController import getSession
from Models import User

def _registerUser(username: str, password: str) -> tuple[dict, int]:
    """
    Creates a new user

    Parameters:
        ``username`` (``str``):
            username
        ``password`` (``str``):
            password
    Returns:
        ``tuple``:
            Containing:
            - dict keys: `id`, `apiKey`, `username`, `perms`, `createdOn`
            - int: HTTP status code
    """
    with getSession() as session:
        if session.query(User).filter_by(username=username).first():
            return {"error": "User already exists"}, 409
        newUser = User(username=username, passwordHash=hashPass(password))
        session.add(newUser)
        session.flush()
        return {"id": newUser.id, "apiKey": newUser.apiKey, 
                "username": newUser.username, "perms": newUser.perms,
                "createdOn": newUser.createdOn}, 201
    
def _loginUser(username: str, password: str) -> tuple[dict, int]:
    """
    Returns user data

    Parameters:
        ``username`` (``str``):
            username
        ``password`` (``str``):
            password
    Returns:
        ``tuple``:
            Containing:
            - dict keys: `id`, `apiKey`, `username`, `perms`, `createdOn`, `updatedOn`, `lastUse`
            - int: HTTP status code
    """
    with getSession() as session:
        if not (user := session.query(User).filter_by(username=username).first()):
            return {"error": "User does not exist"}, 404
        if (verifyPass(password, user.passwordHash)): # type: ignore
            return {"id": user.id, "apiKey": user.apiKey, 
                    "username": user.username, "perms": user.perms,
                    "createdOn": user.createdOn, "updatedOn": user.updatedOn,
                    "lastUse": user.lastUse}, 200
        return {"error": "Invalid credentials"}, 401