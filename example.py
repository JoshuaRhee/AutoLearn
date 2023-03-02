import openai
import requests

with open('key.txt', 'r') as f:
    key = f.read()[:1:-1] # put any character at the front of the key
openai.api_key = key

prompt = "Hello, how are you?"

response = requests.post("https://api.openai.com/v1/engines/davinci-codex/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    },
    json={
        "prompt": prompt,
        "max_tokens": 10
    }
)

print(response.json()["choices"][0]["text"])