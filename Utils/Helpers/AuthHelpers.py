from flask import g
import bcrypt
from Models import Permissions
from Config import APIConfig

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