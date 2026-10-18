from http import HTTPStatus
from io import BytesIO
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, File, Response


def _get_kwargs(
    guild_id: str,
    *,
    hash_: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["hash"] = hash_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/guilds/{guild_id}/avatar".format(
            guild_id=quote(str(guild_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | File | None:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.content))

        return response_200

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
) -> Response[Error | File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient | Client,
    hash_: str,
) -> Response[Error | File]:
    """Get a guild's avatar image

     Public endpoint, no authentication required. Streams the stored webp (or animated webp) avatar. The
    `hash` query parameter is required and must equal the guild's current `avatar_hash`, otherwise 404.
    The response is immutable for a given hash, so it is safe to cache.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        hash_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | File]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        hash_=hash_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    guild_id: str,
    *,
    client: AuthenticatedClient | Client,
    hash_: str,
) -> Error | File | None:
    """Get a guild's avatar image

     Public endpoint, no authentication required. Streams the stored webp (or animated webp) avatar. The
    `hash` query parameter is required and must equal the guild's current `avatar_hash`, otherwise 404.
    The response is immutable for a given hash, so it is safe to cache.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        hash_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | File
    """

    return sync_detailed(
        guild_id=guild_id,
        client=client,
        hash_=hash_,
    ).parsed


async def asyncio_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient | Client,
    hash_: str,
) -> Response[Error | File]:
    """Get a guild's avatar image

     Public endpoint, no authentication required. Streams the stored webp (or animated webp) avatar. The
    `hash` query parameter is required and must equal the guild's current `avatar_hash`, otherwise 404.
    The response is immutable for a given hash, so it is safe to cache.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        hash_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | File]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        hash_=hash_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    guild_id: str,
    *,
    client: AuthenticatedClient | Client,
    hash_: str,
) -> Error | File | None:
    """Get a guild's avatar image

     Public endpoint, no authentication required. Streams the stored webp (or animated webp) avatar. The
    `hash` query parameter is required and must equal the guild's current `avatar_hash`, otherwise 404.
    The response is immutable for a given hash, so it is safe to cache.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        hash_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | File
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
            hash_=hash_,
        )
    ).parsed
