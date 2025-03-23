import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz

BOT_TOKEN = "7957818763:AAFLm17sgZvZPjLJkCHfgzixlaRCYqITIUQ"
CHAT_ID = 969035847
TZ_MOSCOW = pytz.timezone("Europe/Moscow")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TZ_MOSCOW)

# Меню с кнопкой 📊 Анализ
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Анализ")],
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("👋 Привет! Я готов к работе.\nНажми кнопку ниже, чтобы получить анализ рынка!", reply_markup=main_menu)

# Обработка нажатия на кнопку "📊 Анализ"
@dp.message(lambda message: message.text == "📊 Анализ")
async def handle_analysis_request
