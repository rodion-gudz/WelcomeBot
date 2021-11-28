from random import choice

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from WelcomeBot import bot_username, admin_id
from WelcomeBot.utils import db


@Client.on_message(filters.new_chat_members &
                   filters.create(lambda _, bot, m:
                                  bot.get_me().id
                                  in [u.id for u in m.new_chat_members]))
async def add_chat(client, message):
    await db.add_chat(str(message.chat.id))


@Client.on_message(filters.command("test_welcome") | filters.new_chat_members)
async def test(client, message):
    perm = await client.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if (
            not perm.can_manage_chat
            and not perm.can_change_info
            and message.from_user.id != admin_id
            and message.command == ["test_welcome"]
    ):
        await message.reply("**You don't have permission to use this command!**")
        return
    chat_gifs = await db.get_chat_gifs(str(message.chat.id))
    text = await db.get_chat_text(str(message.chat.id))
    if len(chat_gifs) == 0:
        await message.reply_text(text)
        return
    await client.send_cached_media(
        chat_id=message.chat.id,
        reply_to_message_id=message.message_id,
        file_id=choice(chat_gifs),
        caption=text)


@Client.on_message(filters.command(["list", f"list@{bot_username}"]))
async def list(client, message):
    if message.chat.type == 'private':
        await message.reply_text("**Please use this command in a group!**")
        return
    perm = await client.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if (
        not perm.can_manage_chat
        and not perm.can_change_info
        and message.from_user.id != admin_id
    ):
        await message.reply("**You don't have permission to use this command!**")
        return
    await message.reply_text(
        "**Список GIF**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                "Показать список",
                url=f"https://t.me/{bot_username}?start={message.chat.id}")]]
        )
    )


@Client.on_message(filters.command("start"))
async def start(client, message):
    if len(message.command) != 2:
        await message.reply_text(f"**Welcome, {message.from_user.mention}**")
        return
    chat_gifs = await db.get_chat_gifs(str(message.command[1]))
    if len(chat_gifs) == 0:
        await message.reply_text("**Список пуст!**")
        return
    await message.reply_text("**Список GIF:**")
    for i in chat_gifs:
        await client.send_cached_media(chat_id=message.chat.id,
                                       file_id=i)


@Client.on_message(filters.command(["add", f"add@{bot_username}"]))
async def add_gif(client, message):
    if message.chat.type == 'private':
        await message.reply_text("**Please use this command in a group!**")
        return
    try:
        file_id = message.reply_to_message.animation.file_id
        unique_id = message.reply_to_message.animation.file_unique_id
    except AttributeError:
        await message.reply_text("**Please reply to a gif to add it to the list.**")
        return
    perm = await client.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if (
            not perm.can_manage_chat
            and not perm.can_change_info
            and message.from_user.id != admin_id
    ):
        await message.reply("**You don't have permission to use this command!**")
        return
    chat = message.chat.id
    if await db.add_chat_gif(str(chat), file_id, unique_id):
        await message.reply_text("**Gif already in the list!**")
    else:
        await message.reply_text("**Gif added to the list!**")


@Client.on_message(filters.command(["remove", f"remove@{bot_username}"]))
async def remove_gif(client, message):
    if message.chat.type == 'private':
        await message.reply_text("**Please use this command in a group!**")
        return
    try:
        file_id = message.reply_to_message.animation.file_unique_id
    except AttributeError:
        await message.reply_text("**Please reply to a gif to remove it from the list.**")
        return
    perm = await client.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if (
            not perm.can_manage_chat
            and not perm.can_change_info
            and message.from_user.id != admin_id
    ):
        await message.reply("**You don't have permission to use this command!**")
        return
    chat = message.chat.id
    if await db.remove_chat_gif(str(chat), file_id):
        await message.reply_text("**Gif not in the list!**")
    else:
        await message.reply_text("**Gif removed from the list!**")


@Client.on_message(filters.command(["set_text"]))
async def set_text(client, message):
    if message.chat.type == 'private':
        await message.reply_text("**Please use this command in a group!**")
        return
    if len(message.command) < 2:
        await message.reply_text("**Please use the following format:** \n"
                                 "`/set_text Welcome`")
        return
    perm = await client.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if (
            not perm.can_manage_chat
            and not perm.can_change_info
            and message.from_user.id != admin_id
    ):
        await message.reply("**You don't have permission to use this command!**")
        return
    chat = message.chat.id
    await db.set_text(str(chat), message.text.html[10:])
    await message.reply_text("**Text successfully changed**")


@Client.on_message(filters.left_chat_member &
                   filters.create(lambda _, bot, m:
                                  bot.get_me().id == m.left_chat_member.id))
async def remove_chat(client, message):
    await db.del_chat(str(message.chat.id))
