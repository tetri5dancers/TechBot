from aiogram import Bot, F, Router
from aiogram.filters.command import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)

router = Router()


@router.message(Command(commands=["start"]))
async def command_start(message: Message, bot: Bot, base_url: str):
    pass


@router.message(Command(commands=["webview"]))
async def command_webview(message: Message, base_url: str):
    pass


@router.message(~F.message.via_bot)  # Echo to all messages except messages via bot
async def echo_all(message: Message, base_url: str):
    pass