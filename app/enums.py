from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class SortBy(Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"

class SortOrder(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"
