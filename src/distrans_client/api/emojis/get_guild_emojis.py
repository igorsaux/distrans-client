from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.emoji import Emoji
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    guild_id: str,
    *,
    limit: int | Unset = UNSET,
    after: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["after"] = after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/guilds/{guild_id}/emojis".format(
            guild_id=quote(str(guild_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | list[Emoji] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Emoji.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | list[Emoji]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    after: str | Unset = UNSET,
) -> Response[Error | list[Emoji]]:
    """List a guild's custom emojis

     Requires authentication (any logged-in user). Keyset-paginated by emoji `id` (ascending); `after`
    continues past an id. Only this guild's emojis are returned.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[Emoji]]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        limit=limit,
        after=after,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    after: str | Unset = UNSET,
) -> Error | list[Emoji] | None:
    """List a guild's custom emojis

     Requires authentication (any logged-in user). Keyset-paginated by emoji `id` (ascending); `after`
    continues past an id. Only this guild's emojis are returned.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[Emoji]
    """

    return sync_detailed(
        guild_id=guild_id,
        client=client,
        limit=limit,
        after=after,
    ).parsed


async def asyncio_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    after: str | Unset = UNSET,
) -> Response[Error | list[Emoji]]:
    """List a guild's custom emojis

     Requires authentication (any logged-in user). Keyset-paginated by emoji `id` (ascending); `after`
    continues past an id. Only this guild's emojis are returned.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[Emoji]]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        limit=limit,
        after=after,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = UNSET,
    after: str | Unset = UNSET,
) -> Error | list[Emoji] | None:
    """List a guild's custom emojis

     Requires authentication (any logged-in user). Keyset-paginated by emoji `id` (ascending); `after`
    continues past an id. Only this guild's emojis are returned.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        limit (int | Unset):
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[Emoji]
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
            limit=limit,
            after=after,
        )
    ).parsed
