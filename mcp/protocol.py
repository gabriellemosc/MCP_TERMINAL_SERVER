"""
Inspired im JSON-RPC 2.0 protocol
"""

import json
import logging
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime
import uuid

# basic logger setup
logger = logging.getLogger(__name__)

class MCPMessageType(Enum):
    # Types of messages in MCP protocol
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


class MCPMethod(Enum):
    # Operations supported by MCP
    SEARCH_VEHICLES = "search_vehicles"
    GET_VEHICLE = "get_vehicle"
    HEALTH_CHECK = "health_check"
    LIST_FILTERS = "list_filters"


class MCPErrorCode(Enum):
    # Error codes (based on JSON-RPC + custom domain errors)
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

    VEHICLE_NOT_FOUND = -32001
    INVALID_FILTERS = -32002
    DATABASE_ERROR = -32003
    SERVER_ERROR = -32000


class MCPError:
    # Represents an error message

    def __init__(self, code: int, message: str, data: Optional[Any] = None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        err = {"code": self.code, "message": self.message}
        if self.data is not None:
            err["data"] = self.data
        return err

    @classmethod
    def from_dict(cls, err_dict: Dict[str, Any]) -> 'MCPError':
        return cls(
            code=err_dict.get("code", MCPErrorCode.INTERNAL_ERROR.value),
            message=err_dict.get("message", "Unknown error"),
            data=err_dict.get("data")
        )

    def __str__(self):
        return f"MCPError({self.code}: {self.message})"


class MCPMessage:
    """
    Base  for all MCP protocol messages
    """

    def __init__(
        self,
        message_type: MCPMessageType,
        method: Optional[MCPMethod] = None,
        params: Optional[Dict[str, Any]] = None,
        result: Optional[Any] = None,
        error: Optional[Dict[str, Any]] = None,
        message_id: Optional[str] = None
    ):
        self.message_type = message_type
        self.method = method
        self.params = params or {}
        self.result = result
        self.error = error
        self.message_id = message_id or str(uuid.uuid4())
        self.timestamp = datetime.utcnow().isoformat()

        self._validate()

    def _validate(self):
        # basic message validation rules
        if self.message_type == MCPMessageType.REQUEST:
            if not self.method:
                raise ValueError("Method is required for request")
            if self.result is not None:
                raise ValueError("Request cannot have a result")
        elif self.message_type == MCPMessageType.RESPONSE:
            if self.result is not None and self.error is not None:
                raise ValueError("Response cannot have both result and error")

    def to_dict(self) -> Dict[str, Any]:
        msg = {
            "jsonrpc": "2.0",
            "id": self.message_id,
            "timestamp": self.timestamp
        }

        if self.message_type == MCPMessageType.REQUEST:
            msg.update({"method": self.method.value, "params": self.params})
        elif self.message_type == MCPMessageType.RESPONSE:
            if self.error:
                msg["error"] = self.error
            else:
                msg["result"] = self.result
        elif self.message_type == MCPMessageType.NOTIFICATION:
            msg.update({"method": self.method.value, "params": self.params})
            msg.pop("id", None)
        elif self.message_type == MCPMessageType.ERROR:
            msg["error"] = self.error

        return msg

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'MCPMessage':
        try:
            data = json.loads(json_str)

            if not isinstance(data, dict):
                raise ValueError("Message must be a JSON object")

            # figure out what type of message this is
            if "method" in data and "id" in data:
                mtype = MCPMessageType.REQUEST
                method = MCPMethod(data["method"])
            elif "result" in data and "id" in data:
                mtype = MCPMessageType.RESPONSE
                method = None
            elif "error" in data and "id" in data:
                mtype = MCPMessageType.RESPONSE
                method = None
            elif "method" in data and "id" not in data:
                mtype = MCPMessageType.NOTIFICATION
                method = MCPMethod(data["method"])
            else:
                mtype = MCPMessageType.ERROR
                method = None

            error_data = data.get("error")
            err = error_data if error_data else None

            return cls(
                message_type=mtype,
                method=method,
                params=data.get("params"),
                result=data.get("result"),
                error=err,
                message_id=data.get("id")
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            raise ValueError(f"Invalid JSON: {e}")
        except KeyError as e:
            logger.error(f"Missing field: {e}")
            raise ValueError(f"Malformed message: missing {e}")
        except ValueError as e:
            logger.error(f"Invalid value in message: {e}")
            raise ValueError(f"Invalid message: {e}")

    def is_error(self) -> bool:
       return self.error is not None

    def get_error(self) -> Optional[MCPError]:
        if self.error:
            return MCPError.from_dict(self.error)
        return None

    def __str__(self):
        base = f"MCPMessage({self.message_type.value}, id={self.message_id[:8]}"
        if self.method:
            base += f", method={self.method.value}"
        if self.result:
            base += ", result=..."
        if self.error:
            base += f", error={self.error}"
        return base + ")"


class MCPRequest(MCPMessage):
    # request message
    def __init__(self, method: MCPMethod, params: Optional[Dict[str, Any]] = None):
        super().__init__(
            message_type=MCPMessageType.REQUEST, method=method, params=params or {}
        )


class MCPResponse(MCPMessage):
    # response message
    def __init__(self, request: MCPMessage, result: Optional[Any] = None, error: Optional[MCPError] = None):
        err_dict = error.to_dict() if error else None
        super().__init__(
            message_type=MCPMessageType.RESPONSE,
            result=result,
            error=err_dict,
            message_id=request.message_id
        )

class MCPNotification(MCPMessage):
    # notification message
    def __init__(self, method: MCPMethod, params: Optional[Dict[str, Any]] = None):
        super().__init__(
            message_type=MCPMessageType.NOTIFICATION,
            method=method,
            params=params or {}
        )


def create_error_response(request: MCPMessage, error_code: MCPErrorCode, message: str, data: Any = None) -> MCPResponse:
    # create an error response
    err = MCPError(error_code.value, message, data)
    return MCPResponse(request, error=err)
def create_success_response(request: MCPMessage, result: Any) -> MCPResponse:
    # create a success response
    return MCPResponse(request, result=result)


def validate_method(method_name: str) -> MCPMethod:
    # helper to validate method names
    try:
        return MCPMethod(method_name)
    except ValueError:
        raise ValueError(f"Unsupported method: {method_name}")


if __name__ == "__main__":
    print("Testing MCP protocol")

    # create request
    req = MCPRequest(method=MCPMethod.SEARCH_VEHICLES, params={"marca": "Toyota", "ano_min": 2020})
    print(f"Request: {req}")
    print(f"JSON: {req.to_json()}")
    # success response
    resp = create_success_response(req, {"veiculos": [], "total": 0})
    print(f"Success response {resp}")
    # error response
    err_resp = create_error_response(req, MCPErrorCode.INVALID_PARAMS, "Invalid search params")
    print(f"Error response: {err_resp}")
    # parse JSON
    json_str = req.to_json()
    parsed = MCPMessage.from_json(json_str)
    print(f"Parsed: {parsed}")
    print("MCP protocol tested successfully!")
