from aiogram.types.message import Message, ContentType
from states.ticket import Ticket
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.webhook import SendMessage

from utils.OneSConnector import OnesDB


async def user_q1_state_input(message: Message, state: FSMContext):
    """
    Handling user comments and pass it to DB
    :param message:
    :param state:
    :return:
    """
    pass


async def user_photo(message: Message, intent: str = None, state: FSMContext = None):
    """

    :param message:
    :param intent:
    :param state:
    :return:
    """
    dp = Dispatcher.get_current()
    if message.caption is None:
        return
    if intent is None:
        return
    if intent.startswith("ticket"):
        data = {"message_id": message.message_id, "chat_id": message.chat.id, "intent": intent, "chat_type": message.chat.type}
        conn = OnesDB(dp.bot.data['config'].oneSParams.base_url)
        result = None
        try:
            result = await conn.add_task(data)
        except Exception as ex:
            result = None
            print(ex)
        finally:
            if result is not None:
                dp.tickets.append(result)
                #await message.reply(f"Задача номер {result['ticket_id']} успешно добавлена")
                return SendMessage(-1001635770778, f"Задача номер {result['ticket_id']} успешно добавлена")


async def user_input(message: Message, intent: str, state: FSMContext):
    """

    :param message:
    :param intent:
    :param state:
    :return: Diagnostic message
    """
    dp = Dispatcher.get_current()
    if intent.startswith("ticket"):
        data = {"message_id": message.message_id, "chat_id": message.chat.id, "intent": intent, "chat_type": message.chat.type}
        conn = OnesDB(dp.bot.data['config'].oneSParams.base_url)
        result = None
        try:
            result = await conn.add_task(data)
        except Exception as ex:
            result = None
            print(ex)
        finally:
            if result is not None:
                dp.tickets.append(result)
                #await message.reply(f"Задача номер {result['ticket_id']} успешно добавлена")
                return SendMessage(-1001635770778, f"Задача номер {result['ticket_id']} успешно добавлена")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_input, state="*")
    dp.register_message_handler(user_photo, content_types=ContentType.PHOTO)
    dp.register_message_handler(user_q1_state_input, state=Ticket.Q1)