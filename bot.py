import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

ADMIN_CHANNEL = -1001234567890   # заменим позже на твой канал


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Здравствуйте! 👋\n"
        "Это бот сервиса *USABOX Delivery*.\n\n"
        "Мы доставляем товары из США во все страны мира (кроме РФ).\n\n"
        "Чтобы сделать заказ, отправьте ссылку на товар Amazon/eBay/Walmart/BestBuy\n"
        "и укажите страну доставки. 🎁✈️"
    )


@dp.message()
async def forward_message(message: types.Message):
    text = message.text

    await bot.send_message(
        ADMIN_CHANNEL,
        f"📦 Новая заявка:\n"
        f"От: {message.from_user.first_name}\n"
        f"Юзернейм: @{message.from_user.username}\n\n"
        f"Сообщение:\n{text}"
    )

    await message.answer(
        "Спасибо! Ваша заявка принята.\n"
        "Мы свяжемся с вами в ближайшее время."
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
