from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel_notification_settings import ChannelNotificationSettings
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    channel_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/users/@me/channels/{channel_id}/notifications".format(
            channel_id=quote(str(channel_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ChannelNotificationSettings | Error | None:
    if response.status_code == 200:
        response_200 = ChannelNotificationSettings.from_dict(response.json())

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
) -> Response[ChannelNotificationSettings | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    channel_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ChannelNotificationSettings | Error]:
    """Get the current user's channel notification settings

     Returns the caller's notification settings for the channel (text channel or category). These are
    personal settings: they are gated only by authentication, not by any channel permission. When the
    user has never changed them the default `level` (`inherit`) is returned, never 404. An unknown
    channel is 404 "Channel not found". Alongside the stored `level` the response carries the resolved
    `effective_level`, following the inheritance chain channel -> parent category -> guild: `inherit` on
    a text channel falls back to its parent category's level (which may itself inherit from the guild),
    and a category (no parent) falls back to the guild. `effective_level` is never `inherit`. No gateway
    event is dispatched. The level drives the notification fan-out for the channel (`all_messages`
    always, `only_mentions` only for a non-suppressed mention, `nothing` never).

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChannelNotificationSettings | Error]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    channel_id: str,
    *,
    client: AuthenticatedClient,
) -> ChannelNotificationSettings | Error | None:
    """Get the current user's channel notification settings

     Returns the caller's notification settings for the channel (text channel or category). These are
    personal settings: they are gated only by authentication, not by any channel permission. When the
    user has never changed them the default `level` (`inherit`) is returned, never 404. An unknown
    channel is 404 "Channel not found". Alongside the stored `level` the response carries the resolved
    `effective_level`, following the inheritance chain channel -> parent category -> guild: `inherit` on
    a text channel falls back to its parent category's level (which may itself inherit from the guild),
    and a category (no parent) falls back to the guild. `effective_level` is never `inherit`. No gateway
    event is dispatched. The level drives the notification fan-out for the channel (`all_messages`
    always, `only_mentions` only for a non-suppressed mention, `nothing` never).

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChannelNotificationSettings | Error
    """

    return sync_detailed(
        channel_id=channel_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    channel_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ChannelNotificationSettings | Error]:
    """Get the current user's channel notification settings

     Returns the caller's notification settings for the channel (text channel or category). These are
    personal settings: they are gated only by authentication, not by any channel permission. When the
    user has never changed them the default `level` (`inherit`) is returned, never 404. An unknown
    channel is 404 "Channel not found". Alongside the stored `level` the response carries the resolved
    `effective_level`, following the inheritance chain channel -> parent category -> guild: `inherit` on
    a text channel falls back to its parent category's level (which may itself inherit from the guild),
    and a category (no parent) falls back to the guild. `effective_level` is never `inherit`. No gateway
    event is dispatched. The level drives the notification fan-out for the channel (`all_messages`
    always, `only_mentions` only for a non-suppressed mention, `nothing` never).

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChannelNotificationSettings | Error]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    channel_id: str,
    *,
    client: AuthenticatedClient,
) -> ChannelNotificationSettings | Error | None:
    """Get the current user's channel notification settings

     Returns the caller's notification settings for the channel (text channel or category). These are
    personal settings: they are gated only by authentication, not by any channel permission. When the
    user has never changed them the default `level` (`inherit`) is returned, never 404. An unknown
    channel is 404 "Channel not found". Alongside the stored `level` the response carries the resolved
    `effective_level`, following the inheritance chain channel -> parent category -> guild: `inherit` on
    a text channel falls back to its parent category's level (which may itself inherit from the guild),
    and a category (no parent) falls back to the guild. `effective_level` is never `inherit`. No gateway
    event is dispatched. The level drives the notification fan-out for the channel (`all_messages`
    always, `only_mentions` only for a non-suppressed mention, `nothing` never).

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChannelNotificationSettings | Error
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
        )
    ).parsed
