from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Boolean

Base = declarative_base()


class Role(Base):
    # noinspection SpellCheckingInspection
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)


class User(Base):
    # noinspection SpellCheckingInspection
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('roles.id'), nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    role = relationship(Role)


class Status(Base):
    # noinspection SpellCheckingInspection
    __tablename__ = 'statuses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)


class Order(Base):
    # noinspection SpellCheckingInspection
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    executor_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey('statuses.id'), nullable=False)
    is_deleted: Mapped[int] = mapped_column(Boolean, nullable=False, default=False)

    customer = relationship(User, foreign_keys=[customer_id])
    executor = relationship(User, foreign_keys=[executor_id])
    status = relationship(Status)
