from aiogram.dispatcher import Dispatcher
from utils.model import MLPModel
from utils.OneSConnector import OnesDB


class BotDispatcher(Dispatcher):
    def __init__(self, bot):
        super().__init__(bot)
        self.intents = None
        self.model = MLPModel(intents=self.intents)
        self.tickets = list

    def ml_process(self, text):
        return self.model.process(text)

    def model_train(self):
        self.model = MLPModel(self.intents)

    def get_intent(self, text):
        return self.model.get_intent_ml(text)

    async def get_tickets(self):
        connector = OnesDB(baseUrl=self.bot.data['config'].oneSParams.base_url)
        self.tickets = await connector.get_tasks()
