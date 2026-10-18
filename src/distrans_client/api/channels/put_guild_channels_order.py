from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.put_guild_channels_order_body import PutGuildChannelsOrderBody
from ...types import Response


def _get_kwargs(
    guild_id: str,
    *,
    body: PutGuildChannelsOrderBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/guilds/{guild_id}/channels/order".format(
            guild_id=quote(str(guild_id), safe=""),
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
    guild_id: str,
    *,
    client: AuthenticatedClient,
    body: PutGuildChannelsOrderBody,
) -> Response[Any | Error]:
    """Reorder a guild's channels within one parent (modify_channels required)

     Sets the order of the children of one scope in a single atomic request.
    `parent_id` selects the scope: `null`/absent means the root (categories
    and root channels), otherwise a category id. `channels` must list
    **exactly** the channels whose parent is that scope, each once, in the
    desired order; positions are then assigned densely as `0..K-1`.

    Every channel whose index changes must be modifiable by the caller
    (`modify_channels` computed on that channel); otherwise the request is a
    403. Channels whose index is unchanged are pinned and need no rights.
    Only ordering within one scope is affected — channels are not reparented.

    On success the server emits a `channels_reordered` gateway event
    carrying only `guild_id`; clients refetch
    `GET /guilds/{guild_id}/channels`.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutGuildChannelsOrderBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: PutGuildChannelsOrderBody,
) -> Any | Error | None:
    """Reorder a guild's channels within one parent (modify_channels required)

     Sets the order of the children of one scope in a single atomic request.
    `parent_id` selects the scope: `null`/absent means the root (categories
    and root channels), otherwise a category id. `channels` must list
    **exactly** the channels whose parent is that scope, each once, in the
    desired order; positions are then assigned densely as `0..K-1`.

    Every channel whose index changes must be modifiable by the caller
    (`modify_channels` computed on that channel); otherwise the request is a
    403. Channels whose index is unchanged are pinned and need no rights.
    Only ordering within one scope is affected — channels are not reparented.

    On success the server emits a `channels_reordered` gateway event
    carrying only `guild_id`; clients refetch
    `GET /guilds/{guild_id}/channels`.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutGuildChannelsOrderBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
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
    body: PutGuildChannelsOrderBody,
) -> Response[Any | Error]:
    """Reorder a guild's channels within one parent (modify_channels required)

     Sets the order of the children of one scope in a single atomic request.
    `parent_id` selects the scope: `null`/absent means the root (categories
    and root channels), otherwise a category id. `channels` must list
    **exactly** the channels whose parent is that scope, each once, in the
    desired order; positions are then assigned densely as `0..K-1`.

    Every channel whose index changes must be modifiable by the caller
    (`modify_channels` computed on that channel); otherwise the request is a
    403. Channels whose index is unchanged are pinned and need no rights.
    Only ordering within one scope is affected — channels are not reparented.

    On success the server emits a `channels_reordered` gateway event
    carrying only `guild_id`; clients refetch
    `GET /guilds/{guild_id}/channels`.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutGuildChannelsOrderBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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
    body: PutGuildChannelsOrderBody,
) -> Any | Error | None:
    """Reorder a guild's channels within one parent (modify_channels required)

     Sets the order of the children of one scope in a single atomic request.
    `parent_id` selects the scope: `null`/absent means the root (categories
    and root channels), otherwise a category id. `channels` must list
    **exactly** the channels whose parent is that scope, each once, in the
    desired order; positions are then assigned densely as `0..K-1`.

    Every channel whose index changes must be modifiable by the caller
    (`modify_channels` computed on that channel); otherwise the request is a
    403. Channels whose index is unchanged are pinned and need no rights.
    Only ordering within one scope is affected — channels are not reparented.

    On success the server emits a `channels_reordered` gateway event
    carrying only `guild_id`; clients refetch
    `GET /guilds/{guild_id}/channels`.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutGuildChannelsOrderBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
            body=body,
        )
    ).parsed
