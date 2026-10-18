from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.guild_notification_settings import GuildNotificationSettings
from ...types import Response


def _get_kwargs(
    guild_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/users/@me/guilds/{guild_id}/notifications".format(
            guild_id=quote(str(guild_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GuildNotificationSettings | None:
    if response.status_code == 200:
        response_200 = GuildNotificationSettings.from_dict(response.json())

        return response_200

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
) -> Response[Error | GuildNotificationSettings]:
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
) -> Response[Error | GuildNotificationSettings]:
    """Get the current user's guild notification settings

     Returns the caller's notification settings for the guild. These are personal settings: they are
    gated only by authentication, not by any guild permission. When the user has never changed them the
    defaults are returned (`level` = `all_messages`, `suppress_everyone` = false, `suppress_roles` =
    false, `push` = true), never 404. No gateway event is dispatched. The settings drive the
    notification fan-out: `level` decides whether the guild's messages produce a browser push
    (`all_messages` always, `only_mentions` only for a non-suppressed direct/role/`@everyone` mention,
    `nothing` never), the `suppress_*` flags gate the mention kinds only, and `push` disables pushes for
    the whole guild.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GuildNotificationSettings]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    guild_id: str,
    *,
    client: AuthenticatedClient,
) -> Error | GuildNotificationSettings | None:
    """Get the current user's guild notification settings

     Returns the caller's notification settings for the guild. These are personal settings: they are
    gated only by authentication, not by any guild permission. When the user has never changed them the
    defaults are returned (`level` = `all_messages`, `suppress_everyone` = false, `suppress_roles` =
    false, `push` = true), never 404. No gateway event is dispatched. The settings drive the
    notification fan-out: `level` decides whether the guild's messages produce a browser push
    (`all_messages` always, `only_mentions` only for a non-suppressed direct/role/`@everyone` mention,
    `nothing` never), the `suppress_*` flags gate the mention kinds only, and `push` disables pushes for
    the whole guild.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GuildNotificationSettings
    """

    return sync_detailed(
        guild_id=guild_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Error | GuildNotificationSettings]:
    """Get the current user's guild notification settings

     Returns the caller's notification settings for the guild. These are personal settings: they are
    gated only by authentication, not by any guild permission. When the user has never changed them the
    defaults are returned (`level` = `all_messages`, `suppress_everyone` = false, `suppress_roles` =
    false, `push` = true), never 404. No gateway event is dispatched. The settings drive the
    notification fan-out: `level` decides whether the guild's messages produce a browser push
    (`all_messages` always, `only_mentions` only for a non-suppressed direct/role/`@everyone` mention,
    `nothing` never), the `suppress_*` flags gate the mention kinds only, and `push` disables pushes for
    the whole guild.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GuildNotificationSettings]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    guild_id: str,
    *,
    client: AuthenticatedClient,
) -> Error | GuildNotificationSettings | None:
    """Get the current user's guild notification settings

     Returns the caller's notification settings for the guild. These are personal settings: they are
    gated only by authentication, not by any guild permission. When the user has never changed them the
    defaults are returned (`level` = `all_messages`, `suppress_everyone` = false, `suppress_roles` =
    false, `push` = true), never 404. No gateway event is dispatched. The settings drive the
    notification fan-out: `level` decides whether the guild's messages produce a browser push
    (`all_messages` always, `only_mentions` only for a non-suppressed direct/role/`@everyone` mention,
    `nothing` never), the `suppress_*` flags gate the mention kinds only, and `push` disables pushes for
    the whole guild.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GuildNotificationSettings
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
        )
    ).parsed
