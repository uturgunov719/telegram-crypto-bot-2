import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz

# 🔐 Токен и chat_id
BOT_TOKEN = "7957818763:AAFLm17sgZvZPjLJkCHfgzixlaRCYqITIUQ"
CHAT_ID = 969035847
TZ_MOSCOW = pytz.timezone("Europe/Moscow")

# Инициализация
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TZ_MOSCOW)

# Главное меню — одна кнопка "📂 МЕНЮ"
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📂 МЕНЮ")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажми МЕНЮ 👇"
)

# Подменю — три кнопки
submenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Анализ")],
        [KeyboardButton(text="💼
