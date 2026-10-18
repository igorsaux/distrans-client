from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.messages_sync import MessagesSync
from ...types import UNSET, Response, Unset


def _get_kwargs(
    channel_id: str,
    *,
    since: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["since"] = since

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/channels/{channel_id}/messages/sync".format(
            channel_id=quote(str(channel_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | MessagesSync | None:
    if response.status_code == 200:
        response_200 = MessagesSync.from_dict(response.json())

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
) -> Response[Error | MessagesSync]:
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
    since: int | Unset = UNSET,
) -> Response[Error | MessagesSync]:
    """Changed channel messages since a cursor

     Returns only the ids of present messages changed since `since` (upserts). Requires `read_messages`
    on the channel. A soft-deleted message stays present and is therefore listed; the client drops it
    after fetching it and observing `deleted_at`. Hard deletions are not listed.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MessagesSync]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        since=since,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Error | MessagesSync | None:
    """Changed channel messages since a cursor

     Returns only the ids of present messages changed since `since` (upserts). Requires `read_messages`
    on the channel. A soft-deleted message stays present and is therefore listed; the client drops it
    after fetching it and observing `deleted_at`. Hard deletions are not listed.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MessagesSync
    """

    return sync_detailed(
        channel_id=channel_id,
        client=client,
        since=since,
    ).parsed


async def asyncio_detailed(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Response[Error | MessagesSync]:
    """Changed channel messages since a cursor

     Returns only the ids of present messages changed since `since` (upserts). Requires `read_messages`
    on the channel. A soft-deleted message stays present and is therefore listed; the client drops it
    after fetching it and observing `deleted_at`. Hard deletions are not listed.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MessagesSync]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        since=since,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Error | MessagesSync | None:
    """Changed channel messages since a cursor

     Returns only the ids of present messages changed since `since` (upserts). Requires `read_messages`
    on the channel. A soft-deleted message stays present and is therefore listed; the client drops it
    after fetching it and observing `deleted_at`. Hard deletions are not listed.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MessagesSync
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
            since=since,
        )
    ).parsed
