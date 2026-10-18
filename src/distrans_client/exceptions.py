"""Exceptions raised by the client."""

from __future__ import annotations

from http import HTTPStatus


class DistransError(Exception):
    """Base class for client-side errors."""


class DistransAPIError(DistransError):
    """A documented API error response (``{"message": "..."}``)."""

    def __init__(self, status_code: int | HTTPStatus, message: str) -> None:
        self.status_code = int(status_code)
        self.message = message
        super().__init__(f"{self.status_code}: {message}")


class DistransDownloadError(DistransError):
    """A public file download returned a non-2xx response."""

    def __init__(self, url: str, status_code: int | None = None, message: str = "") -> None:
        self.url = url
        self.status_code = None if status_code is None else int(status_code)
        self.message = message
        detail = url if self.status_code is None else f"{self.status_code} for {url}"
        if message:
            detail = f"{detail}: {message}"
        super().__init__(f"download failed ({detail})")


class DistransGatewayError(DistransError):
    """Base class for WebSocket gateway errors."""


class GatewayConnectionError(DistransGatewayError):
    """The gateway connection could not be established or was lost."""


class GatewayHandshakeError(GatewayConnectionError):
    """The HTTP upgrade was rejected by the server."""

    def __init__(self, status_code: int, message: str = "") -> None:
        self.status_code = int(status_code)
        self.message = message
        detail = f"{self.status_code}" if not message else f"{self.status_code}: {message}"
        super().__init__(f"gateway handshake failed ({detail})")


class GatewayAuthError(DistransGatewayError):
    """The server closed the connection before completing ``identify``/``hello``."""


class GatewayProtocolError(DistransGatewayError):
    """The server sent a frame that does not match the gateway protocol."""


class GatewayClosedError(GatewayConnectionError):
    """The server closed an established gateway connection."""

    def __init__(self, code: int | None, reason: str = "") -> None:
        self.code = code
        self.reason = reason
        detail = "no close code" if code is None else str(code)
        if reason:
            detail = f"{detail}: {reason}"
        super().__init__(f"gateway connection closed ({detail})")
