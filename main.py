import asyncio
from aiogram import Bot, Dispatcher, types, executor
import aiogram.utils.exceptions

# Logging
import logging
logging.basicConfig(level=logging.INFO)

# Environment variables
from dotenv import load_dotenv
from os import getenv
from hashlib import sha256
load_dotenv()

# Load token from .env file
BOT_TOKEN: str = getenv("TELEGRAM_BOT_PRIVATE_KEY")
token_sha = sha256(BOT_TOKEN.encode()).hexdigest()
logging.info(f"Token SHA256: {token_sha[:16]}...{token_sha[-16:]}")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

@dp.message_handler()
async def echo(message: types.Message):
    # Return the same message. If there are contents,
    # then return the contents of the message.
    if message.text:
        await message.answer(message.text)
    else:
        await message.answer("I can't echo this")

if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except aiogram.utils.exceptions.TelegramAPIError as e:
        logging.error(e)