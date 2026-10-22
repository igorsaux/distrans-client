from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.message import Message
from ...types import UNSET, Response, Unset


def _get_kwargs(
    channel_id: str,
    *,
    limit: int | Unset = UNSET,
    before: str | Unset = UNSET,
    after: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["before"] = before

    params["after"] = after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/channels/{channel_id}/pins/messages".format(
            channel_id=quote(str(channel_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | list[Message] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Message.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | list[Message]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    before: str | Unset = UNSET,
    after: str | Unset = UNSET,
) -> Response[Error | list[Message]]:
    """List full pinned messages (keyset pagination)

     Returns the channel's pinned, non-deleted messages as full `Message` objects, ascending by message
    id. Unpinned and soft-deleted messages are excluded. `before` and `after` are mutually exclusive.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        before (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[Message]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        limit=limit,
        before=before,
        after=after,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    before: str | Unset = UNSET,
    after: str | Unset = UNSET,
) -> Error | list[Message] | None:
    """List full pinned messages (keyset pagination)

     Returns the channel's pinned, non-deleted messages as full `Message` objects, ascending by message
    id. Unpinned and soft-deleted messages are excluded. `before` and `after` are mutually exclusive.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        before (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[Message]
    """

    return sync_detailed(
        channel_id=channel_id,
        client=client,
        limit=limit,
        before=before,
        after=after,
    ).parsed


async def asyncio_detailed(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    before: str | Unset = UNSET,
    after: str | Unset = UNSET,
) -> Response[Error | list[Message]]:
    """List full pinned messages (keyset pagination)

     Returns the channel's pinned, non-deleted messages as full `Message` objects, ascending by message
    id. Unpinned and soft-deleted messages are excluded. `before` and `after` are mutually exclusive.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        before (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[Message]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        limit=limit,
        before=before,
        after=after,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    before: str | Unset = UNSET,
    after: str | Unset = UNSET,
) -> Error | list[Message] | None:
    """List full pinned messages (keyset pagination)

     Returns the channel's pinned, non-deleted messages as full `Message` objects, ascending by message
    id. Unpinned and soft-deleted messages are excluded. `before` and `after` are mutually exclusive.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        before (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[Message]
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
            limit=limit,
            before=before,
            after=after,
        )
    ).parsed
