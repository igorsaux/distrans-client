from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    message_id: str,
    *,
    emoji_id: str | Unset = UNSET,
    unicode_emoji: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["emoji_id"] = emoji_id

    params["unicode_emoji"] = unicode_emoji

    params["limit"] = limit

    params["after"] = after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/messages/{message_id}/reactions/users".format(
            message_id=quote(str(message_id), safe=""),
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
    message_id: str,
    *,
    client: AuthenticatedClient,
    emoji_id: str | Unset = UNSET,
    unicode_emoji: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> Response[Error | list[str]]:
    """List the users who reacted with one emoji (read_messages required)

     Returns the ids of the users who reacted to the message with exactly the requested emoji, ascending
    by user id. Soft-deleted users are excluded, so the array length matches the corresponding `count`
    of `GET /messages/{message_id}/reactions`. Returns an empty array (not 404) when nobody reacted with
    that emoji.

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        emoji_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        unicode_emoji (str | Unset):
        limit (int | Unset):  Default: 50.
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[str]]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        emoji_id=emoji_id,
        unicode_emoji=unicode_emoji,
        limit=limit,
        after=after,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    message_id: str,
    *,
    client: AuthenticatedClient,
    emoji_id: str | Unset = UNSET,
    unicode_emoji: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> Error | list[str] | None:
    """List the users who reacted with one emoji (read_messages required)

     Returns the ids of the users who reacted to the message with exactly the requested emoji, ascending
    by user id. Soft-deleted users are excluded, so the array length matches the corresponding `count`
    of `GET /messages/{message_id}/reactions`. Returns an empty array (not 404) when nobody reacted with
    that emoji.

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        emoji_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        unicode_emoji (str | Unset):
        limit (int | Unset):  Default: 50.
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[str]
    """

    return sync_detailed(
        message_id=message_id,
        client=client,
        emoji_id=emoji_id,
        unicode_emoji=unicode_emoji,
        limit=limit,
        after=after,
    ).parsed


async def asyncio_detailed(
    message_id: str,
    *,
    client: AuthenticatedClient,
    emoji_id: str | Unset = UNSET,
    unicode_emoji: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> Response[Error | list[str]]:
    """List the users who reacted with one emoji (read_messages required)

     Returns the ids of the users who reacted to the message with exactly the requested emoji, ascending
    by user id. Soft-deleted users are excluded, so the array length matches the corresponding `count`
    of `GET /messages/{message_id}/reactions`. Returns an empty array (not 404) when nobody reacted with
    that emoji.

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        emoji_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        unicode_emoji (str | Unset):
        limit (int | Unset):  Default: 50.
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[str]]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        emoji_id=emoji_id,
        unicode_emoji=unicode_emoji,
        limit=limit,
        after=after,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    message_id: str,
    *,
    client: AuthenticatedClient,
    emoji_id: str | Unset = UNSET,
    unicode_emoji: str | Unset = UNSET,
    limit: int | Unset = 50,
    after: str | Unset = UNSET,
) -> Error | list[str] | None:
    """List the users who reacted with one emoji (read_messages required)

     Returns the ids of the users who reacted to the message with exactly the requested emoji, ascending
    by user id. Soft-deleted users are excluded, so the array length matches the corresponding `count`
    of `GET /messages/{message_id}/reactions`. Returns an empty array (not 404) when nobody reacted with
    that emoji.

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        emoji_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        unicode_emoji (str | Unset):
        limit (int | Unset):  Default: 50.
        after (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[str]
    """

    return (
        await asyncio_detailed(
            message_id=message_id,
            client=client,
            emoji_id=emoji_id,
            unicode_emoji=unicode_emoji,
            limit=limit,
            after=after,
        )
    ).parsed
