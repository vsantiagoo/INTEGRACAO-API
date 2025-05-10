import requests
import os
from dotenv import load_dotenv

load_dotenv ()

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API Key não encontrada nas variáveis de ambiente!")

url = "https://api.thedogapi.com/v1/images/search?limit=5"

headers = {
    'x-api-key': api_key
}

params = {
    "limit": 5
}

resposta = requests.get(url=url, headers=headers)
print(resposta.status_code)
if resposta.status_code == 200:
    print(resposta.json())
