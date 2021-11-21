import motor.motor_asyncio

from WelcomeBot import mongo_url

client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
db = client.WelcomeBot
chats = db['chats']


async def add_chat_gif(chat, gif, unique_id):
    chat = await chats.find_one({'chat_id': chat})
    chat_gifs = chat.get('gif', {})
    if unique_id in chat_gifs:
        return True
    await chats.update_one(chat, {'$set': {f'gif.{unique_id}': gif}})


async def remove_chat_gif(chat, unique_id):
    chat = await chats.find_one({'chat_id': chat})
    chat_gifs = chat.get('gif', {})
    if unique_id not in chat_gifs:
        return True
    await chats.update_one(chat, {'$unset': {f'gif.{unique_id}': ""}})


async def set_text(chat, text):
    chat = await chats.find_one({'chat_id': chat})
    await chats.update_one(chat, {'$set': {'text': text}})


async def add_chat(chat):
    await chats.insert_one({'chat_id': chat})


async def del_chat(chat):
    await chats.delete_one({'chat_id': chat})


async def get_chat_gifs(chat):
    chat = await chats.find_one({'chat_id': chat})
    chat_gifs = chat.get('gif', {})
    return list(chat_gifs.values())


async def get_chat_text(chat):
    chat = await chats.find_one({'chat_id': chat})
    return chat.get('text', '**Welcome**')
