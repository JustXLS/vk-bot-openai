import tomli
from vkbottle.bot import Bot, Message
from conf import config, persons
from gpt_instance import GptInstance


global_prefix = config["global_prefix"]
chats: dict[int, list[GptInstance]] = {}
bot = Bot(config["secrets"]["vk"])


async def get_username(id: int) -> str:
    if id < 0:
        group = (await bot.api.groups.get_by_id(group_id=-id))[0]
        return group.name
    else:
        user = (await bot.api.users.get(id))[0]
        return user.first_name


@bot.on.message(blocking=False)
async def save_history(msg: Message) -> str:
    username = await get_username(msg.from_id)
    for instance in chats.get(msg.chat_id, []):
        text = msg.text
        if text.startswith(instance.prefix):
            text = text[len(instance.prefix):].strip()
        instance.history += [f"{username}: {text}"]


@bot.on.message(blocking=False)
async def history_clear(msg: Message) -> str:
    for instance in chats.get(msg.chat_id, []):
        if msg.text.startswith(instance.prefix + "r"):
            instance.history = []
            await msg.reply(f"История сообщений очищена для {instance.prefix} ({instance.name})")


@bot.on.message(blocking=False)
async def generate(msg: Message) -> str:
    for instance in chats.get(msg.chat_id, []):
        if instance.is_triggered(msg.text):
            generation = instance.generate()
            await msg.reply(f"{generation}")


@bot.on.message(text=f"{global_prefix} list<_>")
async def list_persons(*_):
    reply = "Доступные боты:"
    for id in persons.keys():
        name = persons[id]["name"]
        reply += f"\n{id} - {name}"
    return reply


@bot.on.message(text=f"{global_prefix} active<_>")
async def list_active_persons(msg: Message, _):
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
        return f"{instance.id} ({instance.name}) включен"


bot.run_forever()
