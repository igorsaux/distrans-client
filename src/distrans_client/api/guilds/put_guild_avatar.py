from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.put_guild_avatar_response_200 import PutGuildAvatarResponse200
from ...types import File, Response


def _get_kwargs(
    guild_id: str,
    *,
    body: File,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/guilds/{guild_id}/avatar".format(
            guild_id=quote(str(guild_id), safe=""),
        ),
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | PutGuildAvatarResponse200 | None:
    if response.status_code == 200:
        response_200 = PutGuildAvatarResponse200.from_dict(response.json())

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
) -> Response[Error | PutGuildAvatarResponse200]:
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
) -> Response[Error | PutGuildAvatarResponse200]:
    """Set a guild's avatar

     Requires `guild_modify` on the guild. Uploads a static or animated image, within
    `media.avatar.max_dimensions`, `media.avatar.max_input_bytes` and the `media.avatar` animation caps.
    The `Content-Type` must be `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg`;
    unsupported types are rejected with `415`. Images are re-encoded to WebP (animations to animated
    WebP); the response contains the stored `avatar_hash` (XXHash64, 16 lowercase hex chars). The body
    must be non-empty. Use `DELETE` to clear the avatar; a PUT never clears it. Every successful change
    dispatches a `guild_updated` gateway event.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PutGuildAvatarResponse200]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        body=body,
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
) -> Error | PutGuildAvatarResponse200 | None:
    """Set a guild's avatar

     Requires `guild_modify` on the guild. Uploads a static or animated image, within
    `media.avatar.max_dimensions`, `media.avatar.max_input_bytes` and the `media.avatar` animation caps.
    The `Content-Type` must be `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg`;
    unsupported types are rejected with `415`. Images are re-encoded to WebP (animations to animated
    WebP); the response contains the stored `avatar_hash` (XXHash64, 16 lowercase hex chars). The body
    must be non-empty. Use `DELETE` to clear the avatar; a PUT never clears it. Every successful change
    dispatches a `guild_updated` gateway event.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PutGuildAvatarResponse200
    """

    return sync_detailed(
        guild_id=guild_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Response[Error | PutGuildAvatarResponse200]:
    """Set a guild's avatar

     Requires `guild_modify` on the guild. Uploads a static or animated image, within
    `media.avatar.max_dimensions`, `media.avatar.max_input_bytes` and the `media.avatar` animation caps.
    The `Content-Type` must be `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg`;
    unsupported types are rejected with `415`. Images are re-encoded to WebP (animations to animated
    WebP); the response contains the stored `avatar_hash` (XXHash64, 16 lowercase hex chars). The body
    must be non-empty. Use `DELETE` to clear the avatar; a PUT never clears it. Every successful change
    dispatches a `guild_updated` gateway event.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PutGuildAvatarResponse200]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Error | PutGuildAvatarResponse200 | None:
    """Set a guild's avatar

     Requires `guild_modify` on the guild. Uploads a static or animated image, within
    `media.avatar.max_dimensions`, `media.avatar.max_input_bytes` and the `media.avatar` animation caps.
    The `Content-Type` must be `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg`;
    unsupported types are rejected with `415`. Images are re-encoded to WebP (animations to animated
    WebP); the response contains the stored `avatar_hash` (XXHash64, 16 lowercase hex chars). The body
    must be non-empty. Use `DELETE` to clear the avatar; a PUT never clears it. Every successful change
    dispatches a `guild_updated` gateway event.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PutGuildAvatarResponse200
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
            body=body,
        )
    ).parsed
