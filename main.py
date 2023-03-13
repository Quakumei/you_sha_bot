# Telgram bot api
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

# + Config --------------+
BOT_TOKEN: str = getenv("TELEGRAM_BOT_PRIVATE_KEY")
TORCH_SUPPORT: bool = getenv("TORCH_SUPPORT") == 'True'
HELP_FILE: str = 'bot_texts/help.txt'
BOT_NAMES_FILE: str = 'bot_texts/bot_names.txt'
# +----------------------+

# Models
from models.echo import generate_answer as generate_echo
if TORCH_SUPPORT:
    from models.rubert_tiny2_russian_emotion_detection import generate_answer as generate_emotions


def load_list(file:str) -> list[str]:
    with open(file, encoding="utf8") as f:
        result = [l.strip() for l in f.readlines()]
    return result

def load_string_banner(file:str) -> list[str]:
    with open(file, encoding="utf8") as f:
        result = ''.join(f.readlines())
    return result


# Load token from .env file
token_sha = sha256(BOT_TOKEN.encode()).hexdigest()
logging.info(f"Token SHA256: {token_sha[:16]}...{token_sha[-16:]}")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Load strings
help_message : str   = load_string_banner(HELP_FILE)
bot_names : set[str] = set(load_list(BOT_NAMES_FILE))


def strip_command(text:str) -> str:
    """
        Убирает /команду из строки
    """
    text_split = text.split(' ')
    if len(text_split) == 1:
        return ''
    return ' '.join(text.split(' ')[1:])


# /start
# /help
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(help_message)

# /emotions
if TORCH_SUPPORT:
    @dp.message_handler(commands=['emotions'])
    async def emotions(message: types.Message):
        text_arg = generate_echo(strip_command(message.text))
        if text_arg:
            await message.answer(generate_emotions(strip_command(message.text)))
        else:
            await message.answer("/emotions [text], пожалуйста.")


# /echo
@dp.message_handler(commands=['echo'])
async def echo(message: types.Message):
    text_arg = generate_echo(strip_command(message.text))
    if text_arg:
        await message.answer(text_arg)
    else:
        await message.answer("/echo [text], пожалуйста.")


# Ответить, если кто-то упомянул бота
@dp.message_handler()
async def callout(message: types.Message):
    text : str = message.text
    cleaned_words : set[str] = set(text.lower().split(' '))
    if len(cleaned_words.intersection(bot_names)):
        await message.answer('Дада, это я!')
    else:
        pass

if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except aiogram.utils.exceptions.TelegramAPIError as e:
        logging.error(e)