import logging
from aiogram import Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from Dispatcher import BotDispatcher
from aiogram.utils.executor import start_webhook
from config import tg_bot_token, load_config

from filters.admin import AdminFilter
from handlers.admin import register_admin
from handlers.echo import register_echo
from handlers.user import register_user
from middleware.db import ProcessMessage
from utils.OneSConnector import OnesDB
from aiohttp.web import run_app
from aiohttp.web_app import Application
#from handlers import router
#from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import MenuButtonWebApp, WebAppInfo


API_TOKEN = tg_bot_token
WEBHOOK_HOST = 'https://ticket.skk-znanie.com'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '192.168.0.252'  # or ip
WEBAPP_PORT = 8081

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = BotDispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


def register_all_middlewares(dp):
    dp.setup_middleware(ProcessMessage())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)

    #register_echo(dp)


async def on_startup(dp):
    config = load_config(".env")
    bot['config'] = config

    connector = OnesDB(config.oneSParams.base_url)
    await connector.get_init_data()
    config.tg_bot.admin_ids = connector.init_data["admins"]
    bot['config'] = config

    dp.intents = connector.init_data["intents"]
    dp.model_train()
    await dp.get_tickets()

    #dp.include_router(router)
    #app = Application()
    #app["bot"] = bot

    #app.router.add_get("/app", demo_handler)

    register_all_filters(dp)
    register_all_handlers(dp)
    register_all_middlewares(dp)
    await bot.set_webhook(WEBHOOK_URL)
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="APP", web_app=WebAppInfo(url=f"{WEBHOOK_HOST}/app"))
    )


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
