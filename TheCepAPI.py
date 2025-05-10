import requests
import os
from dotenv import load_dotenv

import requests

# Tipos de lista de contatos
clientes = []
fornecedores = []

# Função para buscar o endereço com base no CEP
def buscar_endereco_completo(cep):
    if len(cep) != 8 or not cep.isdigit():
        print("CEP inválido. Deve conter 8 dígitos numéricos.")
        return None

    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # Levanta erro se status HTTP não for 200
        dados = resposta.json()

        if "erro" in dados:
            print("CEP não encontrado.")
            return None

        # Organizar o endereço em formato de lista
        endereco_formatado = {
            "logradouro": dados['logradouro'],
            "bairro": dados['bairro'],
            "cidade": dados['localidade'],
            "estado": dados['uf'],
            "cep": dados['cep']
        }
        return endereco_formatado

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o ViaCEP: {e}")
        return None
    except ValueError:
        print("Erro ao processar a resposta do ViaCEP. Formato inválido.")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

# Função para aplicar a ação na lista de contatos (clientes ou fornecedores)
def aplicar_funcao(funcao_escolhida):
    print("\nEscolha a lista que você deseja visualizar:")
    print("1 - Clientes")
    print("2 - Fornecedores")
    resposta = input("Digite 1 ou 2: ")
    if resposta == "1":
        return funcao_escolhida(clientes)
    elif resposta == "2":
        return funcao_escolhida(fornecedores)
    else:
        print("Opção inválida. Tente novamente.")
        return None

# Menu principal
def menu():
    print("\nMenu de opções:")
    print("""
    0 - Sair
    1 - Cadastrar novo contato
    2 - Editar um contato
    3 - Deletar um contato
    4 - Mostrar todos os contatos cadastrados
    """)
    return input("Escolha uma opção: ")

# Cadastrar contato
def cadastrar_contato(lista_tipo_contato):
    contato = {}
    contato["codigo"] = len(lista_tipo_contato)
    contato["nome"] = input("Digite o nome: ")
    contato["email"] = input("Digite o e-mail: ")
    contato["telefone"] = input("Digite o telefone: ")

    # Buscar endereço pelo CEP
    while True:
        cep = input("Digite o CEP (somente números): ")
        endereco = buscar_endereco_completo(cep)
        if endereco:
            contato["endereco"] = endereco
            break
        else:
            print("Por favor, insira um CEP válido.")

    lista_tipo_contato.append(contato)
    print("Contato cadastrado com sucesso!")

# Editar contato
def editar_contato(lista_tipo_contato):
    try:
        codigo = int(input("Digite o código do contato que deseja editar: "))
        if 0 <= codigo < len(lista_tipo_contato):
            print("Contato atual:", lista_tipo_contato[codigo])
            nome = input("Digite o novo nome (ou deixe em branco para manter o mesmo): ")
            email = input("Digite o novo e-mail (ou deixe em branco para manter o mesmo): ")
            telefone = input("Digite o novo telefone (ou deixe em branco para manter o mesmo): ")

            # Atualizando os dados do contato
            if nome:
                lista_tipo_contato[codigo]["nome"] = nome
            if email:
                lista_tipo_contato[codigo]["email"] = email
            if telefone:
                lista_tipo_contato[codigo]["telefone"] = telefone

            # Pergunta para atualizar o endereço (caso o usuário queira)
            alterar_endereco = input("Deseja alterar o endereço? (s/n): ").lower()
            if alterar_endereco == 's':
                while True:
                    cep = input("Digite o novo CEP (somente números): ")
                    endereco = buscar_endereco_completo(cep)
                    if endereco:
                        lista_tipo_contato[codigo]["endereco"] = endereco
                        break
                    else:
                        print("Por favor, insira um CEP válido.")

            print("Contato atualizado com sucesso!")
        else:
            print("Código inválido.")
    except ValueError:
        print("Erro: O código informado não é válido. Tente novamente.")
    except IndexError:
        print("Erro: Contato não encontrado.")
    except Exception as e:
        print(f"Erro inesperado ao editar contato: {e}")

# Deletar contato
def deletar_contato(lista_tipo_contato):
    try:
        codigo = int(input("Digite o código do contato que deseja deletar: "))
        if 0 <= codigo < len(lista_tipo_contato):
            lista_tipo_contato.pop(codigo)
            # Atualiza os códigos após remoção
            for i in range(len(lista_tipo_contato)):
                lista_tipo_contato[i]["codigo"] = i
            print("Contato deletado com sucesso!")
        else:
            print("Código inválido.")
    except ValueError:
        print("Erro: O código informado não é válido. Tente novamente.")
    except Exception as e:
        print(f"Erro inesperado ao deletar contato: {e}")

# Mostrar contatos
def mostrar_contatos(lista_tipo_contato):
    if lista_tipo_contato:
        print("\nLista de contatos:")
        for contato in lista_tipo_contato:
            print(f"\nCódigo: {contato['codigo']}")
            print(f"Nome: {contato['nome']}")
            print(f"E-mail: {contato['email']}")
            print(f"Telefone: {contato['telefone']}")
            print("Endereço:")
            # Exibe o endereço em formato de lista
            endereco = contato["endereco"]
            print(f"  - Logradouro: {endereco['logradouro']}")
            print(f"  - Bairro: {endereco['bairro']}")
            print(f"  - Cidade: {endereco['cidade']}")
            print(f"  - Estado: {endereco['estado']}")
            print(f"  - CEP: {endereco['cep']}")
        
        # Perguntar ao usuário o que deseja fazer após mostrar os contatos
        while True:
            try:
                opcao = input("\nO que deseja fazer agora? (1 - Voltar ao menu, 2 - Sair): ")
                if opcao == '1':
                    break  # Volta ao menu principal
                elif opcao == '2':
                    print("Saindo do programa.")
                    exit()  # Sai do programa
                else:
                    print("Opção inválida. Tente novamente.")
            except Exception as e:
                print(f"Erro ao processar a opção: {e}")
    else:
        print("Nenhum contato cadastrado.")

# Loop principal
while True:
    try:
        opcao = menu()
        if opcao == "0":
            print("Saindo do programa.")
            break
        elif opcao == "1":
            aplicar_funcao(cadastrar_contato)
        elif opcao == "2":
            aplicar_funcao(editar_contato)
        elif opcao == "3":
            aplicar_funcao(deletar_contato)
        elif opcao == "4":
            aplicar_funcao(mostrar_contatos)
        else:
            print("Opção inválida.")
    except Exception as e:
        print(f"Erro inesperado no menu: {e}")