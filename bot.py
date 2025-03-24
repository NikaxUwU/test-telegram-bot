import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
print(config.WEBHOOK_URL)

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

if __name__ == "__main__":
    asyncio.run(main())