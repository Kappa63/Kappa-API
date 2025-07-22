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
