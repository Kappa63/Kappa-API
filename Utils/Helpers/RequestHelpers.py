from flask import jsonify
from werkzeug.datastructures import FileStorage
from enum import Enum
from Utils.Types import Any, Tuple, Optional, List, FieldSpec, HandlerFunc, JSONDict, Response

def requireField(data: dict, key: str) -> Tuple[Optional[Any], Optional[Response], Optional[int]]:
    """
    Validate that a required key exists in request data.

    Parameters:
        ``data`` (``dict``):
            The request JSON payload.
        ``key`` (``str``):
            The required field name.

    Returns:
        ``tuple``:
            - The extracted value (or ``None`` if missing).
            - ``jsonify`` error response on error.
            - HTTP status code on error.
    """
    if key not in data:
        return None, jsonify({"error": f"{key} required"}), 400
    return data[key], None, None


def convertField(value: Any, expectedType: type, key: str):
    """
    Convert a field value into a required type.

    Parameters:
        ``value`` (``any``):
            The raw value.
        ``expectedType`` (``type``):
            The desired type.
        ``key`` (``str``):
            The field name.

    Returns:
        ``tuple``:
            - Converted value or ``None``.
            - Error response or ``None``.
            - Error code or ``None``.
    """
    try:
        if expectedType == bool:
            lower = str(value).lower()
            if lower in ["true", "1", "yes"]:
                return True, None, None
            if lower in ["false", "0", "no"]:
                return False, None, None
            return None, jsonify({"error": f"Invalid bool for field '{key}'"}), 400

        return expectedType(value), None, None

    except (ValueError, TypeError):
        return None, jsonify({
            "error": f"Invalid type for field '{key}', expected {expectedType.__name__}"
        }), 400


def handleEndpoint(data: JSONDict, fields: List[FieldSpec], func: HandlerFunc) -> Tuple[Response, int]:
    """
    Validate endpoint input fields, convert them to their correct types,
    and pass them to the handler function.

    Parameters:
        ``data`` (``dict``):
            The request JSON payload.
        ``fields`` (``list``):
            Field definitions in the format (name, type, required).
        ``func`` (``callable``):
            Handler function invoked after validation.

    Returns:
        ``tuple``:
            - ``jsonify`` response dict.
            - HTTP status code.
    """
    finalFields = {}

    for field, expectedType, isRequired in fields:
        if isRequired:
            value, err, code = requireField(data, field)
            if err:
                return err, code
        else:
            if field not in data:
                continue
            value = data[field]

        if isinstance(value, FileStorage):
            finalFields[field] = value
            continue

        if isinstance(expectedType, type) and issubclass(expectedType, Enum):
            lowerVal = str(value).lower()
            acceptedVals = {e.value.lower(): e for e in expectedType}

            if lowerVal not in acceptedVals:
                return jsonify({
                    "error": f"Invalid value for '{field}', expected one of {[e.value for e in expectedType]}"
                }), 400

            finalFields[field] = acceptedVals[lowerVal]
            continue

        value, err, code = convertField(value, expectedType, field)
        if err:
            return err, code

        finalFields[field] = value

    response, code = func(**finalFields)
    return jsonify(response), code
