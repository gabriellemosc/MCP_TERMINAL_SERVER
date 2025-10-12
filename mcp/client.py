import socket
import json
from protocol import MCPRequest, MCPMethod

HOST = '127.0.0.1'
PORT = 65432

def send_mcp_request(method: MCPMethod, params: dict) -> dict:
    """Sends an MCP request, and return a dict"""
    request = MCPRequest(
        method=method, params=params)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(request.to_json().encode('utf-8'))
        response_data = s.recv(4096).decode('utf-8')

    # Convert the request JSON in DICT 
    response_json = json.loads(response_data)
    return response_json

def agent_conversation():
    print(" Hello. I'm the assistant, Gabriel. Let's Find your ideal car?")
    print("Can you tell me what you are looking? \n")

    # Interactive  collection
    marca = input("Do you have any brands in mind?")
    modelo = input("And any specific model? ")
    ano_min = input("Minimum year of car? ")
    ano_max = input("Max year of car? ")
    tp_combustivel = input("Fuel type? (Gasoline, Alcohol, Flex)")
    preco_min = input("Min price? ")
    preco_max = input("Max price? ")

    # filter buildere
    filters = {"marca": marca or None, "modelo": modelo or None,
        "ano_min": int(ano_min) if ano_min else None,"ano_max": int(ano_max) if ano_max else None,
        "tp_combustivel": tp_combustivel or None,
        "preco_min": float(preco_min) if preco_min else None, "preco_max": float(preco_max) if preco_max else None}

    print("\n Searching for vehicles... ")

    # Send the request to server  
    response = send_mcp_request(MCPMethod.SEARCH_VEHICLES, filters)

    # show results  
    if response.get("result") and "results" in response["result"]:
        results = response["result"]["results"]
        if results:
            print(f" Encontramos {len(results)} veículo(s) compatíveis")
            for v in results:
                print(f"{v['marca']} {v['modelo']} ({v['ano']}) - {v['cor']}, "
                      f"{v['quilometragem']} km - R$ {v['preco']}")
        else:
            print("\n⚠️ Nenhum veículo encontrado com esses filtros.")
    else:
        print(f"Erro: {response.get('error', 'Resposta inválida  servidor')}")

if __name__ == "__main__":
    agent_conversation()
