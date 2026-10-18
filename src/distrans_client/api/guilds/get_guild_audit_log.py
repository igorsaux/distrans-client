from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_guild_audit_log_response_200 import GetGuildAuditLogResponse200
from ...models.get_guild_audit_log_sort import GetGuildAuditLogSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    guild_id: str,
    *,
    user: str | Unset = UNSET,
    action: str | Unset = UNSET,
    offset: int | Unset = 0,
    sort: GetGuildAuditLogSort | Unset = GetGuildAuditLogSort.NEWEST,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["user"] = user

    params["action"] = action

    params["offset"] = offset

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/guilds/{guild_id}/audit-log".format(
            guild_id=quote(str(guild_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetGuildAuditLogResponse200 | None:
    if response.status_code == 200:
        response_200 = GetGuildAuditLogResponse200.from_dict(response.json())

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

    if response.status_code == 405:
        response_405 = Error.from_dict(response.json())

        return response_405

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | GetGuildAuditLogResponse200]:
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
    user: str | Unset = UNSET,
    action: str | Unset = UNSET,
    offset: int | Unset = 0,
    sort: GetGuildAuditLogSort | Unset = GetGuildAuditLogSort.NEWEST,
    limit: int | Unset = UNSET,
) -> Response[Error | GetGuildAuditLogResponse200]:
    """Read a guild's audit log

     Per-guild, append-only log of management actions (channels, roles, overwrites, emojis, webhooks,
    guild updates, moderation). Entries carry the actor and the target ids only, never a before/after
    payload. Requires the guild-level `view_audit_log` permission. Results are ordered by `sort` (newest
    first by default) and paginated with `offset`/`limit`; `total` is the exact number of matches and
    does not depend on the requested page.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        user (str | Unset):
        action (str | Unset):
        offset (int | Unset):  Default: 0.
        sort (GetGuildAuditLogSort | Unset):  Default: GetGuildAuditLogSort.NEWEST.
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetGuildAuditLogResponse200]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        user=user,
        action=action,
        offset=offset,
        sort=sort,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    user: str | Unset = UNSET,
    action: str | Unset = UNSET,
    offset: int | Unset = 0,
    sort: GetGuildAuditLogSort | Unset = GetGuildAuditLogSort.NEWEST,
    limit: int | Unset = UNSET,
) -> Error | GetGuildAuditLogResponse200 | None:
    """Read a guild's audit log

     Per-guild, append-only log of management actions (channels, roles, overwrites, emojis, webhooks,
    guild updates, moderation). Entries carry the actor and the target ids only, never a before/after
    payload. Requires the guild-level `view_audit_log` permission. Results are ordered by `sort` (newest
    first by default) and paginated with `offset`/`limit`; `total` is the exact number of matches and
    does not depend on the requested page.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        user (str | Unset):
        action (str | Unset):
        offset (int | Unset):  Default: 0.
        sort (GetGuildAuditLogSort | Unset):  Default: GetGuildAuditLogSort.NEWEST.
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetGuildAuditLogResponse200
    """

    return sync_detailed(
        guild_id=guild_id,
        client=client,
        user=user,
        action=action,
        offset=offset,
        sort=sort,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    user: str | Unset = UNSET,
    action: str | Unset = UNSET,
    offset: int | Unset = 0,
    sort: GetGuildAuditLogSort | Unset = GetGuildAuditLogSort.NEWEST,
    limit: int | Unset = UNSET,
) -> Response[Error | GetGuildAuditLogResponse200]:
    """Read a guild's audit log

     Per-guild, append-only log of management actions (channels, roles, overwrites, emojis, webhooks,
    guild updates, moderation). Entries carry the actor and the target ids only, never a before/after
    payload. Requires the guild-level `view_audit_log` permission. Results are ordered by `sort` (newest
    first by default) and paginated with `offset`/`limit`; `total` is the exact number of matches and
    does not depend on the requested page.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        user (str | Unset):
        action (str | Unset):
        offset (int | Unset):  Default: 0.
        sort (GetGuildAuditLogSort | Unset):  Default: GetGuildAuditLogSort.NEWEST.
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetGuildAuditLogResponse200]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        user=user,
        action=action,
        offset=offset,
        sort=sort,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    user: str | Unset = UNSET,
    action: str | Unset = UNSET,
    offset: int | Unset = 0,
    sort: GetGuildAuditLogSort | Unset = GetGuildAuditLogSort.NEWEST,
    limit: int | Unset = UNSET,
) -> Error | GetGuildAuditLogResponse200 | None:
    """Read a guild's audit log

     Per-guild, append-only log of management actions (channels, roles, overwrites, emojis, webhooks,
    guild updates, moderation). Entries carry the actor and the target ids only, never a before/after
    payload. Requires the guild-level `view_audit_log` permission. Results are ordered by `sort` (newest
    first by default) and paginated with `offset`/`limit`; `total` is the exact number of matches and
    does not depend on the requested page.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        user (str | Unset):
        action (str | Unset):
        offset (int | Unset):  Default: 0.
        sort (GetGuildAuditLogSort | Unset):  Default: GetGuildAuditLogSort.NEWEST.
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetGuildAuditLogResponse200
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
            user=user,
            action=action,
            offset=offset,
            sort=sort,
            limit=limit,
        )
    ).parsed
