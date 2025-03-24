import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz
import requests
import matplotlib.pyplot as plt
import os

# 🔐 ВСТАВЛЕННЫЕ ДАННЫЕ
BOT_TOKEN = "7980459096:AAF-FST5zPLmyMwflq2H9mHpEI5kkpoAyJE"
CHAT_ID = 969035847
TZ_MOSCOW = pytz.timezone("Europe/Moscow")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TZ_MOSCOW)

main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📊 Анализ")],
             [KeyboardButton(text="💼 Портфель")],
             [KeyboardButton(text="📈 График")],
             [KeyboardButton(text="⬅️ Назад")]],
    resize_keyboard=True,
    input_field_placeholder="🔹 Нажми МЕНЮ 👇"
)

def interpret_rsi(rsi):
    if rsi < 30:
        return f"{rsi:.1f} — Перепродан → Возможен ЛОНГ"
    elif rsi < 50:
        return f"{rsi:.1f} — Слабость / флэт → Лучше подождать"
    elif rsi < 70:
        return f"{rsi:.1f} — Сила / рост → Возможен ЛОНГ"
    else:
        return f"{rsi:.1f} — Перекуплен → Возможен ШОРТ"

@dp.message(lambda msg: msg.text == "/start")
async def start_command(message: types.Message):
    await message.answer("👋 Привет! Я бот для анализа крипты.\n\n🔹Нажми кнопку МЕНЮ ниже 👇", reply_markup=main_menu)

@dp.message(lambda msg: msg.text == "📈 График")
async def handle_graph_button(message: types.Message):
    # Топ-10 монет + TON
    buttons = [
        [InlineKeyboardButton(text=symbol, callback_data=f"chart_{symbol.lower()}") for symbol in ["BTC", "ETH", "BNB"]],
        [InlineKeyboardButton(text=symbol, callback_data=f"chart_{symbol.lower()}") for symbol in ["SOL", "ADA", "XRP"]],
        [InlineKeyboardButton(text=symbol, callback_data=f"chart_{symbol.lower()}") for symbol in ["DOGE", "AVAX", "MATIC"]],
        [InlineKeyboardButton(text="DOT", callback_data="chart_dot"), InlineKeyboardButton(text="TON", callback_data="chart_ton")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выбери монету для графика:", reply_markup=markup)

if __name__ == "__main__":
    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    asyncio.run(main())
