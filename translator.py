from python_translator import Translator
import gpt


translator = Translator()


def translate(text, src, dest):
    translation = translator.translate_text(text, dest, src)
    return str(translation)


def generate_russian(text: str) -> str:
    eng_prompt = translate(text, "ru", "en")
    eng_gen = gpt.generate(eng_prompt)
    rus_gen = translate(eng_gen, "en", "ru")
    return rus_gen
