from sqlalchemy.ext.asyncio import AsyncSession

from services.data_subservices.users import Users
from services.data_subservices.roles import Roles
from services.data_subservices.orders import Orders


class Data:
    def __init__(self, async_session: AsyncSession):
        self.users = Users(async_session)
        self.roles = Roles(async_session)
        self.orders = Orders(async_session)
