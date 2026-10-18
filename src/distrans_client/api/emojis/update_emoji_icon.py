from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.update_emoji_icon_response_200 import UpdateEmojiIconResponse200
from ...types import File, Response


def _get_kwargs(
    emoji_id: str,
    *,
    body: File,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/emojis/{emoji_id}/icon".format(
            emoji_id=quote(str(emoji_id), safe=""),
        ),
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UpdateEmojiIconResponse200 | None:
    if response.status_code == 200:
        response_200 = UpdateEmojiIconResponse200.from_dict(response.json())

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
) -> Response[Error | UpdateEmojiIconResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    emoji_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Response[Error | UpdateEmojiIconResponse200]:
    """Update a custom emoji's icon

     Requires `modify_emoji` on the emoji's guild. The body is a raw image with `Content-Type`
    `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg` (an unsupported type is `415`)
    and must be within the `media.emoji` caps; it is re-encoded to WebP (animations to animated WebP),
    hashed and stored, replacing the existing icon. On success the new `icon_hash` is returned so the
    client can fetch the image from `GET /emojis/{emoji_id}/icon?hash={icon_hash}`. Dispatches an
    `emoji_updated` gateway event.

    Args:
        emoji_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateEmojiIconResponse200]
    """

    kwargs = _get_kwargs(
        emoji_id=emoji_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    emoji_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Error | UpdateEmojiIconResponse200 | None:
    """Update a custom emoji's icon

     Requires `modify_emoji` on the emoji's guild. The body is a raw image with `Content-Type`
    `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg` (an unsupported type is `415`)
    and must be within the `media.emoji` caps; it is re-encoded to WebP (animations to animated WebP),
    hashed and stored, replacing the existing icon. On success the new `icon_hash` is returned so the
    client can fetch the image from `GET /emojis/{emoji_id}/icon?hash={icon_hash}`. Dispatches an
    `emoji_updated` gateway event.

    Args:
        emoji_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateEmojiIconResponse200
    """

    return sync_detailed(
        emoji_id=emoji_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    emoji_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Response[Error | UpdateEmojiIconResponse200]:
    """Update a custom emoji's icon

     Requires `modify_emoji` on the emoji's guild. The body is a raw image with `Content-Type`
    `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg` (an unsupported type is `415`)
    and must be within the `media.emoji` caps; it is re-encoded to WebP (animations to animated WebP),
    hashed and stored, replacing the existing icon. On success the new `icon_hash` is returned so the
    client can fetch the image from `GET /emojis/{emoji_id}/icon?hash={icon_hash}`. Dispatches an
    `emoji_updated` gateway event.

    Args:
        emoji_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateEmojiIconResponse200]
    """

    kwargs = _get_kwargs(
        emoji_id=emoji_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    emoji_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Error | UpdateEmojiIconResponse200 | None:
    """Update a custom emoji's icon

     Requires `modify_emoji` on the emoji's guild. The body is a raw image with `Content-Type`
    `image/webp`, `image/gif`, `image/png`, `image/jpeg` or `image/jpg` (an unsupported type is `415`)
    and must be within the `media.emoji` caps; it is re-encoded to WebP (animations to animated WebP),
    hashed and stored, replacing the existing icon. On success the new `icon_hash` is returned so the
    client can fetch the image from `GET /emojis/{emoji_id}/icon?hash={icon_hash}`. Dispatches an
    `emoji_updated` gateway event.

    Args:
        emoji_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateEmojiIconResponse200
    """

    return (
        await asyncio_detailed(
            emoji_id=emoji_id,
            client=client,
            body=body,
        )
    ).parsed
