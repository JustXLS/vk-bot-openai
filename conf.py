import tomli

with open("config.toml", "rb") as f:
    config = tomli.load(f)

with open("persons.toml", "rb") as f:
    persons = tomli.load(f)
