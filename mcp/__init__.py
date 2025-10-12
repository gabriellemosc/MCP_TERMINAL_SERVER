# mcp/__init__.py

"""
Package: Implementation of MCP
Include server, client and type of messages
"""

# SERVER
from .server import MCPServer

# CLIENT
from .client import  send_mcp_request          

# PROTOCOL MCP
from .protocol import (
    MCPMessage,
    MCPRequest,
    MCPResponse,
    MCPMethod,
    MCPErrorCode,
    create_success_response,
    create_error_response
)

# TYPES OF MESSAGES
from .message_type import (
    VehicleSearchRequest,
    VehicleSearchResponse,
    VehicleResponse,
    HealthResponse,
    AvailableFilters
)

#  public exportations
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
