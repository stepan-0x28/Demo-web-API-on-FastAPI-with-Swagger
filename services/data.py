from sqlalchemy.ext.asyncio import AsyncSession

from services.data_sub_services.user import User
from services.data_sub_services.orders import Orders


class Data:
    def __init__(self, async_session: AsyncSession):
        self.user = User(async_session)
        self.orders = Orders(async_session)
