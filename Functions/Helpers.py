from Models import Permissions
from flask import g
import bcrypt

def hashPass(passStr: str) -> str:
    """
    Hash Password using bcrypt

    Parameters:
        ``passStr`` (``str``):
            The string password
    Returns:
        ``str``: The hashed password
    """
    hashed = bcrypt.hashpw(passStr.encode(), bcrypt.gensalt())
    return hashed.decode()

def verifyPass(passStr: str, passHash: str) -> bool:
    """
    Check password using

    Parameters:
        ``passStr`` (``str``):
            The string password

        ``passHash`` (``str``):
            The hash password
    Returns:
        ``bool``: Whether password is correct
    """
    return bcrypt.checkpw(passStr.encode(), passHash.encode())

def getUserRatelimit() -> str:
    """
    Get the user's rate limit via their permissions

    Returns:
        ``str``: The rate limit string
    """
    if not (p := g.user):
        return "2/minute"

    if p.perms & Permissions.ADMIN:
        return "1000/minute"
    elif p.perms & Permissions.PRIVATE:
        return "100/minute"
    else:
        return "10/minute"
    