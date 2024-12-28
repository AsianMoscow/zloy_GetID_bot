from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram import F
import asyncio
import logging
import os


API_TOKEN = os.getenv("zloy_GetID_bot__TOKEN")
if not API_TOKEN:
    raise ValueError("API token not set. Please define 'getId_bot_token' as an environment variable.")

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# Инициализация бота, маршрутизатора и диспетчера
bot = Bot(token=API_TOKEN)
router = Router()
dp = Dispatcher()


@router.message(F)
async def get_ids(message: Message):
    """
    Получение ID пользователя, чата или группы.
    Ответит информацией, если ему переслать сообщение.
    """
    user_id = message.from_user.id
    username = message.from_user.username or "(нет имени пользователя)"
    first_name = message.from_user.first_name or "(нет имени)"
    last_name = message.from_user.last_name or "(нет фамилии)"
    is_bot = message.from_user.is_bot

    chat_id = message.chat.id
    chat_type = message.chat.type
    chat_title = message.chat.title or "(нет названия)"
    chat_username = message.chat.username or "(нет username)"

    forward_info = "(Пересланное сообщение отсутствует или не содержит дополнительной информации.)"

    if message.forward_from:
        forward_user_id = message.forward_from.id
        forward_username = message.forward_from.username or "(нет имени пользователя)"
        forward_first_name = message.forward_from.first_name or "(нет имени)"
        forward_last_name = message.forward_from.last_name or "(нет фамилии)"
        forward_is_bot = message.forward_from.is_bot
        forward_info = (
            f"👤 Информация о пересланном пользователе:\n"
            f"  - ID: {forward_user_id}\n"
            f"  - Имя: {forward_first_name}\n"
            f"  - Фамилия: {forward_last_name}\n"
            f"  - Имя пользователя: {forward_username}\n"
            f"  - Бот: {'Да' if forward_is_bot else 'Нет'}\n"
        )
    elif message.forward_from_chat:
        forward_chat_id = message.forward_from_chat.id
        forward_chat_title = message.forward_from_chat.title or "(нет названия)"
        forward_chat_username = message.forward_from_chat.username or "(нет username)"
        forward_chat_type = message.forward_from_chat.type
        forward_info = (
            f"💾 Информация о пересланном чате:\n"
            f"  - ID: {forward_chat_id}\n"
            f"  - Название: {forward_chat_title}\n"
            f"  - Имя пользователя: {forward_chat_username}\n"
            f"  - Тип: {forward_chat_type}\n"
        )

    response_text = (
        f"👤 Информация о пользователе:\n"
        f"  - ID: {user_id}\n"
        f"  - Имя: {first_name}\n"
        f"  - Фамилия: {last_name}\n"
        f"  - Имя пользователя: {username}\n"
        f"  - Бот: {'Да' if is_bot else 'Нет'}\n\n"
        f"💬 Информация о чате:\n"
        f"  - ID: {chat_id}\n"
        f"  - Тип: {chat_type}\n"
        f"  - Название: {chat_title}\n"
        f"  - Имя пользователя чата: {chat_username}\n\n"
        f"{forward_info}"
    )

    logger.info(
        f"Processed message: User ID: {user_id}, Username: {username}, Chat ID: {chat_id}, Chat Type: {chat_type}, Title: {chat_title}"
    )
    await message.reply(response_text)


async def main():
    # Регистрация обработчиков
    dp.include_router(router)
    # Запуск бота
    logger.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
