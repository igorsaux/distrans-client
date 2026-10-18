"""Internal gateway helpers."""

from __future__ import annotations

from websockets.exceptions import ConnectionClosed

__all__ = ["close_details"]


def close_details(exc: ConnectionClosed) -> tuple[int | None, str]:
    """Return the received close code and reason without deprecated properties."""
    frame = exc.rcvd
    if frame is None:
        return None, ""
    return frame.code, frame.reason or ""
