import openai
from conf import config

# Set the API key
openai.api_key = config["secrets"]["openai"]

# Set the model
model_engine = "text-davinci-003"

# Set the number of completions
num_completions = 1

# Set the temperature
temperature = 1

# Set the max tokens
max_tokens = config["limits"]["generating_tokens"]

# Set the top p
top_p = 1

# Set the frequency penalty
frequency_penalty = 0

# Set the presence penalty
presence_penalty = 0


def generate(prompt):
    # Send the request to ChatGPT
    completions = openai.Completion.create(
        model=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=num_completions,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return completions.choices[0].text
