from enum import StrEnum


class Roles(StrEnum):
    CUSTOMER = 'customer'
    EXECUTOR = 'executor'


class Statuses(StrEnum):
    NEW = 'new'
