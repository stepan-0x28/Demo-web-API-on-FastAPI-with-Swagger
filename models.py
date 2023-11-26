from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, UniqueConstraint

Base = declarative_base()


# noinspection SpellCheckingInspection
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('login', name='users_un'),)
