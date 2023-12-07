from aiogram import Bot, Dispatcher, executor
from aiogram.types import *

from mini_bot_db import create_table, add_users, check_user, add_message, get_user_id

import psycopg2
from os import system
system("clear")

connection = psycopg2.connect(
    host = "localhost",
    database = "mini_bot",
    user = "yeraly",
    password = "123",
    port = "5432"
)

bot = Bot(token="6239692911:AAF8Ue3tvAXCdOwyCs2aQymgNgsw1R8h268", 
    parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=["repost"])
async def repost(message: Message):
    if message.text.split()[-1].startswith("http"):
        link = message.text.split()[-1]
        gp_link = f"\n<a href='{link}'>Подробнее</a>"
        text = message.text[message.text.find(" ")+1:].rstrip(link) + gp_link
    else:
        text = message.text[message.text.find(" ")+1:]

    if message.from_user.id == 1310237124:
        for user_id in get_user_id(connection):
            await bot.send_message(user_id, text)
    else:
        await message.answer("У вас недостаточно полномочии для этой команды")

@dp.message_handler(commands=["start"])
async def start(message: Message):
    create_table(connection)
    user_user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username
    user_is_bot = message.from_user.is_bot
    user_language_code = message.from_user.language_code
    user_is_premium = message.from_user.is_premium
    
    if check_user(connection, user_user_id) is None:
        add_users(connection, user_user_id, user_first_name,
        user_last_name, user_username, user_is_bot,
        user_language_code, user_is_premium)
    else:
        pass
    
    await message.answer("Привет я бот который ничего не делает")

@dp.message_handler(content_types=ContentTypes.TEXT)
async def msg(message: Message):
    user_user_id = message.from_user.id
    user_user_text = message.text
    add_message(connection, user_user_id, user_user_text)

    await message.answer(message.text)

if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    except(KeyboardInterrupt, SystemExit):
        pass


# connection.commit()
# cursor.close()
# connection.close()