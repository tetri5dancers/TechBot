from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.webhook import SendMessage
from states.ticket import Ticket
import re

from utils.OneSConnector import OnesDB


def regular_match(text):
    return True if re.search("[Г-г]отово", text) or re.search("✅", text) else False

def search_ticket(tickets, message_id):
    for i in tickets:
        if i['message_id'] == message_id:
            return i
    else:
        return None

async def admin_start(message: Message):
    #await message.reply("Hello, admin!")
    #return SendMessage(message.chat.id, "Hello, admin!", reply_to_message_id=message.message_id)
    return SendMessage(message.chat.id, "Hello, admin!", reply_to_message_id=message.message_id)

async def tickets(message: Message):
    dispatcher = Dispatcher.get_current()
    reply = ""
    num = 1
    for i in dispatcher.tickets:
        reply += f"{num}: {i.get('title')} номер {i.get('ticket_id')} \n"
        num += 1
    #return SendMessage(message.chat.id, f"{reply}", reply_to_message_id=message.message_id)
    return SendMessage(-1001635770778, f"{reply}")

async def ticket_handler(message: Message):
    dispatcher = Dispatcher.get_current()
    if regular_match(message.text) and message.reply_to_message.message_id in list(i['message_id'] for i in dispatcher.tickets)\
            and message.chat.id in list(j['chat_id'] for j in dispatcher.tickets):
        ticket: dict = search_ticket(dispatcher.tickets, message.reply_to_message.message_id)
        if ticket is not None:
            ticket.update({"admin_id": message.from_user.id})
            conn = OnesDB(dispatcher.bot.data['config'].oneSParams.base_url)
            result = await conn.done_task(ticket['ticket_id'], ticket)
            if result["result"]:
                dispatcher.tickets.remove(ticket)
        #await message.reply(f"Заявка №{ticket['ticket_id']} выполнена")
        return SendMessage(-1001635770778, f"Заявка №{ticket['ticket_id']} выполнена")

    #if regular_match(message.text) and message.message_thread_id in list(i['message_id'] for i in dispatcher.tickets):
    #   await message.reply("вызов закрытия тикета ответом на сообщение бота")




def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(tickets, commands=["tickets"], state="*", is_admin=True)
    dp.register_message_handler(ticket_handler, state="*", is_admin=True)