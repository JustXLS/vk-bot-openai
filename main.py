from urllib.request import urlopen

import tomli
from vkbottle.bot import Bot, Message
from conf import config, persons, reload_from_url_persons
from gpt_instance import GptInstance
from random import randint


global_prefix = config["global_prefix"]
chats: dict[int, list[GptInstance]] = {}
bot = Bot(config["secrets"]["vk"])


async def get_username(id: int) -> str:
    if id < 0:
        group = (await bot.api.groups.get_by_id(group_id=-id))[0]
        return group.name
    else:
        user = (await bot.api.users.get(id))[0]
        return user.first_name + f" {user.last_name[0]}."


def add_to_all_history(chat_id: int, text: str):
    for instance in chats.get(chat_id, []):
        instance.history += [text]


@bot.on.message(blocking=False)
async def history_clear(msg: Message) -> str:
    for instance in chats.get(msg.chat_id, []):
        if msg.text == instance.prefix + "r":
            msg.text = msg.text[len(instance.prefix):]
            instance.history = []
            await msg.reply(f"История сообщений очищена для {instance.prefix} ({instance.name})")


@bot.on.message(blocking=False)
async def save_history(msg: Message) -> str:
    username = await get_username(msg.from_id)
    for instance in chats.get(msg.chat_id, []):
        text = msg.text
        if text.startswith(instance.prefix):
            text = text[len(instance.prefix):].strip()
        instance.history += [f"{username}: {text}"]


async def recursive_generation(chat_id: int, text: str, depth: int = 0):
    if depth >= 4:
        return
    for instance in chats.get(chat_id, []):
        if instance.is_triggered(text):
            generation = instance.generate()
            add_to_all_history(chat_id, f"{instance.name}: {generation}")
            await bot.api.messages.send(chat_id=chat_id, message=f"{instance.name}: {generation}", random_id=randint(0, 100000))
            await recursive_generation(chat_id, generation, depth + 1)


@bot.on.message(blocking=False)
async def generate(msg: Message) -> str:
    await recursive_generation(msg.chat_id, msg.text)


@bot.on.message(text=f"{global_prefix} list<_>")
async def list_persons(*_):
    reply = "Доступные боты:"
    for id in persons.keys():
        name = persons[id]["name"]
        reply += f"\n{id} - {name}"
    return reply


@bot.on.message(text=f"{global_prefix} active<_>")
async def list_active_persons(msg: Message, _):
    if msg.chat_id not in chats:
        return "Нет активных ботов в этом чате"
    reply = "Активные боты в этом чате:"
    for instance in chats[msg.chat_id]:
        reply += f"\n{instance.id} - {instance.name}"
    return reply


@bot.on.message(text=f"{global_prefix} toggle <id>")
async def toggle_active_person(msg: Message, id: str):
    if msg.chat_id not in chats:
        chats[msg.chat_id] = []
    chat = chats[msg.chat_id]
    if id not in persons:
        return "Нет такого бота"
    try:
        i = next(i for i, x in enumerate(chat) if x.id == id)
        instance = chat.pop(i)
        return f"{instance.id} ({instance.name}) выключен"
    except StopIteration:
        instance = GptInstance(id, persons[id])
        chat += [instance]
        return f"{instance.id} ({instance.name}) активирован"


@bot.on.message(text=f"{global_prefix} reload")
async def toggle_active_person(msg: Message):
    global persons
    f = urlopen(config["persons_url"])
    persons = tomli.load(f)
    return "Конфиг ботов перезагружен"


bot.run_forever()
