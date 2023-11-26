from pydantic import BaseModel


class HelloWorld(BaseModel):
    message: str = 'Hello World'


class User(BaseModel):
    id: int
    login: str
    password: str
