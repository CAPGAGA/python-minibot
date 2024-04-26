from bot import Bot
from handlers import MessageHandler, CommandHandler
import asyncio

async def say_hello(chat_id):
    print(await bot.get_updates())
    await bot.send_message(chat_id, 'Hello! How are you?')
    await bot.send_message(chat_id, "I'm minibot")


if __name__ == "__main__":
    token = '6441274875:AAFVanHERYQwzMW51zYWJWpKlEV7n1wyOyw'
    bot = Bot(token)
    bot.add_handler(CommandHandler(callback='hello'))
    bot.add_handler(MessageHandler(action=say_hello, callback='hello'))
    asyncio.run(bot.run())