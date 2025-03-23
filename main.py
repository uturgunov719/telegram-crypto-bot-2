import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz

# 🔐 Твой токен и chat_id
BOT_TOKEN = "7957818763:AAFLm17sgZvZPjLJkCHfgzixlaRCYqITIUQ"
CHAT_ID = 969035847
TZ_MOSCOW = pytz.timezone("Europe/Moscow")

# Бот и диспетчер
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TZ_MOSCOW)

# Команда /start
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("👋 Привет! Бот работает.\n\n👉 Напиши /analyze, чтобы получить анализ по альткоинам!")

# Команда /analyze
@dp.message(Command("analyze"))
async def show_analysis_button(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Получить анализ топ-5 альтов", callback_data="get_analysis")]
    ])
    await message.answer("Нажми кнопку ниже, чтобы получить свежий анализ по рынку 👇", reply_markup=keyboard)

# Обработка кнопки
@dp.callback_query(lambda call: call.data == "get_analysis")
async def handle_analysis_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("🧠 Анализ запрашивается... Подключаюсь к рынку 📡")
    # Тут позже будет анализ как у профи

# Планировщик: ежедневная рассылка в 17:00
async def send_daily_analysis():
    now = datetime.now(TZ_MOSCOW).strftime("%Y-%m-%d %H:%M")
    fake_data = "📈 Топ-10 альткоинов сегодня:\n\n1. SOL +4.5%\n2. AVAX +3.1%\n3. LINK +2.8%\n..."
    await bot.send_message(chat_id=CHAT_ID, text=f"🕔 {now} МСК\n\n{fake_data}")

# Запуск
async def main():
    scheduler.add_job(send_daily_analysis, CronTrigger(hour=17, minute=0))
    scheduler.start()

    print("✅ Бот с кнопкой и планировщиком запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
