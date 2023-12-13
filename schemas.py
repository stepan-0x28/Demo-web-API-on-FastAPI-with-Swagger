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


class UserOut(BaseUser):
    id: int
    role_id: int


class Response(BaseModel):
    message: str


class Order(BaseModel):
    id: int
    customer_id: int
    executor_id: int
    name: str
    description: str
