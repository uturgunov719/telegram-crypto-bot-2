import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

# 🔐 Токен от BotFather
BOT_TOKEN = "7957818763:AAFLm17sgZvZPjLJkCHfgzixlaRCYqITIUQ"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer("Привет! 👋 Я живой и работаю на Aiogram 3.x!")

# Главная асинхронная функция
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
