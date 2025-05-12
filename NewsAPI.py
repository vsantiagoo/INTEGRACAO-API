import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY_NEWS")

if not api_key:
    raise ValueError("API Key não encontrada nas variáveis.")

url = "https://newsapi.org/v2/everything"

params = {
    "q": "tecnologia",  # você pode alterar a palavra-chave de busca
    "language": "pt",   # ou "en" para inglês
    "pageSize": 10      # quantas notícias trazer
}

headers = {
    'x-api-key': api_key
}

resposta = requests.get(url=url, headers=headers, params=params)
print("Status da requisição:", resposta.status_code)

if resposta.status_code != 200:
    print("Erro na requisição:", resposta.text)
    exit()

resposta_json = resposta.json()

print("\nSite da notícia na posição 7:", resposta_json["articles"][7]["source"]["name"])

print("\n--- Primeiras 10 notícias ---\n")
for i, artigo in enumerate(resposta_json["articles"][:10], start=1):
    print(f"{i}. Título: {artigo['title']}")
    print(f"   Fonte: {artigo['source']['name']}")
    print(f"   Link: {artigo['url']}\n")