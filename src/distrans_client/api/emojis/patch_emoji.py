from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.patch_emoji_body import PatchEmojiBody
from ...types import Response


def _get_kwargs(
    emoji_id: str,
    *,
    body: PatchEmojiBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/emojis/{emoji_id}".format(
            emoji_id=quote(str(emoji_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

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
    emoji_id: str,
    *,
    client: AuthenticatedClient,
    body: PatchEmojiBody,
) -> Response[Any | Error]:
    """Rename a custom emoji

     Requires `modify_emoji` on the emoji's guild. The body is a JSON object with a single `name` field;
    the name is not nullable. A duplicate name in the same guild is rejected. Dispatches an
    `emoji_updated` gateway event.

    Args:
        emoji_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchEmojiBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: PatchEmojiBody,
) -> Any | Error | None:
    """Rename a custom emoji

     Requires `modify_emoji` on the emoji's guild. The body is a JSON object with a single `name` field;
    the name is not nullable. A duplicate name in the same guild is rejected. Dispatches an
    `emoji_updated` gateway event.

    Args:
        emoji_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchEmojiBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
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
    body: PatchEmojiBody,
) -> Response[Any | Error]:
    """Rename a custom emoji

     Requires `modify_emoji` on the emoji's guild. The body is a JSON object with a single `name` field;
    the name is not nullable. A duplicate name in the same guild is rejected. Dispatches an
    `emoji_updated` gateway event.

    Args:
        emoji_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchEmojiBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: PatchEmojiBody,
) -> Any | Error | None:
    """Rename a custom emoji

     Requires `modify_emoji` on the emoji's guild. The body is a JSON object with a single `name` field;
    the name is not nullable. A duplicate name in the same guild is rejected. Dispatches an
    `emoji_updated` gateway event.

    Args:
        emoji_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchEmojiBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            emoji_id=emoji_id,
            client=client,
            body=body,
        )
    ).parsed
