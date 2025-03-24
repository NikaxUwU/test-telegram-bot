import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, Update
from fastapi import FastAPI
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
WEBHOOK_URL = config.WEBHOOK_URL
app = FastAPI()

@dp.message(lambda message: message.text == "/start")
async def send_welcome(message: Message):
    await message.answer("Прив!")

@dp.message(lambda message: message.text == "/info")
async def send_info(message: Message):
    await message.answer("Я гей")

@dp.message(lambda message: message.text.startswith("/greet"))
async  def send_welcome_with_name(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        await  message.answer(f"Привет, {parts[1]}")
    else:
        await message.answer("Привет, незнакомец")

async def main():
    await dp.start_polling(bot)

@app.post("/webhook")
async def webhook(update: dict):
    telegram_update = Update(**update)
    await dp.feed_update(bot, telegram_update)

async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown():
    await bot.delete_webhook()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    asyncio.run(main())