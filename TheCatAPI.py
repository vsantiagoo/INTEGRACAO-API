import requests
import os
from dotenv import load_dotenv

import requests

# Função para buscar todas as raças disponíveis
def obter_racas():
    url = "https://api.thecatapi.com/v1/breeds"
    resposta = requests.get(url).json()
    return resposta

# Função principal de busca
def buscar_gatos():
    racas = obter_racas()

    # Menu de filtro
    while True:
        print("\n📋 Escolha o tipo de filtro para a busca:")
        print("[1] Buscar por raça")
        print("[2] Buscar por país de origem")
        print("[3] Buscar livre (sem filtro)")

        filtro = input("Digite sua opção: ")

        if filtro not in ['1', '2', '3']:
            print("Opção inválida. Tente novamente.\n")
            continue

        breed_id = None  # usado apenas se for filtro por raça

        if filtro == '1':
            print("\n🐾 Raças disponíveis (limitado a 5):")
            racas_limitadas = racas[:5]  # Limita às 5 primeiras raças
            for idx, raca in enumerate(racas_limitadas):
                print(f"[{idx}] {raca['name']}")

            try:
                escolha = int(input("Digite o número da raça desejada: "))
                breed_id = racas_limitadas[escolha]['id']
            except (ValueError, IndexError):
                print("Raça inválida. Retornando ao menu...\n")
                continue

        elif filtro == '2':
            # Lista de países permitidos (limitado)
            paises_permitidos = ["Brazil", "United States", "Japan", "China", "Italy"]
            print("\n🌍 Países de origem disponíveis:")
            for idx, pais in enumerate(paises_permitidos):
                print(f"[{idx}] {pais}")

            try:
                escolha = int(input("Digite o número do país desejado: "))
                pais_escolhido = paises_permitidos[escolha]
                racas_filtradas = [r['id'] for r in racas if r['origin'] == pais_escolhido]
                if not racas_filtradas:
                    print("Nenhuma raça encontrada para esse país.\n")
                    continue
                breed_id = ",".join(racas_filtradas)
            except (ValueError, IndexError):
                print("País inválido. Retornando ao menu...\n")
                continue

        # Menu de imagem ou gif
        tipo = input("\nVocê quer ver [1] Imagens ou [2] GIFs de gatos? ")
        if tipo not in ['1', '2']:
            print("Escolha inválida! Digite 1 ou 2.\n")
            continue
        mime_type = "gif" if tipo == '2' else "jpg,png"

        # Laço para quantidade
        while True:
            try:
                qtd = int(input("Quantos gatos você quer ver? (máx 5): "))
                if 1 <= qtd <= 5:
                    url = f"https://api.thecatapi.com/v1/images/search?limit={qtd}&mime_types={mime_type}"
                    if breed_id:
                        url += f"&breed_ids={breed_id}"

                    resposta = requests.get(url).json()

                    if not resposta:
                        print("Nenhum resultado encontrado para os filtros escolhidos.")
                    else:
                        print("\n🐱 Resultados:")
                        for i, gato in enumerate(resposta[:qtd], 1):
                            print(f"Gato {i}: {gato['url']}")
                    break
                else:
                    print("Digite um número entre 1 e 5.\n")
            except ValueError:
                print("Entrada inválida. Use apenas números.\n")
        break


# Loop principal
while True:
    buscar_gatos()
    nova_busca = input("\n🔄 Deseja fazer uma nova busca? (s/n): ").lower()
    if nova_busca != 's':
        print("\n👋 Encerrando o programa. Até a próxima!")
        break