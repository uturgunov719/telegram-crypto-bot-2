import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz

# Твой токен и ID
BOT_TOKEN = "7957818763:AAFLm17sgZvZPjLJkCHfgzixlaRCYqITIUQ"
CHAT_ID = 969035847
TZ_MOSCOW = pytz.timezone("Europe/Moscow")

# Инициализация
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TZ_MOSCOW)

# Установка команды в "Меню бота" (☰)
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="analyze", description="📊 Получить анализ альткоинов"),
    ]
    await bot.set_my_commands(commands)

# /start показывает приветствие
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот для анализа альткоинов.\n\nНажми <b>☰ Меню</b> и выбери <b>📊 Анализ</b>, чтобы получить свежую информацию!",
    )

# /analyze — команда из меню
@dp.message(Command("analyze"))
async def analyze_command(message: types.Message):
    await message.answer("🧠 Анализ запрашивается... Подключаюсь к рынку 📡")
    # Здесь позже вставим теханализ

# Планировщик: рассылка в 17:00
async def send_daily_analysis():
    now = datetime.now(TZ_MOSCOW).strftime("%Y-%m-%d %H:%M")
    fake_data = "📈 Топ-10 альткоинов сегодня:\n\n1. SOL +4.5%\n2. AVAX +3.1%\n3. LINK +2.8%\n..."
    await bot.send_message(chat_id=CHAT_ID, text=f"🕔 {now} МСК\n\n{fake_data}")

# Запуск
async def main():
    scheduler.add_job(send_daily_analysis, CronTrigger(hour=17, minute=0))
    scheduler.start()

    await set_bot_commands(bot)  # Установим меню
    print("✅ Бот с меню и планировщиком запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
