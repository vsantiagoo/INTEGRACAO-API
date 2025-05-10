import requests
import os
from dotenv import load_dotenv
 
load_dotenv()
 
api_key = os.getenv("API_KEY_NEWS")
 
if not api_key:
    raise ValueError("API Key não encontrada nas varíaveis.")
 
url = "https://newsapi.org/v2/everything"
 
headers = {
    'x-api-key': api_key
}
 
resposta = requests.get(url=url, headers=headers)
print(resposta.status_code)
 
resposta_json = resposta.json()
 
print("Site da noticia de posição 7:", resposta_json["articles"][7]["source"]["name"])
 
 
for artigo in resposta_json["articles"][:10]:

    