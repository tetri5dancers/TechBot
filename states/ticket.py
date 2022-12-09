from aiogram.dispatcher.filters.state import StatesGroup, State


class Ticket(StatesGroup):
    Q1 = State()
    Q2 = State()