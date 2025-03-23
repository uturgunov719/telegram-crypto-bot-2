import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

# Токен твоего бота (замени на свой токен)
API_TOKEN = '7957818763:AAFLm17sgZvZPjLJkCHfgzixlaRCYqITIUQ'

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Привет, мой кожаный друг! Твой chat_id: {chat_id}")
    logging.info(f"Пользователь {chat_id} написал боту")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
