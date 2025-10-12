import socket
import json
from mcp.protocol import MCPRequest, MCPMethod  

HOST = '127.0.0.1'
PORT = 65432

def send_mcp_request(method: MCPMethod, params: dict) -> dict:


    request = MCPRequest(method=method, params=params)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)  #limit of five seconds
        try:
            s.connect((HOST, PORT))
            s.sendall(request.to_json().encode('utf-8'))

            # receive all the data
            response_data = b""
            while True:
                try:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    response_data += chunk

                    try:
                        parsed = json.loads(response_data.decode('utf-8'))
                        return parsed  
                    except json.JSONDecodeError:
                        continue 
                except socket.timeout:
                    print("Tentando finalizar...")
                    break

            #  decode what receive
            response_str = response_data.decode('utf-8').strip()
            if not response_str:
                return {"error": "Empty response from server"}
            try:
                return json.loads(response_str)
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"📄 Response preview: {response_str[:200]}...")
                return {"error": f"Invalid JSON: {e}"}

        except (ConnectionRefusedError, socket.timeout) as e:
            return {"error": f"Connection failed: {e}"}


