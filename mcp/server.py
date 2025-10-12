import socket
import json
import logging
from protocol import (
    MCPMessage, MCPRequest, MCPResponse, MCPMethod,
    create_success_response, create_error_response, MCPErrorCode
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self, host="127.0.0.1", port=65432):
        self.host = host
        self.port = port
        self.vehicles_db = [
            {"id": 1, "marca": "Toyota", "modelo": "Corolla", "ano": 2022, "preco": 110000, "cor": "Prata", "quilometragem": 25000, "tp_combustivel": "Gasolina", "tp_transmissao": "Automática", "motorizacao": "2.0", "num_portas": 4, "disponivel": True},
            {"id": 2, "marca": "Honda", "modelo": "Civic", "ano": 2020, "preco": 95000, "cor": "Preto", "quilometragem": 40000, "tp_combustivel": "Flex", "tp_transmissao": "Manual", "motorizacao": "1.8", "num_portas": 4, "disponivel": True}
        ]
        logger.info(f"MCP Server listening on {host}:{port}")

    def start(self):
        """Start the TCP server and wait for clients."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logger.info("Server started and waiting for connections...")

            while True:
                conn, addr = s.accept()
                with conn:
                    logger.info(f"Connected by {addr}")
                    data = conn.recv(4096)
                    if not data:
                        break
                    response = self.handle_message(data.decode())
                    conn.sendall(response.encode())

    def handle_message(self, message_json: str) -> str:
        """Process the MCP message and return the response as JSON."""
        try:
            message = MCPMessage.from_json(message_json)

            if message.method == MCPMethod.SEARCH_VEHICLES:
                return self._handle_search(message).to_json()
            elif message.method == MCPMethod.GET_VEHICLE:
                return self._handle_get_vehicle(message).to_json()
            elif message.method == MCPMethod.HEALTH_CHECK:
                return create_success_response(message, {"status": "ok"}).to_json()
            else:
                return create_error_response(message, MCPErrorCode.METHOD_NOT_FOUND, "Unknown method").to_json()

        except Exception as e:
            logger.exception("Error handling message")
            return json.dumps({"error": f"Internal error: {e}"})

    def _handle_search(self, request: MCPRequest) -> MCPResponse:
        params = request.params
        marca = params.get("marca")
        ano = params.get("ano")
        tp_combustivel = params.get("tp_combustivel")

        result = [v for v in self.vehicles_db if
                  (not marca or v["marca"].lower() == marca.lower()) and
                  (not ano or v["ano"] == ano) and
                  (not tp_combustivel or v["tp_combustivel"].lower() == tp_combustivel.lower())]

        return create_success_response(request, {"results": result, "count": len(result)})

    def _handle_get_vehicle(self, request: MCPRequest) -> MCPResponse:
        vid = request.params.get("id")
        vehicle = next((v for v in self.vehicles_db if v["id"] == vid), None)
        if not vehicle:
            return create_error_response(request, MCPErrorCode.VEHICLE_NOT_FOUND, "Vehicle not found")
        return create_success_response(request, vehicle)

if __name__ == "__main__":
    MCPServer().start()
