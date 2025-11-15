from Controllers.DBController import getSession

def getFromDB(model, idValue: int, notFoundMessage: str):
    """
    Fetch a single database record by ID.

    Parameters:
        ``model``:
            The SQLAlchemy model class.
        ``idValue`` (``int``):
            The primary key of the record.
        ``notFoundMessage`` (``str``):
            Error message returned if the record does not exist.

    Returns:
        ``tuple``:
            - dict output from ``model.toDict()``.
            - HTTP status code.
    """
    with getSession() as session:
        obj = session.get(model, idValue)
        if not obj:
            return {"error": notFoundMessage}, 404
        return obj.toDict(), 200

def createInDB(model):
    """
    Insert a new SQLAlchemy model instance into the database.

    Parameters:
        ``model``:
            A fully constructed SQLAlchemy model object to be persisted.

    Returns:
        ``model``:
            The same model instance after insertion, including any
            auto-generated fields such as primary keys.
    """
    with getSession() as session:
        session.add(model)
        session.flush()
        return model