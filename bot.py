import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, Update
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

WEBHOOK_URL = config.WEBHOOK_URL
app = FastAPI()

@dp.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer("Привет!")

@dp.message(F.text == "/info")
async def send_info(message: Message):
    await message.answer("Я Telegram-бот!")

@dp.message(F.text.startswith("/greet"))
async def send_welcome_with_name(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        await message.answer(f"Привет, {parts[1]}!")
    else:
        await message.answer("Привет, незнакомец!")

@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    telegram_update = Update(**update)
    await dp.feed_update(bot, telegram_update)

async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown():
    await bot.delete_webhook()

if __name__ == "__main__":
    import uvicorn

    asyncio.run(on_startup())
    uvicorn.run(app, host="0.0.0.0", port=8000)
