import asyncio
import aiohttp
import json
from aiogram.types.message import Message


class OnesDB():
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.admins = {}
        self.loop = asyncio.get_event_loop()
        #self.schedule_task(self.get_init_data)
        self.last_status = None
        self.init_data = None

    async def get_init_data(self):
        url = self.baseUrl + '/init'
        self.init_data = await self.request(url, "GET")

    async def request(self, url, method, json=None):
        session = aiohttp.ClientSession()

        async with session.request(method, url, json=json) as resp:
            self.last_status = resp.status
            response = await resp.json()
        await session.close()
        return response

    def add_coro(self, loop, func):
        asyncio.ensure_future(func(), loop=loop)

    def schedule_task(self, func):
        self.loop.call_later(0, self.add_coro, self.loop, func)

    async def message_process(self, message):
        url = self.baseUrl + '/message'
        result = await self.request(url, "POST", message)
        return result

    def get_last_status(self):
        return self.last_status

    def get_tasks(self):
        pass

    def get_task(self):
        pass

    async def add_task(self, data):
        url = self.baseUrl + '/ticket'
        result = await self.request(url, "POST", data)
        return result

    def remove_task(self):
        pass

    def get_comments(self):
        pass

    def add_comment(self):
        pass

    def add_file(self):
        pass

    def get_updates(self):
        pass




async def main():
    client = OnesDB('http://10.3.1.20/itservices/hs/bot')
    while client.get_last_status() == None:
        await asyncio.sleep(1)

    print(client.get_last_status())



if __name__ == "__main__":
    asyncio.run(main())