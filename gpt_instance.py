from conf import config
from translator import generate_russian


class GptInstance:
    def __init__(self, id: str, params: dict):
        self.id = id
        self.prefix = params["prefix"]
        self.name = params["name"]
        self.prompt = params["prompt"]
        self.history = []

    def is_triggered(self, text: str) -> bool:
        i = text.lower().find(self.name.lower())
        return text.startswith(self.prefix) or (i != -1 and (i == 0 or text[i-1] == " "))

    def construct_prompt(self) -> str:
        msgs = "\n".join(self.history)
        return f"{self.prompt}\n{msgs}\n{self.name}: "

    def generate(self) -> str:
        while len(prompt := self.construct_prompt()) > config["limits"]["max_context"] and len(self.history) > 0:
            self.history.pop(0)
        output = generate_russian(prompt).strip()
        return output
