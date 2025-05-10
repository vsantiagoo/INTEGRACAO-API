import requests

# Substitua com a sua chave da API
API_KEY = 'sua_api_key_aqui'

# Endpoint para buscar uma imagem aleatória de cachorro
url = 'https://api.thedogapi.com/v1/images/search'

# Headers com a API Key
headers = {
    'x-api-key': API_KEY
}

# Fazendo a requisição GET
response = requests.get(url, headers=headers)

# Verificando o status e exibindo o resultado
if response.status_code == 200:
    data = response.json()
    for dog in data:
        print("Imagem:", dog['url'])
else:
    print("Erro na requisição:", response.status_code, response.text)

    import requests

url = "https://api.thedogapi.com/v1/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=1"

headers = {
    "Content-Type": "application/json",
    "x-api-key": "DEMO-API-KEY"
}

try:
    response = requests.get(url, headers=headers, allow_redirects=True)
    response.raise_for_status()  # Lança erro se a resposta for um código 4xx/5xx
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"error: {e}")