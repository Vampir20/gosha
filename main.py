from aiogram import Bot, Dispatcher
from aiogram.utils import executor

TOKEN = '5469448316:AAGnQ2VU3l2RecqkWF6EpHtxJgUqqMe5uY8'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

