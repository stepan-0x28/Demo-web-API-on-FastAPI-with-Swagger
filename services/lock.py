import asyncio


class Lock:
    def __init__(self):
        self.__service_lock = asyncio.Lock()

        self.__locks = {}

    def __create_lock(self, key: str) -> asyncio.Lock:
        lock = asyncio.Lock()

        self.__locks[key] = lock

        return lock

    async def get_lock(self, key: str) -> asyncio.Lock:
        async with self.__service_lock:
            lock = self.__locks.get(key)

            if not lock:
                lock = self.__create_lock(key)

            return lock
