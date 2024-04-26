import asyncio
import aiohttp
import json
from handlers import BaseHandler


class Bot:

    def __init__(self, token):
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{token}/'
        self.offset = None
        self.handlers = BaseHandler()

    async def __build(self):
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

    async def __send_request(self, method, data):
        async with self.session.post(self.base_url + method, data=data) as response:
            return await response.text()

    async def get_updates(self):
        response = await self.__send_request('getUpdates', {'offset': self.offset, 'timeout': 30})
        return json.loads(response)

    async def start_polling(self):
        while True:
            updates = await self.get_updates()
            if 'result' in updates and updates['result']:
                for update in updates['result']:
                    await self.handlers.handle_update(update)
                    self.offset = update['update_id'] + 1
            else:
                await asyncio.sleep(1)

    async def send_message(self, chat_id, text):
        response = await self.__send_request(f'sendMessage?chat_id={chat_id}&text={text}', {chat_id: chat_id, 'text': text})
        response_json = json.loads(response)
        if not response_json['ok']:
            print(f'Error responding: {response_json["description"]}')

    def add_handler(self, handler):
        handler.send_message = self.send_message
        self.handlers.add_handler(handler)

    async def run(self):
        await self.__build()
        await self.start_polling()



