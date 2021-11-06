import logging

from aiogram import types, Bot
from aiogram.utils.markdown import quote_html

from app.config import Config


async def notify_new_user(user: types.User) -> None:
    bot = Bot.get_current()
    user = await bot.get_chat(chat_id=user.id)
    pics = await bot.get_user_profile_photos(user.id)
    txt = [
        "#new_user",
        f"Имя: {quote_html(user.full_name)}",
        f'id: <a href="tg://user?id={user.id}">{user.id}</a>',
        f"username: @{user.username}",
    ]
    try:
        photo = pics.photos[0][-1].file_id
    except Exception as e:
        logging.error(e)
        photo = ''
    for admin in Config.ADMINS:
        if photo:
            await bot.send_photo(admin, photo=photo, caption=('\n'.join(txt)))
        else:
            await bot.send_message(admin, '\n'.join(txt))
