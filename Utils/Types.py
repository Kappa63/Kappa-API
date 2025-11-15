from typing import Any, Dict, List, Tuple, Callable, Optional
from werkzeug.datastructures import FileStorage
from flask import Response
from enum import Enum

JSONDict = Dict[str, Any]
FieldSpec = Tuple[str, type, bool]
HandlerFunc = Callable[..., Tuple[Dict[str, Any], int]]
ResponsePayload = Tuple[Dict[str, Any], int]