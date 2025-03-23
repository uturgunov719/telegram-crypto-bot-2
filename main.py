from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

bot = Bot(token="7957818763:AAFLm17sgZvZPjLJkCHfgzixlaRCYqITIUQ", parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Нажми /analyze для анализа.")

@dp.message(Command("analyze"))
async def analyze_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Получить анализ", callback_data="analyze")]
        ]
    )
    await message.answer("Выбери опцию:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "analyze")
async def handle_callback(callback: types.CallbackQuery):
    await callback.message.answer("📡 Анализ подключается...")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
