from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.guild_sync import GuildSync
from ...types import UNSET, Response, Unset


def _get_kwargs(
    guild_id: str,
    *,
    since: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["since"] = since

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/guilds/{guild_id}/sync".format(
            guild_id=quote(str(guild_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GuildSync | None:
    if response.status_code == 200:
        response_200 = GuildSync.from_dict(response.json())

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
) -> Response[Error | GuildSync]:
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
    since: int | Unset = UNSET,
) -> Response[Error | GuildSync]:
    """Changed guild entities since a cursor

     Per-guild changed-since delta. Every field is an array of ids of present rows whose `updated_at` is
    newer than `since` (upserts); entity bodies are never returned. `overwrites` carry their
    `channel_id` because `(target_type, target_id)` is not unique within a guild. `member_roles` is the
    caller's complete current role-id set (not filtered by `since`), because grant/revoke hard-delete
    the row and a delta cannot express revocation. Hard deletions are not listed; the client reconciles
    them with a periodic full refetch or gateway events. Metadata is readable by any authenticated user.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GuildSync]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        since=since,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Error | GuildSync | None:
    """Changed guild entities since a cursor

     Per-guild changed-since delta. Every field is an array of ids of present rows whose `updated_at` is
    newer than `since` (upserts); entity bodies are never returned. `overwrites` carry their
    `channel_id` because `(target_type, target_id)` is not unique within a guild. `member_roles` is the
    caller's complete current role-id set (not filtered by `since`), because grant/revoke hard-delete
    the row and a delta cannot express revocation. Hard deletions are not listed; the client reconciles
    them with a periodic full refetch or gateway events. Metadata is readable by any authenticated user.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GuildSync
    """

    return sync_detailed(
        guild_id=guild_id,
        client=client,
        since=since,
    ).parsed


async def asyncio_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Response[Error | GuildSync]:
    """Changed guild entities since a cursor

     Per-guild changed-since delta. Every field is an array of ids of present rows whose `updated_at` is
    newer than `since` (upserts); entity bodies are never returned. `overwrites` carry their
    `channel_id` because `(target_type, target_id)` is not unique within a guild. `member_roles` is the
    caller's complete current role-id set (not filtered by `since`), because grant/revoke hard-delete
    the row and a delta cannot express revocation. Hard deletions are not listed; the client reconciles
    them with a periodic full refetch or gateway events. Metadata is readable by any authenticated user.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GuildSync]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        since=since,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Error | GuildSync | None:
    """Changed guild entities since a cursor

     Per-guild changed-since delta. Every field is an array of ids of present rows whose `updated_at` is
    newer than `since` (upserts); entity bodies are never returned. `overwrites` carry their
    `channel_id` because `(target_type, target_id)` is not unique within a guild. `member_roles` is the
    caller's complete current role-id set (not filtered by `since`), because grant/revoke hard-delete
    the row and a delta cannot express revocation. Hard deletions are not listed; the client reconciles
    them with a periodic full refetch or gateway events. Metadata is readable by any authenticated user.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GuildSync
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
            since=since,
        )
    ).parsed
