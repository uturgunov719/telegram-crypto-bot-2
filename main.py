import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import openai
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токены и настройки из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TZ_MOSCOW = pytz.timezone("Europe/Moscow")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TZ_MOSCOW)
openai.api_key = OPENAI_API_KEY

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
            [InlineKeyboardButton(text="BTC", callback_data="analyze_BTC"), InlineKeyboardButton(text="ETH", callback_data="analyze_ETH")],
            [InlineKeyboardButton(text="BNB", callback_data="analyze_BNB"), InlineKeyboardButton(text="ADA", callback_data="analyze_ADA")],
            [InlineKeyboardButton(text="SOL", callback_data="analyze_SOL"), InlineKeyboardButton(text="AVAX", callback_data="analyze_AVAX")],
            [InlineKeyboardButton(text="LINK", callback_data="analyze_LINK"), InlineKeyboardButton(text="MATIC", callback_data="analyze_MATIC")],
            [InlineKeyboardButton(text="ARB", callback_data="analyze_ARB"), InlineKeyboardButton(text="XRP", callback_data="analyze_XRP")]
        ]
    )
    await message.answer("💡 Выбери монету для анализа:", reply_markup=keyboard)

# Обработка выбора монеты и запрос в GPT
@dp.callback_query(lambda c: c.data.startswith("analyze_"))
async def handle_coin_analysis(callback: types.CallbackQuery):
    coin = callback.data.split("_")[1]
    await callback.answer()
    await callback.message.answer(f"🧠 Запрашиваю анализ по <b>{coin}</b>...", parse_mode=ParseMode.HTML)

    prompt = f"Представь, что ты трейдер. Дай технический анализ по {coin}/USDT. Укажи текущую точку входа, тренд, RSI, уровни поддержки/сопротивления и скажи, лонг или шорт. Кратко, как профи."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ Ошибка при запросе к GPT: {e}"

    await callback.message.answer(reply)

# Портфель
@dp.message(lambda msg: msg.text == "\ud83d\udcbc \u041f\u043e\u0440\u0442\u0444\u0435\u043b\u044c")
async def portfolio(message: types.Message):
    await message.answer("💼 Здесь будет отображаться твой крипто-портфель. В будущем сюда можно добавить отслеживание активов.")

# График с прогнозом
@dp.message(lambda msg: msg.text == "\ud83d\udcc8 \u0413\u0440\u0430\u0444\u0438\u043a")
async def chart(message: types.Message):
    prices = [28000, 28200, 28100, 28500, 28900, 29100, 28800, 29200, 29400, 29500]
    timestamps = list(range(len(prices)))
    plt.figure(figsize=(8, 4))
    plt.plot(timestamps, prices, marker='o')
    plt.title("BTC/USDT: движение цены")
    plt.xlabel("Время")
    plt.ylabel("Цена, $")
    plt.grid(True)
    plt.tight_layout()
    filepath = "btc_chart.png"
    plt.savefig(filepath)
    plt.close()

    photo = FSInputFile(filepath)
    await message.answer_photo(photo=photo, caption="📈 Пример графика BTC. Прогноз: возможен рост после закрепления выше $29,500")
    os.remove(filepath)

# Ежедневная рассылка
async def send_daily_analysis():
    now = datetime.now(TZ_MOSCOW).strftime("%Y-%m-%d %H:%M")
    prompt = "Дай краткий технический обзор по 3 топ-альткоинам на сегодня. Укажи краткие точки входа и рекомендации."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content
    except Exception as e:
        text = f"❌ Ошибка при получении анализа: {e}"
    await bot.send_message(chat_id=CHAT_ID, text=f"🕔 {now} МСК\n\n{text}")

# Запуск
async def main():
    scheduler.add_job(send_daily_analysis, CronTrigger(hour=17, minute=0))
    scheduler.start()
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
