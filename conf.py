import tomli
from urllib.request import urlopen

with open("config.toml", "rb") as f:
    config = tomli.load(f)

with open("persons.toml", "rb") as f:
    persons = tomli.load(f)

if "config_url" in config:
    f = urlopen(config["config_url"])
    config = tomli.load(f)

persons = None


def reload_from_url_persons():
    global persons
    if "persons_url" in config:
        f = urlopen(config["persons_url"])
        persons = tomli.load(f)


reload_from_url_persons()

