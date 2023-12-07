from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: int
    username: str
    role_id: int
    first_name: str
    last_name: str


class Order(BaseModel):
    id: int
    customer_id: int
    executor_id: int
    name: str
    description: str
