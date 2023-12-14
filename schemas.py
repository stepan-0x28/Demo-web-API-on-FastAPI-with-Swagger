from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserData(BaseModel):
    first_name: str
    last_name: str


class BaseUser(UserData):
    username: str


class UserIn(BaseUser):
    password: str
    role_id: int


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


class Order(BaseModel):
    id: int
    customer_id: int
    executor_id: int
    name: str
    description: str
    status_id: int
