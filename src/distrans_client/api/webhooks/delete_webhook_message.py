from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    webhook_id: str,
    token: str,
    message_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/webhooks/{webhook_id}/{token}/messages/{message_id}".format(
            webhook_id=quote(str(webhook_id), safe=""),
            token=quote(str(token), safe=""),
            message_id=quote(str(message_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    webhook_id: str,
    token: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | Error]:
    """Delete a webhook message (token-authenticated, no session)

     Soft-deletes a message previously sent by this webhook. The webhook and message checks are the same
    as `GET`. Emits `message_deleted` and returns 204. Deleting the same message twice returns 404 the
    second time.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        token=token,
        message_id=message_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    webhook_id: str,
    token: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | Error | None:
    """Delete a webhook message (token-authenticated, no session)

     Soft-deletes a message previously sent by this webhook. The webhook and message checks are the same
    as `GET`. Emits `message_deleted` and returns 204. Deleting the same message twice returns 404 the
    second time.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        webhook_id=webhook_id,
        token=token,
        message_id=message_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    webhook_id: str,
    token: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | Error]:
    """Delete a webhook message (token-authenticated, no session)

     Soft-deletes a message previously sent by this webhook. The webhook and message checks are the same
    as `GET`. Emits `message_deleted` and returns 204. Deleting the same message twice returns 404 the
    second time.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        token=token,
        message_id=message_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: str,
    token: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | Error | None:
    """Delete a webhook message (token-authenticated, no session)

     Soft-deletes a message previously sent by this webhook. The webhook and message checks are the same
    as `GET`. Emits `message_deleted` and returns 204. Deleting the same message twice returns 404 the
    second time.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            webhook_id=webhook_id,
            token=token,
            message_id=message_id,
            client=client,
        )
    ).parsed
