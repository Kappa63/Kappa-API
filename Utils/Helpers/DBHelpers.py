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
        if not obj or getattr(obj, "active", True) is False:
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
        return model.toDict()
    
def softDeleteFromDB(model, idValue: int, notFoundMessage: str):
    """
    Soft-delete a database record by setting ``active`` to False.

    Parameters:
        ``model``:
            The SQLAlchemy model class.
        ``idValue`` (``int``):
            Primary key of the record.
        ``notFoundMessage`` (``str``):
            Error message if record does not exist or is already inactive.

    Returns:
        ``tuple``:
            - dict: Result message or error message.
            - int: HTTP status code.
    """
    with getSession() as session:
        obj = session.get(model, idValue)

        if not obj or getattr(obj, "active", True) is False:
            return {"error": notFoundMessage}, 404

        obj.active = False
        session.flush()

        return {"message": "Deleted"}, 200

def hardDeleteLinkFromDB(model, filters: dict, notFoundMessage: str):
    """
    Hard-delete a row from a link/association table.

    Parameters:
        ``model``:
            The SQLAlchemy model class for the link table.
        ``filters`` (``dict``):
            Column-value pairs used to look up the link row.
        ``notFoundMessage`` (``str``):
            Error message if the link does not exist.

    Returns:
        ``tuple``:
            - dict: result or error.
            - int: HTTP status code.
    """
    with getSession() as session:
        obj = session.query(model).filter_by(**filters).first()

        if not obj:
            return {"error": notFoundMessage}, 404

        session.delete(obj)
        session.flush()

        return {"message": "Deleted"}, 200
    
def listFromDB(model):
    """
    Fetch all active records from the given model.

    Returns:
        - List of serialized objects (via toDict())
        - HTTP 200 status code
    """
    with getSession() as session:
        objs = session.query(model).filter_by(active=True).all()
        return [obj.toDict() for obj in objs], 200
    
def updateInDB(model, idValue: int, updates: dict, notFoundMessage: str):
    """
    Update an existing active record by ID.

    Parameters:
        model: SQLAlchemy model class.
        idValue (int): Primary key.
        updates (dict): Fields to update.
        notFoundMessage (str): Error message if not found.

    Returns:
        (dict, int): Updated model serialized, HTTP code.
    """
    with getSession() as session:
        obj = session.get(model, idValue)

        if not obj or getattr(obj, "active", True) is False:
            return {"error": notFoundMessage}, 404

        for key, value in updates.items():
            setattr(obj, key, value)

        session.flush()
        return obj.toDict(), 200

def listRelatedFromDB(model, idValue: int, relationName: str, notFoundMessage: str):
    """
    Fetch a parent object, validate it, extract a relationship, filter active
    children, and serialize them.

    Parameters:
        model: SQLAlchemy model class.
        idValue (int): ID of the parent object.
        relationName (str): Relationship attribute name on the model.
        notFoundMessage (str): Error when parent not found.

    Returns:
        tuple:
            - list of serialized children
            - HTTP status code
    """
    with getSession() as session:
        parent = session.get(model, idValue)
        if not parent or not parent.active:
            return {"error": notFoundMessage}, 404

        related = getattr(parent, relationName, None)
        if related is None:
            return {"error": f"Relationship '{relationName}' does not exist"}, 500

        results = [obj.toDict() for obj in related if getattr(obj, "active", True)]
        return results, 200

def listNestedRelatedFromDB(model, idValue: int, path: list[str], notFoundMessage: str):
    """
    Traverse a multi-level relationship chain starting from a root model and
    return all nested related objects.

    Parameters:
        ``model``:
            The SQLAlchemy model class used as the root of the lookup.

        ``idValue`` (``int``):
            The primary key value of the root record.

        ``path`` (``list[str]``):
            Ordered list of relationship names to traverse.
            Example: ["schedules", "doses"] will fetch all doses across
            all schedules belonging to the root object.

        ``notFoundMessage`` (``str``):
            Error message returned if the root object does not exist
            or is marked inactive.

    Returns:
        ``tuple``:
            - ``list``: A list of serialized objects from the final
              relationship level, using ``toDict()``.
            - ``int``: HTTP status code.
                - ``200`` on success.
                - ``404`` if the root object is not found or inactive.
                - ``500`` if a relationship in the chain does not exist.

    Notes:
        - Only objects with ``active == True`` are included.
        - Supports any depth of traversal as long as each relationship
          name in ``path`` exists on the previous model.
    """
    with getSession() as session:
        obj = session.get(model, idValue)
        if not obj or not obj.active:
            return {"error": notFoundMessage}, 404

        current = [obj]

        for rel in path:
            nextRelation = []
            for item in current:
                related = getattr(item, rel, None)
                if related is None:
                    return {"error": f"Relationship '{rel}' not found"}, 500

                nextRelation.extend([child for child in related if getattr(child, "active", True)])

            current = nextRelation

        return [c.toDict() for c in current], 200
