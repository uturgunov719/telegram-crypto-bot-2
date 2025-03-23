import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import requests
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токены и настройки из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
TZ_MOSCOW = pytz.timezone("Europe/Moscow")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TZ_MOSCOW)

# Главное меню с кнопкой "МЕНЮ"
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="\ud83d\udcc2 \u041c\u0415\u041d\u042e")],
    ],
    resize_keyboard=True,
    input_field_placeholder="\u041d\u0430\u0436\u043c\u0438 \u041c\u0415\u041d\u042e \ud83d\udc47"
)

# Подменю с кнопками: Анализ, Портфель, График
submenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="\ud83d\udcca \u0410\u043d\u0430\u043b\u0438\u0437")],
        [KeyboardButton(text="\ud83d\udcbc \u041f\u043e\u0440\u0442\u0444\u0435\u043b\u044c")],
        [KeyboardButton(text="\ud83d\udcc8 \u0413\u0440\u0430\u0444\u0438\u043a")],
        [KeyboardButton(text="\ud83d\udd19 \u041d\u0430\u0437\u0430\u0434")],
    ],
    resize_keyboard=True,
    input_field_placeholder="\u0412\u044b\u0431\u0435\u0440\u0438 \u0440\u0430\u0437\u0434\u0435\u043b \ud83d\udc47"
)

# /start
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        "\ud83d\udc4b \u041f\u0440\u0438\u0432\u0435\u0442! \u042f \u0431\u043e\u0442 \u0434\u043b\u044f \u0430\u043d\u0430\u043b\u0438\u0437\u0430 \u043a\u0440\u0438\u043f\u0442\u044b.\n\n\u041d\u0430\u0436\u043c\u0438 \u043a\u043d\u043e\u043f\u043a\u0443 \u041c\u0415\u041d\u042e \u043d\u0438\u0436\u0435 \ud83d\udc47",
        reply_markup=main_menu
    )

# Нажал "МЕНЮ"
@dp.message(lambda msg: msg.text == "\ud83d\udcc2 \u041c\u0415\u041d\u042e")
async def open_submenu(message: types.Message):
    await message.answer("\ud83d\udcc2 \u0412\u044b\u0431\u0435\u0440\u0438 \u0440\u0430\u0437\u0434\u0435\u043b:", reply_markup=submenu)

# Назад
@dp.message(lambda msg: msg.text == "\ud83d\udd19 \u041d\u0430\u0437\u0430\u0434")
async def go_back(message: types.Message):
    await message.answer("⬅️ Возвращаемся в главное меню", reply_markup=main_menu)

# Анализ с топ-10 монетами
@dp.message(lambda msg: msg.text == "\ud83d\udcca \u0410\u043d\u0430\u043b\u0438\u0437")
async def analysis_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="BTC", callback_data="analyze_bitcoin"), InlineKeyboardButton(text="ETH", callback_data="analyze_ethereum")],
            [InlineKeyboardButton(text="BNB", callback_data="analyze_binancecoin"), InlineKeyboardButton(text="ADA", callback_data="analyze_cardano")],
            [InlineKeyboardButton(text="SOL", callback_data="analyze_solana"), InlineKeyboardButton(text="AVAX", callback_data="analyze_avalanche-2")],
            [InlineKeyboardButton(text="LINK", callback_data="analyze_chainlink"), InlineKeyboardButton(text="MATIC", callback_data="analyze_polygon")],
            [InlineKeyboardButton(text="ARB", callback_data="analyze_arbitrum"), InlineKeyboardButton(text="XRP", callback_data="analyze_ripple")]
        ]
    )
    await message.answer("💡 Выбери монету для анализа:", reply_markup=keyboard)

# Обработка выбора монеты и прогноз на основе CoinGecko
@dp.callback_query(lambda c: c.data.startswith("analyze_"))
async def handle_coin_analysis(callback: types.CallbackQuery):
    coin_id = callback.data.split("_")[1]
    await callback.answer()
    await callback.message.answer(f"🔍 Получаю данные по <b>{coin_id.upper()}</b>...", parse_mode=ParseMode.HTML)

    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        res = requests.get(url, params={"localization": "false", "tickers": "false", "market_data": "true"})
        data = res.json()
        price = data['market_data']['current_price']['usd']
        change = data['market_data']['price_change_percentage_24h']

        trend = "📉 Рынок падает — рекомендуется ШОРТ" if change < -2 else "📈 Рынок растёт — можно входить в ЛОНГ" if change > 2 else "🤔 Рынок во флэте — жди подтверждения"

        reply = (
            f"<b>{data['name']} ({data['symbol'].upper()})</b>\n"
            f"💰 Цена: ${price:.2f}\n"
            f"📊 Изменение за 24ч: {change:.2f}%\n"
            f"\n<b>{trend}</b>"
        )
    except Exception as e:
        reply = f"❌ Не удалось получить данные: {e}"

    await callback.message.answer(reply, parse_mode=ParseMode.HTML)

# Остальные функции (портфель, график и т.д.) можно обновить позже

# Запуск
async def main():
    scheduler.start()
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
