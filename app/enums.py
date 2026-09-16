from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Role(Enum):
    USER = "user"
    ADMIN = "admin"
