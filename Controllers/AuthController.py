from Functions.Helpers import hashPass
from .DBController import getSession
from Models import User

def registerUser(uname: str, pwd: str) -> tuple[dict, int]:
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
            - dict keys: `apiKey`, `username`, `perms`, `createdOn`
            - int: HTTP status code
    """
    with getSession() as session:
        existing = session.query(User).filter_by(username=uname).first()
        if existing:
            return {"error": "User already exists"}, 409
        newUser = User(username=uname, passwordHash=hashPass(pwd))
        session.add(newUser)
        session.flush()
        return {"apiKey": newUser.apiKey, "username": newUser.username,
                "perms": newUser.perms, "createdOn": newUser.createdOn}, 201