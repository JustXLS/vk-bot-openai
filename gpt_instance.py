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
        return text.startswith(self.prefix) or self.name.lower() in text.lower()

    def construct_prompt(self) -> str:
        msgs = "\n".join(self.history)
        return f"{self.prompt}\n{msgs}\n{self.name}: "

    def generate(self) -> str:
        while len(prompt := self.construct_prompt()) > config["limits"]["max_context"] and len(self.history) > 0:
            self.history.pop(0)
        output = generate_russian(prompt).strip()
        self.history += [f"{self.name}: {output}"]
        return output
