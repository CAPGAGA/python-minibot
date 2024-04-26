from typing import Union, Callable
import asyncio

class BaseHandler:

    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    async def handle_update(self, update):
        if 'message' in update:
            message = update['message']
            for handler in self.handlers:
                if handler.can_handle(message):
                    await handler.handle_message(message)
                    break
                else:
                    continue


class MessageHandler:

    def __init__(self, action: Callable, filters=None, callback: Union[str, None] = None):
        self.filters = filters
        self.callback = callback
        self.action = action

    def can_handle(self, message):
        return 'text' in message and message['text'] == self.callback

    async def handle_message(self, message):
        chat_id = message['chat']['id']
        await self.action(chat_id)


class CommandHandler:

    def __init__(self, callback: Union[str, None] = None):
        self.callback = callback

    def can_handle(self, message):
        return 'text' in message and message['text'].startswith('/') and self.callback in message['text']

    async def handle_message(self, message):
        text = message['text']
        chat_id = message['chat']['id']

        await self.send_message(chat_id, f'This is command')