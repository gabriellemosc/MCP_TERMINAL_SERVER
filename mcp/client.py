import socket
import json
from protocol import MCPRequest, MCPMethod

HOST = '127.0.0.1'
PORT = 65432

def send_mcp_request(method: MCPMethod, params: dict) -> dict:
    """Envia uma requisição MCP ao servidor e retorna a resposta como dicionário"""
    request = MCPRequest(
        method=method,
        params=params
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.to_json().encode('utf-8'))
        response_data = s.recv(4096).decode('utf-8')

    # Converte a resposta JSON em objeto dicionário
    response_json = json.loads(response_data)
    return response_json

def agent_conversation():
    print("👋 Olá! Eu sou o seu assistente virtual de veículos. Vamos achar seu carro ideal?")
    print("Pode me contar o que você está procurando de forma natural.\n")

    # Coleta interativa de dados
    marca = input("Você tem alguma marca em mente? ")
    modelo = input("E algum modelo específico? ")
    ano_min = input("Ano mínimo do carro? ")
    ano_max = input("Ano máximo do carro? ")
    tp_combustivel = input("Tipo de combustível? (Gasolina, Flex, Diesel...) ")
    preco_min = input("Preço mínimo? ")
    preco_max = input("Preço máximo? ")

    # Constrói filtros
    filters = {
        "marca": marca or None,
        "modelo": modelo or None,
        "ano_min": int(ano_min) if ano_min else None,
        "ano_max": int(ano_max) if ano_max else None,
        "tp_combustivel": tp_combustivel or None,
        "preco_min": float(preco_min) if preco_min else None,
        "preco_max": float(preco_max) if preco_max else None
    }

    print("\n🔎 Procurando veículos compatíveis...")

    # Envia requisição para o servidor
    response = send_mcp_request(MCPMethod.SEARCH_VEHICLES, filters)

    # Mostra resultados
    if response.get("result") and "results" in response["result"]:
        results = response["result"]["results"]
        if results:
            print(f"\n✅ Encontramos {len(results)} veículo(s) compatível(is):\n")
            for v in results:
                print(f"{v['marca']} {v['modelo']} ({v['ano']}) - {v['cor']}, "
                      f"{v['quilometragem']} km - R$ {v['preco']}")
        else:
            print("\n⚠️ Nenhum veículo encontrado com esses filtros.")
    else:
        print(f"\n❌ Erro: {response.get('error', 'Resposta inválida do servidor')}")

if __name__ == "__main__":
    agent_conversation()
