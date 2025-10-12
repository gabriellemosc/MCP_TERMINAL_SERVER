import socket
import json
import logging
from .protocol import (
    MCPMessage, MCPRequest, MCPResponse, MCPMethod,
    create_success_response, create_error_response, MCPErrorCode
)
from sqlalchemy.orm import Session
from models import Veiculos, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self, host="127.0.0.1", port=65432):
        self.host = host
        self.port = port
        logger.info(f"MCP Server ready on {host}:{port}")

    def start(self):
        """Start the TCP server and accept multiple clients."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logger.info("Server started and waiting for connections...")

            while True:
                conn, addr = s.accept()
                logger.info(f"Connected by {addr}")
                # Handle each client in a separate method
                self.handle_client(conn)

    def handle_client(self, conn):
        """Handle a single client connection."""
        with conn:
            try:
                # Reeceive all the datas from client
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if len(chunk) < 4096:
                        break

                if not data:
                    return
                message_str = data.decode("utf-8")
                logger.info(f"Received message: {message_str[:100]}...")

                response = self.handle_message(message_str)



                if hasattr(response, "to_json"):
                    response_json = response.to_json()
                elif isinstance(response, dict):
                    response_json = json.dumps(response)
                else:
                    logger.warning(f"Unexpected response type: {type(response)}")
                    response_json = json.dumps({"result": str(response)})

                # send response complete
                conn.sendall(response_json.encode("utf-8"))
                logger.info(f"Sent response: {len(response_json)} characters")

            except Exception as e:
                logger.exception(f"Error handling client: {e}")
                error_response = {"error": f"Internal server error: {str(e)}"}
                try:
                    conn.sendall(json.dumps(error_response).encode("utf-8"))
                except:
                    pass  #case the connection close

    def handle_message(self, message_json: str):
        """Process MCP message and route to the right handler."""
        try:
            message = MCPMessage.from_json(message_json)

            if message.method == MCPMethod.SEARCH_VEHICLES:
                return self._handle_search(message)
            elif message.method == MCPMethod.GET_VEHICLE:
                return self._handle_get_vehicle(message)
            elif message.method == MCPMethod.HEALTH_CHECK:
                return create_success_response(message, {"status": "ok"})
            else:
                return create_error_response(message, MCPErrorCode.METHOD_NOT_FOUND, "Unknown method")

        except Exception as e:
            logger.exception("Error handling message")
            return create_error_response(
                MCPMessage.from_json('{"jsonrpc":"2.0","id":"error","method":"unknown"}'),
                MCPErrorCode.INTERNAL_ERROR,
                f"Internal error: {e}"
            )

    def _handle_search(self, request):
        try:
            params = request.params or {}
            marca = params.get("marca")
            modelo = params.get("modelo")
            ano_min = params.get("ano_min")
            ano_max = params.get("ano_max")
            tp_combustivel = params.get("tp_combustivel")
            preco_min = params.get("preco_min")
            preco_max = params.get("preco_max")

            with Session(bind=engine) as session:
                query = session.query(Veiculos)  # use each sessio with 'with'

                if marca:
                    query = query.filter(Veiculos.marca.ilike(f"%{marca}%"))
                if modelo:
                    query = query.filter(Veiculos.modelo.ilike(f"%{modelo}%"))
                if ano_min is not None:
                    query = query.filter(Veiculos.ano >= ano_min)
                if ano_max is not None:
                    query = query.filter(Veiculos.ano <= ano_max)
                if tp_combustivel:
                    query = query.filter(Veiculos.tp_combustivel.ilike(f"%{tp_combustivel}%"))
                if preco_min is not None:
                    query = query.filter(Veiculos.preco >= preco_min)
                if preco_max is not None:
                    query = query.filter(Veiculos.preco <= preco_max)

                vehicles = query.all()
                results = []



                for vehicle in vehicles:
                    results.append({
                        'id': vehicle.id,
                        'marca': vehicle.marca,
                        'modelo': vehicle.modelo,
                        'ano': vehicle.ano,
                        'motorizacao': vehicle.motorizacao,
                        'tp_combustivel': vehicle.tp_combustivel,
                        'tp_transmissao': vehicle.tp_transmissao,
                        'num_portas': vehicle.num_portas,
                        'modelo_carro': vehicle.modelo_carro,
                        'cor': vehicle.cor,
                        'quilometragem': vehicle.quilometragem,
                        'preco': float(vehicle.preco),
                        'disponivel': vehicle.disponivel
                    })


                logger.info(f"Search returned {len(results)} vehicles")
                return create_success_response(request, {"results": results, "count": len(results)})
        except Exception as e:
            logger.exception("Erro ao processar busca de veículos")
            return create_error_response(request, MCPErrorCode.INTERNAL_ERROR, str(e))

    def _handle_get_vehicle(self, request):
        vid = request.params.get("id")
        if vid is None:
            return create_error_response(request, MCPErrorCode.INVALID_PARAMS, "Vehicle ID not provided")

        with Session(bind=engine) as session:
            vehicle = session.query(Veiculos).filter(Veiculos.id == vid).first()
            if not vehicle:
                return create_error_response(request, MCPErrorCode.VEHICLE_NOT_FOUND, "Vehicle not found")



            result = {
                'id': vehicle.id,
                'marca': vehicle.marca,
                'modelo': vehicle.modelo,
                'ano': vehicle.ano,
                'motorizacao': vehicle.motorizacao,
                'tp_combustivel': vehicle.tp_combustivel,
                'tp_transmissao': vehicle.tp_transmissao,
                'num_portas': vehicle.num_portas,
                'modelo_carro': vehicle.modelo_carro,
                'cor': vehicle.cor,
                'quilometragem': vehicle.quilometragem,
                'preco': float(vehicle.preco),
                'disponivel': vehicle.disponivel
                  }

            return create_success_response(request, {"results": result, "count": 1})


if __name__ == "__main__":
    MCPServer().start()
