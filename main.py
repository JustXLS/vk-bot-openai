from vkbottle.bot import Bot, Message
from vkbottle import GroupEventType
from conf import config
from translator import generate_russian


prefix = config["prefix"]
name = config["name"]
start = config["prompt"]
array = []
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
    global array
    if msg.text.startswith(prefix):
        text = msg.text[len(prefix):].strip()
    else:
        text = msg.text
    if len(msg.text) > 0:
        from_name = await get_username(msg.from_id)
        array += [f"{from_name}: {text}"]
    print("DEBUG!!!!!!:", array)


@bot.on.message(text=[f"{prefix}r"])
async def history_clear(_) -> str:
    global array
    array = []
    return "История сообщений очищена."


def generate_match(s: Message):
    s_low = s.text.lower()
    return s_low.startswith(prefix) or name.lower() in s_low


@bot.on.message(func=generate_match)
async def generate(*_) -> str:
    global array
    history = "\n".join(array)
    prompt = f"{start}\n{history}\n{name}: "
    while len(prompt) > config["limits"]["max_context"]:
        array.pop(0)
        prompt = f"{start}\n{history}\n{name}: "
    output = generate_russian(prompt)
    if output.endswith("\n"):
        output = output[:-1]
    array += [f"{name}: {output}"]
    return output


bot.run_forever()
