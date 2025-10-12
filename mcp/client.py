import socket
import json
from .protocol import MCPRequest, MCPMethod

HOST = '127.0.0.1'
PORT = 65432

def send_mcp_request(method: MCPMethod, params: dict) -> dict:
    """Sends an MCP request and returns a dict"""
    request = MCPRequest(method=method, params=params)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.to_json().encode('utf-8'))
        
        # ✅ CORREÇÃO: Receber dados em chunks até completar
        response_data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_data += chunk
            # Tentar parsear para ver se é JSON completo
            # try:
            #     json.loads(response_data.decode('utf-8'))
            #     break  # JSON completo, para de receber
            # except json.JSONDecodeError:
            #     continue  # Continua recebendo
        
        response_str = response_data.decode('utf-8')
        response = json.loads(response_str)
        print(f"DEBUG Received {len(response_str)} characters")
        return json.loads(response)


def show_all_vehicles():
    print("🔎 Fetching all vehicles from the database...")

    # Passa um dict vazio para pegar todos os veículos
    response = send_mcp_request(MCPMethod.SEARCH_VEHICLES, {})

    if response.get("result") and "results" in response["result"]:
        results = response["result"]["results"]
        print(f"\n✅ Encontramos {len(results)} veículo(s) no banco:\n")
        for v in results:
            print(f"ID {v['id']} - {v['marca']} {v['modelo']} ({v['ano']}) - "
                  f"{v['cor']}, {v['quilometragem']} km - R$ {v['preco']} - "
                  f"{'Disponível' if v['disponivel'] else 'Indisponível'}")
    else:
        print(f"\n❌ Erro: {response.get('error', 'Resposta inválida do servidor')}")

if __name__ == "__main__":
    show_all_vehicles()
