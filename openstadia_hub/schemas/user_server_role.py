from enum import Enum


class UserServerRole(str, Enum):
    OWNER = 'owner'
    USER = 'user'
