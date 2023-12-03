from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Order(BaseModel):
    id: int
    customer_id: int
    executor_id: int
    name: str
    description: str
