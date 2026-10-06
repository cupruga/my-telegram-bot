import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

TOKEN = "8825665309:AAFkruH4b_u7__ismdoHlJMEgcwQUyUo8rg"
ADMINS_LIST = [7803999857, 6533423791, 7816067688]

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет! 🕊️\nСначала скрин, потом ваша анкета. нет скрина - нет анкеты."
    )

@dp.message()
async def forward_to_admins(message: Message):
    if message.from_user.id not in ADMINS_LIST:
        for admin_id in ADMINS_LIST:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"📩 Новая анкета от @{message.from_user.username} (ID: {message.from_user.id}):"
                )
                await message.forward(chat_id=admin_id)
            except Exception:
                continue
        await message.answer("Ваше сообщение успешно отправлено!")
        
    elif message.reply_to_message and message.reply_to_message.forward_from:
        user_id = message.reply_to_message.forward_from.id
        try:
            await bot.send_message(chat_id=user_id, text=message.text)
            await message.answer("Ответ отправлен пользователю!")
        except Exception:
            await message.answer("Не удалось отправить ответ.")

async def main():
    print("Бот успешно запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
