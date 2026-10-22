from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
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
        "url": "/channels/{channel_id}/pins".format(
            channel_id=quote(str(channel_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | list[str] | None:
    if response.status_code == 200:
        response_200 = cast(list[str], response.json())

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
) -> Response[Error | list[str]]:
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
) -> Response[Error | list[str]]:
    """List pinned message ids (keyset pagination)

     Returns the ids (decimal strings, ascending) of the channel's pinned non-deleted messages. `before`
    and `after` are mutually exclusive. Use `/channels/{channel_id}/pins/messages` to fetch the full
    pinned messages in one response.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        before (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[str]]
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
) -> Error | list[str] | None:
    """List pinned message ids (keyset pagination)

     Returns the ids (decimal strings, ascending) of the channel's pinned non-deleted messages. `before`
    and `after` are mutually exclusive. Use `/channels/{channel_id}/pins/messages` to fetch the full
    pinned messages in one response.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        before (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[str]
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
) -> Response[Error | list[str]]:
    """List pinned message ids (keyset pagination)

     Returns the ids (decimal strings, ascending) of the channel's pinned non-deleted messages. `before`
    and `after` are mutually exclusive. Use `/channels/{channel_id}/pins/messages` to fetch the full
    pinned messages in one response.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        before (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[str]]
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
) -> Error | list[str] | None:
    """List pinned message ids (keyset pagination)

     Returns the ids (decimal strings, ascending) of the channel's pinned non-deleted messages. `before`
    and `after` are mutually exclusive. Use `/channels/{channel_id}/pins/messages` to fetch the full
    pinned messages in one response.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        before (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[str]
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
