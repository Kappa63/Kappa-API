from Models import User, DetachedUser
from Utils.Helpers.DBHelpers import getFromDB, softDeleteFromDB

def _getUser(u: DetachedUser) -> tuple[dict, int]:
    """
    Returns user data

    Parameters:
        ``u`` (``DetachedUser``):
            Detached user object from authorize
    Returns:
        ``tuple``:
            Containing:
            - dict keys: `id`, `apiKey`, `username`, `perms`, `createdOn`, `updatedOn`, `lastUse`
            - int: HTTP status code
    """
    return getFromDB(User, u.id, "User not found")

def _deleteUser(u: DetachedUser) -> tuple[dict, int]:
    """
    Deletes user data

    Parameters:
        ``u`` (``DetachedUser``):
            Detached user object from authorize
    Returns:
        ``tuple``:
             - dict: result message
             - int: HTTP status code
    """
    return softDeleteFromDB(User, u.id, "User not found")