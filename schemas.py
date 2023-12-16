from pydantic import BaseModel
from fastapi import Form
from typing import Annotated

from utilities import remove_keys


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserData(BaseModel):
    first_name: str
    last_name: str

    @classmethod
    def as_form(cls, first_name: Annotated[str, Form()], last_name: Annotated[str, Form()]) -> BaseModel:
        return cls(**remove_keys(locals(), 'cls'))


class BaseUser(UserData):
    username: str


class UserIn(BaseUser):
    password: str
    role_id: int

    # noinspection PyMethodOverriding
    @classmethod
    def as_form(cls, first_name: Annotated[str, Form()], last_name: Annotated[str, Form()],
                username: Annotated[str, Form()], password: Annotated[str, Form()],
                role_id: Annotated[str, Form()]) -> BaseUser:
        return cls(**remove_keys(locals(), 'cls'))


class Role(BaseModel):
    id: int
    key: str
    name: str
    description: str


class UserOut(BaseUser):
    id: int
    role_id: int


class Response(BaseModel):
    message: str


class Status(BaseModel):
    id: int
    key: str
    name: str
    description: str


class OrderIn(BaseModel):
    executor_id: int
    name: str
    description: str

    @classmethod
    def as_form(cls, executor_id: Annotated[int, Form()], name: Annotated[str, Form()],
                description: Annotated[str, Form()]) -> BaseModel:
        return cls(**remove_keys(locals(), 'cls'))


class OrderOut(OrderIn):
    id: int
    customer_id: int
    status_id: int
    is_deleted: bool
