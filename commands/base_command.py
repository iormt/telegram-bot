from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import CallbackContext


class Command(ABC):
    @abstractmethod
    async def execute(self, update: Update, context: CallbackContext) -> None:
        pass






