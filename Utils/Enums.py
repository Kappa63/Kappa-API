from enum import Enum, IntFlag

class Permissions(IntFlag):
    DEFAULT = 0
    GENERAL = 1
    PRIVATE = 2
    ADMIN = 4

class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"