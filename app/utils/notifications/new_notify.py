from aiogram import Bot, html
from aiogram.types import User, Chat

from app.config import Config
from app.utils.broadcast import broadcast_smth, from_iterable


async def notify_new_user(user: User, bot: Bot) -> int:
    pics = await bot.get_user_profile_photos(user.id)
    txt = [
        "#new_user",
        f"Имя: {html.quote(user.full_name)}",
        f'id: <a href="tg://user?id={user.id}">{user.id}</a>',
        f"username: @{user.username}",
    ]
    photo = None
    if pics and pics.total_count > 0:
        photo = pics.photos[0][-1].file_id

    admins = from_iterable(Config.ADMINS)

    if photo:
        return await broadcast_smth(admins, bot.send_photo, False, photo=photo, caption='\n'.join(txt))
    return await broadcast_smth(admins, bot.send_message, False, text='\n'.join(txt))


async def notify_new_group(chat: Chat, bot: Bot) -> int:
    chat = await bot.get_chat(chat_id=chat.id)
    txt = [
        "#new_group",
        f"Full name: {html.quote(chat.first_name)}",
        f'id: {chat.id}',
        f"Title: {chat.title}",
        f"Description: {chat.description}",
        f"Members: {await bot.get_chat_member_count(chat.id)}",
        f"username: @{chat.username}",
    ]
    admins = from_iterable(Config.ADMINS)

    return await broadcast_smth(admins, bot.send_message, False, text='\n'.join(txt))
