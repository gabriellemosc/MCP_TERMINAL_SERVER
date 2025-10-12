# mcp/__init__.py

"""
Pacote MCP: Implementação do Model Context Protocol (MCP)
Inclui servidor, cliente e tipos de mensagens.
"""

# --- Servidor ---
from .server import MCPServer

# --- Cliente ---
from .client import show_all_vehicles, send_mcp_request

# --- Protocolo MCP ---
from .protocol import (
    MCPMessage,
    MCPRequest,
    MCPResponse,
    MCPMethod,
    MCPErrorCode,
    create_success_response,
    create_error_response
)

# --- Tipos de mensagens específicos ---
from .message_type import (
    VehicleSearchRequest,
    VehicleSearchResponse,
    VehicleResponse,
    HealthResponse,
    AvailableFilters
)

# --- Exportações públicas do pacote ---
__all__ = [
    "MCPServer",
    "agent_conversation",
    "send_mcp_request",
    "MCPMessage",
    "MCPRequest",
    "MCPResponse",
    "MCPMethod",
    "MCPErrorCode",
    "create_success_response",
    "create_error_response",
    "VehicleSearchRequest",
    "VehicleSearchResponse",
    "VehicleResponse",
    "HealthResponse",
    "AvailableFilters",
]
