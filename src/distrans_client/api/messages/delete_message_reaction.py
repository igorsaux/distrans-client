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
    user_id: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["emoji_id"] = emoji_id

    params["unicode_emoji"] = unicode_emoji

    params["user_id"] = user_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/messages/{message_id}/reactions".format(
            message_id=quote(str(message_id), safe=""),
        ),
        "params": params,
    }

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
    message_id: str,
    *,
    client: AuthenticatedClient,
    emoji_id: str | Unset = UNSET,
    unicode_emoji: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
) -> Response[Any | Error]:
    """Remove a reaction (own freely; another user's with delete_reactions and a strictly higher role)

     Removes the caller's reaction with the given emoji; with no emoji parameter, removes all of the
    caller's reactions on the message. With `user_id`, removes that user's reaction instead, which
    requires `delete_reactions` on the channel and being strictly higher in the role hierarchy than the
    target. Idempotent (a missing reaction is still 204).

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        emoji_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        unicode_emoji (str | Unset):
        user_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        emoji_id=emoji_id,
        unicode_emoji=unicode_emoji,
        user_id=user_id,
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
    user_id: str | Unset = UNSET,
) -> Any | Error | None:
    """Remove a reaction (own freely; another user's with delete_reactions and a strictly higher role)

     Removes the caller's reaction with the given emoji; with no emoji parameter, removes all of the
    caller's reactions on the message. With `user_id`, removes that user's reaction instead, which
    requires `delete_reactions` on the channel and being strictly higher in the role hierarchy than the
    target. Idempotent (a missing reaction is still 204).

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        emoji_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        unicode_emoji (str | Unset):
        user_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        message_id=message_id,
        client=client,
        emoji_id=emoji_id,
        unicode_emoji=unicode_emoji,
        user_id=user_id,
    ).parsed


async def asyncio_detailed(
    message_id: str,
    *,
    client: AuthenticatedClient,
    emoji_id: str | Unset = UNSET,
    unicode_emoji: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
) -> Response[Any | Error]:
    """Remove a reaction (own freely; another user's with delete_reactions and a strictly higher role)

     Removes the caller's reaction with the given emoji; with no emoji parameter, removes all of the
    caller's reactions on the message. With `user_id`, removes that user's reaction instead, which
    requires `delete_reactions` on the channel and being strictly higher in the role hierarchy than the
    target. Idempotent (a missing reaction is still 204).

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        emoji_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        unicode_emoji (str | Unset):
        user_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        emoji_id=emoji_id,
        unicode_emoji=unicode_emoji,
        user_id=user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    message_id: str,
    *,
    client: AuthenticatedClient,
    emoji_id: str | Unset = UNSET,
    unicode_emoji: str | Unset = UNSET,
    user_id: str | Unset = UNSET,
) -> Any | Error | None:
    """Remove a reaction (own freely; another user's with delete_reactions and a strictly higher role)

     Removes the caller's reaction with the given emoji; with no emoji parameter, removes all of the
    caller's reactions on the message. With `user_id`, removes that user's reaction instead, which
    requires `delete_reactions` on the channel and being strictly higher in the role hierarchy than the
    target. Idempotent (a missing reaction is still 204).

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        emoji_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        unicode_emoji (str | Unset):
        user_id (str | Unset): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            message_id=message_id,
            client=client,
            emoji_id=emoji_id,
            unicode_emoji=unicode_emoji,
            user_id=user_id,
        )
    ).parsed
