from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.emoji import Emoji
from ...models.error import Error
from ...types import UNSET, File, Response


def _get_kwargs(
    guild_id: str,
    *,
    body: File,
    name: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/guilds/{guild_id}/emojis".format(
            guild_id=quote(str(guild_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Emoji | Error | None:
    if response.status_code == 201:
        response_201 = Emoji.from_dict(response.json())

        return response_201

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Emoji | Error]:
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
    body: File,
    name: str,
) -> Response[Emoji | Error]:
    """Create a custom emoji

     Requires `create_emoji` on the guild. The name travels in the query string (the server does not
    percent-decode query values, so clients must send the name bytes verbatim) and the body is a raw
    image with `Content-Type` `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg` (an
    unsupported type is `415`). The upload must be within the `media.emoji` caps; it is re-encoded to
    WebP (animations to animated WebP) and stored. The guild may hold at most `api.guilds.max_emojis`
    emojis. Names are unique per guild. Dispatches an `emoji_created` gateway event.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        name (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Emoji | Error]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        body=body,
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    name: str,
) -> Emoji | Error | None:
    """Create a custom emoji

     Requires `create_emoji` on the guild. The name travels in the query string (the server does not
    percent-decode query values, so clients must send the name bytes verbatim) and the body is a raw
    image with `Content-Type` `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg` (an
    unsupported type is `415`). The upload must be within the `media.emoji` caps; it is re-encoded to
    WebP (animations to animated WebP) and stored. The guild may hold at most `api.guilds.max_emojis`
    emojis. Names are unique per guild. Dispatches an `emoji_created` gateway event.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        name (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Emoji | Error
    """

    return sync_detailed(
        guild_id=guild_id,
        client=client,
        body=body,
        name=name,
    ).parsed


async def asyncio_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    name: str,
) -> Response[Emoji | Error]:
    """Create a custom emoji

     Requires `create_emoji` on the guild. The name travels in the query string (the server does not
    percent-decode query values, so clients must send the name bytes verbatim) and the body is a raw
    image with `Content-Type` `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg` (an
    unsupported type is `415`). The upload must be within the `media.emoji` caps; it is re-encoded to
    WebP (animations to animated WebP) and stored. The guild may hold at most `api.guilds.max_emojis`
    emojis. Names are unique per guild. Dispatches an `emoji_created` gateway event.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        name (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Emoji | Error]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        body=body,
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    name: str,
) -> Emoji | Error | None:
    """Create a custom emoji

     Requires `create_emoji` on the guild. The name travels in the query string (the server does not
    percent-decode query values, so clients must send the name bytes verbatim) and the body is a raw
    image with `Content-Type` `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg` (an
    unsupported type is `415`). The upload must be within the `media.emoji` caps; it is re-encoded to
    WebP (animations to animated WebP) and stored. The guild may hold at most `api.guilds.max_emojis`
    emojis. Names are unique per guild. Dispatches an `emoji_created` gateway event.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        name (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Emoji | Error
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
            body=body,
            name=name,
        )
    ).parsed
