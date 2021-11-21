import json

import aiofiles

json_path = "WelcomeBot/data.json"


def add_chat_gif(chat, gif, unique_id):
    with open(json_path, "r+") as file:
        data = json.load(file)
        chat_gifs = data['chats'].get(chat, {}).get('gif', {})
        if unique_id in chat_gifs:
            return True
        chat_gifs[unique_id] = gif
        try:
            data['chats'][chat]['gif'] = chat_gifs
        except KeyError:
            data['chats'][chat] = {}
            data['chats'][chat]['gif'] = chat_gifs
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def remove_chat_gif(chat, unique_id):
    with open(json_path, "r+") as file:
        data = json.load(file)
        chat_gifs = data['chats'].get(chat, {}).get('gif', {})
        if unique_id not in chat_gifs:
            return True
        del chat_gifs[unique_id]
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def set_text(chat, text):
    with open(json_path, "r+") as file:
        data = json.load(file)
        try:
            data['chats'][chat]['text'] = text
        except KeyError:
            data['chats'][chat] = {}
            data['chats'][chat]['text'] = text
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def add_chat(chat):
    with open(json_path, "r+") as file:
        data = json.load(file)
        data['chats'][chat] = {}
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def del_chat(chat):
    with open(json_path, "r+") as file:
        data = json.load(file)
        del data['chats'][chat]
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


async def get_chat_gifs(chat):
    async with aiofiles.open(json_path, "r+") as file:
        contents = await file.read()
    data = json.loads(contents)
    chat_gifs = data['chats'].get(chat, {}).get('gif', {})
    chat_gifs = list(chat_gifs.values())
    return chat_gifs


async def get_chat_text(chat):
    async with aiofiles.open(json_path, "r+") as file:
        contents = await file.read()
    data = json.loads(contents)
    return data['chats'].get(chat, {}).get('text', "**Welcome**")
