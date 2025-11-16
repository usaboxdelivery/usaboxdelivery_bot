import logging
from aiogram import Bot, Dispatcher, executor, types

# ===== НАСТРОЙКИ =====
API_TOKEN = "8390554462:AAG23e2ydef4wMq4fO8PJ1BcMw846MpS3Uk"

# ID приватного канала для заявок.
# Пока оставляем как есть, позже заменим на реальный ID, например -1001234567890.
ADMIN_CHANNEL = -1001234567890

# ===== НАСТРОЙКА ЛОГГИРОВАНИЯ =====
logging.basicConfig(level=logging.INFO)

# ===== СОЗДАЁМ БОТА И ДИСПЕТЧЕР =====
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# ===== ОБРАБОТЧИК КОМАНДЫ /start =====
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    text = (
        "Здравствуйте! 👋\n"
        "Это бот сервиса USABOX Delivery.\n\n"
        "Мы доставляем товары из США во многие страны (кроме РФ).\n\n"
        "Чтобы сделать заказ, отправьте ссылку на товар "
        "Amazon / eBay / Walmart / BestBuy и укажите страну и город доставки.\n\n"
        "Пример:\n"
        "https://www.amazon.com/....\n"
        "Страна: Грузия, город Тбилиси."
    )
    await message.answer(text)


# ===== ОБРАБОТЧИК ЛЮБЫХ СООБЩЕНИЙ (ЗАЯВКИ) =====
@dp.message_handler()
async def handle_message(message: types.Message):
    user = message.from_user
    text = message.text if message.text else "(без текста)"

    # Формируем текст заявки для вашего приватного канала
    order_text = (
        "📦 <b>Новая заявка</b>\n\n"
        f"Имя: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username or 'нет'}\n"
        f"User ID: <code>{user.id}</code>\n\n"
        f"Сообщение:\n{text}"
    )

    # Пытаемся отправить заявку в приватный канал (если ID будет корректен)
    try:
        await bot.send_message(ADMIN_CHANNEL, order_text, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Не удалось отправить заявку в канал: {e}")

    # Отвечаем пользователю
    await message.answer(
        "Спасибо! Ваша заявка принята.\n"
        "Мы свяжемся с вами в ближайшее время."
    )


# ===== ТОЧКА ВХОДА =====
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
