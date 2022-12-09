import asyncio
import json
from datetime import datetime

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher import Dispatcher
from utils.OneSConnector import OnesDB


class Connector(BaseMiddleware):
    def __init__(self, address):
        super().__init__()
        self.connector = OnesDB(address)


class ProcessMessage(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        dispatcher = Dispatcher.get_current()
        conn = OnesDB(dispatcher.bot.data['config'].oneSParams.base_url)
        if message.text is not None:
            data["intent"] = dispatcher.get_intent(message.text)
            msg = message.to_python()
            print(msg)
            #msg = msg.update({"date": datetime.now()})
            result = await conn.message_process(msg)

    async def on_process_callback_query(self, cq: types.CallbackQuery):
        print("Processing callback query")