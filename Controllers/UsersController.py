from Models import User, DetachedUser
from .DBController import getSession

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
    with getSession() as session:
        if not (user := session.query(User).filter_by(id=u.id).first()):
            return {"error": "User not found"}, 404
        return {"id": user.id, "apiKey": user.apiKey, 
                "username": user.username, "perms": user.perms,
                "createdOn": user.createdOn, "updatedOn": user.updatedOn,
                "lastUse": user.lastUse}, 200

def _deleteUser(u: User) -> int:
    """
    Deletes user data

    Parameters:
        ``u`` (``DetachedUser``):
            Detached user object from authorize
    Returns:
      - int: HTTP status code
    """
    with getSession() as session:
        if not (user := session.query(User).filter_by(id=u.id).first()):
            return 404
        
        session.delete(user)

        return 200