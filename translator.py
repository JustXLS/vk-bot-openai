from python_translator import Translator
import gpt
from conf import config

lang = config["lang"]
translator = Translator()


def translate(text, src, dest):
    translation = translator.translate_text(text, dest, src)
    return str(translation)


def generate_lang(text: str) -> str:
    eng_prompt = translate(text, lang, "en")
    eng_gen = gpt.generate(eng_prompt)
    lang_gen = translate(eng_gen, "en", lang)
    return lang_gen
