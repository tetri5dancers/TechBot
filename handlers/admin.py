from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.webhook import SendMessage


async def admin_start(message: Message):
    #await message.reply("Hello, admin!")
    return SendMessage(message.chat.id, "Hello, admin!", reply_to_message_id=message.message_id)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
