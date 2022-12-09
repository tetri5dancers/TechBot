from aiogram.types.message import Message
from aiogram.dispatcher import Dispatcher

from utils.OneSConnector import OnesDB


async def user_input(message: Message, intent: str):
    dp = Dispatcher.get_current()
    if intent.startswith("ticket"):
        data = {"message_id": message.message_id, "chat_id": message.chat.id, "intent": intent, "chat_type": message.chat.type}
        conn = OnesDB(dp.bot.data['config'].oneSParams.base_url)
        result = await conn.add_task(data)
        if result["result"]:
            await message.reply(f"Задача номер {result['ticket_code']} успешно добавлена")
        else:
            await message.reply(f"Произошла ошибка")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_input, state="*")
