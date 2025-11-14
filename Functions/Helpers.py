from Models import Permissions
from flask import g
import bcrypt
from Config import APIConfig

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
    if not (p := getattr(g, "user", None)):
        return APIConfig.NOT_USER_RATELIMIT

    if p.perms & Permissions.ADMIN:
        return APIConfig.ADMIN_RATELIMIT
    elif p.perms & Permissions.PRIVATE:
        return APIConfig.PRIVATE_RATELIMIT
    else:
        return APIConfig.GENERAL_RATELIMIT
    