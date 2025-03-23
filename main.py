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
        [KeyboardButton(text="💼 Портфель")],
        [KeyboardButton(text="📈 График")],
        [KeyboardButton(text="🔙 Назад")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери раздел 👇"
)

# 👉 /start
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот для анализа крипты.\n\nНажми кнопку МЕНЮ ниже 👇",
        reply_markup=main_menu
    )

# 👉 Нажал "📂 МЕНЮ" — откроем подменю
@dp.message(lambda msg: msg.text == "📂 МЕНЮ")
async def open_submenu(message: types.Message):
    await message.answer("📂 Выбери раздел ниже:", reply_markup=submenu)

# 👉 Нажал "🔙 Назад" — возвращаемся в главное меню
@dp.message(lambda msg: msg.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("⬅️ Возвращаемся в главное меню", reply_markup=main_menu)

# 👉 Анализ
@dp.message(lambda msg: msg.text == "📊 Анализ")
async def analysis(message: types.Message):
    await message.answer("🧠 Запрашиваю анализ по топ-альтам... (вставим позже)")

# 👉 Портфель
@dp.message(lambda msg: msg.text == "💼 Портфель")
async def portfolio(message: types.Message):
    await message.answer("💼 Здесь будет отображаться твой крипто-портфель")

# 👉 График
@dp.message(lambda msg: msg.text == "📈 График")
async def chart(message: types.Message):
    await message.answer("📈 Вот прогноз: рынок может пойти вверх после коррекции")

# 🕔 Планировщик (анализ каждый день в 17:00)
async def send_daily_analysis():
    now = datetime.now(TZ_MOSCOW).strftime("%Y-%m-%d %H:%M")
    fake_data = "📈 Топ-10 альткоинов сегодня:\n\n1. SOL +4.5%\n2. AVAX +3.1%\n3. LINK +2.8%\n..."
    await bot.send_message(chat_id=CHAT_ID, text=f"🕔 {now} МСК\n\n{fake_data}")

# 🚀 Запуск
async def main():
    scheduler.add_job(send_daily_analysis, CronTrigger(hour=17, minute=0))
    scheduler.start()
    print("✅ Бот с МЕНЮ и подменю запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
