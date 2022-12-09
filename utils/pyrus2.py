import aiohttp
import asyncio
from config import pyrus_login, pyrus_secret


class PyrusClient:

    def __init__(self, login, secret):
        self.admins = {}
        self.ticket_types = {}
        self.update_timer = 0
        self.login = login
        self.secret = secret
        self.loop = asyncio.get_event_loop()
        self.token = "n"
        self.schedule_update_token()

    async def authorise(self):
        auth_url = 'https://api.pyrus.com/v4/auth'
        auth_file = {
            "login": self.login,
            "security_key": self.secret
        }

        session = aiohttp.ClientSession()
        resp = await session.post(auth_url, json=auth_file)
        response = await resp.json()
        self.token = response.get('access_token')
        await session.close()
        self.update_timer = 86400
        self.schedule_update_token()

    def schedule_update_token(self):
        self.loop.call_later(self.update_timer, self.update_token_task, self.loop)

    def update_token_task(self, loop):
        asyncio.ensure_future(self.authorise(), loop=loop)

    def get_token(self):
        return self.token

    async def create_task(self, message, intent):
        task = {
            "form_id": 1099340,
            "fields": [
                {
                    "id": 14,
                    "value": message.from_user.full_name
                },
                {
                    "id": 1,
                    "value": self.ticket_types.get(intent)
                },
                {
                    "id": 2,
                    "value": message.text if not None else message.caption
                },
                {
                    "id": 22,
                    "value": f"{message.from_user.id}"
                },
            ]
        }
        url = 'https://api.pyrus.com/v4/tasks/'
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        pass

    async def add_comment(self, task_id, message, activity_action=None):
        if self.is_admin(message.from_user.id):
            assigned = self.is_admin(message.from_user.id)
            comment = {
                "Text": f"{message.from_user.full_name}: {message.text}",
                "reassign_to": {"id": assigned},
                "field_updates": [
                    {
                        "id": 23,
                        "value": {
                            "id": assigned
                        }
                    }
                ]
            }
        else:
            comment = {
                "Text": f"{message.from_user.full_name}: {message.text}",
            }
        comment_url = f'https://api.pyrus.com/v4/tasks/{task_id}/comments'
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        pass

    async def close_task(self, task_id, message, activity_action=None):
        comment = {
            "action": activity_action,
        }
        comment_url = f'https://api.pyrus.com/v4/tasks/{task_id}/comments'
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        pass

    async def attach_file(self):
        pass

    def is_admin(self, id, field=0):
        return self.admins.get(id)[field] if self.admins.get(id) is not None else False

    def send_data(self):
        pass


async def main():
    client = PyrusClient(pyrus_login, pyrus_secret)
    while True:
        await asyncio.sleep(1)
        print(client.get_token())


if __name__ == "__main__":
    asyncio.run(main())


