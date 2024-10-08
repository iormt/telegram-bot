from telegram.ext import CallbackContext

class BotInvoker:
    def __init__(self):
        self.commands = {}

    def register(self, command_name, command) -> None:
        self.commands[command_name] = command

    async def execute(self, command_name, update, context: CallbackContext) -> None:
        print(f'command name: {command_name} is in commands: {command_name in self.commands}')
        if command_name in self.commands:
            await self.commands[command_name].execute(update, context)
        else:
            context.bot_data['free_message'] = command_name
            await self.commands['default'].execute(update, context)