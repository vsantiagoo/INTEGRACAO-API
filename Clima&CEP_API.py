import os
import requests

# 🔐 Substitua por sua chave real da API OpenWeather
API_KEY = os.getenv("API_KEY_CLIMA")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# 🌍 Lista de cidades com identificadores
cidades = {
    1: "Blumenau,BR",
    2: "São Paulo,BR",
    3: "Curitiba,BR",
    4: "Florianopolis,BR",
    5: "Balneario Camboriu,BR"
}

# 📡 Buscar dados climáticos da API
def obter_clima(cidade):
    params = {
        "q": cidade,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt"
    }
    try:
        resposta = requests.get(BASE_URL, params=params)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados para {cidade}: {e}")
        return None

def obter_cidade_por_cep(cep):
    if not cep.isdigit() or len(cep) != 8:
        print("❌ CEP inválido. Certifique-se de digitar 8 números.")
        return None

    try:
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json")
        if resposta.status_code == 200:
            dados = resposta.json()
            if "erro" in dados:
                print("❌ CEP não encontrado. Verifique se digitou corretamente.")
                return None
            return f"{dados['localidade']}"
        else:
            print(f"❌ Erro {resposta.status_code} ao consultar o CEP.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao se conectar à API ViaCEP: {e}")
        return None

# 📋 Exibir informações formatadas
def exibir_informacoes(dados, nome_cidade):
    temp = dados['main']['temp']
    clima = dados['weather'][0]['description']
    umidade = dados['main']['humidity']
    print(f"\n📍 Cidade: {nome_cidade}")
    print(f"🌡️ Temperatura: {temp}°C")
    print(f"☁️ Clima: {clima.capitalize()}")
    print(f"💧 Umidade: {umidade}%")

# 🔥 Mostrar cidade mais quente
def cidade_mais_quente(temperaturas):
    mais_quente = max(temperaturas, key=temperaturas.get)
    print(f"\n🔥 A cidade mais quente agora é: {mais_quente} ({temperaturas[mais_quente]}°C)")

# 🧭 Menu de escolha principal
def menu_principal():
    print("\nComo você gostaria de ver as informações do clima?")
    print("1 - Ver o clima de TODAS as cidades")
    print("2 - Escolher uma ou mais cidades")
    print("3 - Consultar clima por CEP")
    return input("Digite 1, 2 ou 3: ").strip()

# 🧑‍💻 Menu final com nova opção
def menu_final():
    print("\nDeseja fazer outra ação?")
    print("1 - Voltar ao menu principal")
    print("2 - Pesquisar por uma cidade individual (via número)")
    print("3 - Finalizar o programa")
    return input("Digite 1, 2 ou 3: ").strip()

# 🔄 Loop de execução
def main():
    while True:
        escolha = menu_principal()
        temperaturas = {}

        if escolha == "1":
            for cidade_nome in cidades.values():
                dados = obter_clima(cidade_nome)
                if dados:
                    exibir_informacoes(dados, cidade_nome.split(",")[0])
                    temperaturas[cidade_nome.split(",")[0]] = dados['main']['temp']
            if temperaturas:
                cidade_mais_quente(temperaturas)

        elif escolha == "2":
            print("\nEscolha as cidades pelo número (ex: 1,2):")
            for num, nome in cidades.items():
                print(f"{num} - {nome.split(',')[0]}")
            escolhas = input("Digite os números separados por vírgula: ")
            try:
                indices = [int(i.strip()) for i in escolhas.split(",")]
                for i in indices:
                    cidade_nome = cidades.get(i)
                    if cidade_nome:
                        dados = obter_clima(cidade_nome)
                        if dados:
                            exibir_informacoes(dados, cidade_nome.split(",")[0])
                            temperaturas[cidade_nome.split(",")[0]] = dados['main']['temp']
                if temperaturas:
                    cidade_mais_quente(temperaturas)
            except ValueError:
                print("❌ Entrada inválida. Por favor, digite números separados por vírgula.")

        elif escolha == "3":
            cep = input("\nDigite o CEP da cidade (apenas números): ").strip()
            if len(cep) == 8 and cep.isdigit():
                cidade_com_uf = obter_cidade_por_cep(cep)
                if cidade_com_uf:
                    dados = obter_clima(cidade_com_uf)
                    if dados:
                        exibir_informacoes(dados, cidade_com_uf.split(",")[0])
            else:
                print("❌ CEP inválido. Deve conter 8 dígitos numéricos.")

        else:
            print("❌ Opção inválida. Tente novamente.")
            continue

        # Menu final
        while True:
            opcao = menu_final()
            if opcao == "1":
                break  # Volta ao menu principal

            elif opcao == "2":
                print("\nEscolha uma cidade pelo número:")
                for num, nome in cidades.items():
                    print(f"{num} - {nome.split(',')[0]}")
                try:
                    cidade_num = int(input("Digite o número da cidade: ").strip())
                    cidade_nome = cidades.get(cidade_num)
                    if cidade_nome:
                        dados = obter_clima(cidade_nome)
                        if dados:
                            exibir_informacoes(dados, cidade_nome.split(",")[0])
                    else:
                        print("❌ Número inválido.")
                except ValueError:
                    print("❌ Entrada inválida. Digite apenas o número da cidade.")
            elif opcao == "3":
                print("👋 Encerrando o programa. Até logo!")
                return
            else:
                print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()