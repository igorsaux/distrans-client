from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.guild_message_search_result import GuildMessageSearchResult
from ...models.search_guild_messages_sort import SearchGuildMessagesSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    guild_id: str,
    *,
    content: str | Unset = UNSET,
    authors: str | Unset = UNSET,
    channels: str | Unset = UNSET,
    mentions: str | Unset = UNSET,
    mention_roles: str | Unset = UNSET,
    author_types: str | Unset = UNSET,
    has_attachments: bool | Unset = UNSET,
    pinned: bool | Unset = UNSET,
    after: int | Unset = UNSET,
    before: int | Unset = UNSET,
    offset: int | Unset = 0,
    sort: SearchGuildMessagesSort | Unset = SearchGuildMessagesSort.NEWEST,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["content"] = content

    params["authors"] = authors

    params["channels"] = channels

    params["mentions"] = mentions

    params["mention_roles"] = mention_roles

    params["author_types"] = author_types

    params["has_attachments"] = has_attachments

    params["pinned"] = pinned

    params["after"] = after

    params["before"] = before

    params["offset"] = offset

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/guilds/{guild_id}/messages/search".format(
            guild_id=quote(str(guild_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GuildMessageSearchResult | None:
    if response.status_code == 200:
        response_200 = GuildMessageSearchResult.from_dict(response.json())

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

    if response.status_code == 405:
        response_405 = Error.from_dict(response.json())

        return response_405

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | GuildMessageSearchResult]:
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
    content: str | Unset = UNSET,
    authors: str | Unset = UNSET,
    channels: str | Unset = UNSET,
    mentions: str | Unset = UNSET,
    mention_roles: str | Unset = UNSET,
    author_types: str | Unset = UNSET,
    has_attachments: bool | Unset = UNSET,
    pinned: bool | Unset = UNSET,
    after: int | Unset = UNSET,
    before: int | Unset = UNSET,
    offset: int | Unset = 0,
    sort: SearchGuildMessagesSort | Unset = SearchGuildMessagesSort.NEWEST,
    limit: int | Unset = UNSET,
) -> Response[Error | GuildMessageSearchResult]:
    """Search a guild's messages

     Per-guild message search. All filters are optional and combine with AND; each id-list filter accepts
    a comma-separated list of decimal ids and matches any of them (OR within a filter). Results only
    include channels where the caller has effective `read_messages`: unreadable channels are silently
    excluded (never 403). The response is ordered by `sort` (newest first by default, oldest first when
    requested) and paginated with `offset`/`limit`; `total` is the exact number of matches and does not
    depend on the requested page.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        content (str | Unset):
        authors (str | Unset):
        channels (str | Unset):
        mentions (str | Unset):
        mention_roles (str | Unset):
        author_types (str | Unset):
        has_attachments (bool | Unset):
        pinned (bool | Unset):
        after (int | Unset):
        before (int | Unset):
        offset (int | Unset):  Default: 0.
        sort (SearchGuildMessagesSort | Unset):  Default: SearchGuildMessagesSort.NEWEST.
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GuildMessageSearchResult]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        content=content,
        authors=authors,
        channels=channels,
        mentions=mentions,
        mention_roles=mention_roles,
        author_types=author_types,
        has_attachments=has_attachments,
        pinned=pinned,
        after=after,
        before=before,
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
    content: str | Unset = UNSET,
    authors: str | Unset = UNSET,
    channels: str | Unset = UNSET,
    mentions: str | Unset = UNSET,
    mention_roles: str | Unset = UNSET,
    author_types: str | Unset = UNSET,
    has_attachments: bool | Unset = UNSET,
    pinned: bool | Unset = UNSET,
    after: int | Unset = UNSET,
    before: int | Unset = UNSET,
    offset: int | Unset = 0,
    sort: SearchGuildMessagesSort | Unset = SearchGuildMessagesSort.NEWEST,
    limit: int | Unset = UNSET,
) -> Error | GuildMessageSearchResult | None:
    """Search a guild's messages

     Per-guild message search. All filters are optional and combine with AND; each id-list filter accepts
    a comma-separated list of decimal ids and matches any of them (OR within a filter). Results only
    include channels where the caller has effective `read_messages`: unreadable channels are silently
    excluded (never 403). The response is ordered by `sort` (newest first by default, oldest first when
    requested) and paginated with `offset`/`limit`; `total` is the exact number of matches and does not
    depend on the requested page.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        content (str | Unset):
        authors (str | Unset):
        channels (str | Unset):
        mentions (str | Unset):
        mention_roles (str | Unset):
        author_types (str | Unset):
        has_attachments (bool | Unset):
        pinned (bool | Unset):
        after (int | Unset):
        before (int | Unset):
        offset (int | Unset):  Default: 0.
        sort (SearchGuildMessagesSort | Unset):  Default: SearchGuildMessagesSort.NEWEST.
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GuildMessageSearchResult
    """

    return sync_detailed(
        guild_id=guild_id,
        client=client,
        content=content,
        authors=authors,
        channels=channels,
        mentions=mentions,
        mention_roles=mention_roles,
        author_types=author_types,
        has_attachments=has_attachments,
        pinned=pinned,
        after=after,
        before=before,
        offset=offset,
        sort=sort,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient,
    content: str | Unset = UNSET,
    authors: str | Unset = UNSET,
    channels: str | Unset = UNSET,
    mentions: str | Unset = UNSET,
    mention_roles: str | Unset = UNSET,
    author_types: str | Unset = UNSET,
    has_attachments: bool | Unset = UNSET,
    pinned: bool | Unset = UNSET,
    after: int | Unset = UNSET,
    before: int | Unset = UNSET,
    offset: int | Unset = 0,
    sort: SearchGuildMessagesSort | Unset = SearchGuildMessagesSort.NEWEST,
    limit: int | Unset = UNSET,
) -> Response[Error | GuildMessageSearchResult]:
    """Search a guild's messages

     Per-guild message search. All filters are optional and combine with AND; each id-list filter accepts
    a comma-separated list of decimal ids and matches any of them (OR within a filter). Results only
    include channels where the caller has effective `read_messages`: unreadable channels are silently
    excluded (never 403). The response is ordered by `sort` (newest first by default, oldest first when
    requested) and paginated with `offset`/`limit`; `total` is the exact number of matches and does not
    depend on the requested page.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        content (str | Unset):
        authors (str | Unset):
        channels (str | Unset):
        mentions (str | Unset):
        mention_roles (str | Unset):
        author_types (str | Unset):
        has_attachments (bool | Unset):
        pinned (bool | Unset):
        after (int | Unset):
        before (int | Unset):
        offset (int | Unset):  Default: 0.
        sort (SearchGuildMessagesSort | Unset):  Default: SearchGuildMessagesSort.NEWEST.
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GuildMessageSearchResult]
    """

    kwargs = _get_kwargs(
        guild_id=guild_id,
        content=content,
        authors=authors,
        channels=channels,
        mentions=mentions,
        mention_roles=mention_roles,
        author_types=author_types,
        has_attachments=has_attachments,
        pinned=pinned,
        after=after,
        before=before,
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
    content: str | Unset = UNSET,
    authors: str | Unset = UNSET,
    channels: str | Unset = UNSET,
    mentions: str | Unset = UNSET,
    mention_roles: str | Unset = UNSET,
    author_types: str | Unset = UNSET,
    has_attachments: bool | Unset = UNSET,
    pinned: bool | Unset = UNSET,
    after: int | Unset = UNSET,
    before: int | Unset = UNSET,
    offset: int | Unset = 0,
    sort: SearchGuildMessagesSort | Unset = SearchGuildMessagesSort.NEWEST,
    limit: int | Unset = UNSET,
) -> Error | GuildMessageSearchResult | None:
    """Search a guild's messages

     Per-guild message search. All filters are optional and combine with AND; each id-list filter accepts
    a comma-separated list of decimal ids and matches any of them (OR within a filter). Results only
    include channels where the caller has effective `read_messages`: unreadable channels are silently
    excluded (never 403). The response is ordered by `sort` (newest first by default, oldest first when
    requested) and paginated with `offset`/`limit`; `total` is the exact number of matches and does not
    depend on the requested page.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        content (str | Unset):
        authors (str | Unset):
        channels (str | Unset):
        mentions (str | Unset):
        mention_roles (str | Unset):
        author_types (str | Unset):
        has_attachments (bool | Unset):
        pinned (bool | Unset):
        after (int | Unset):
        before (int | Unset):
        offset (int | Unset):  Default: 0.
        sort (SearchGuildMessagesSort | Unset):  Default: SearchGuildMessagesSort.NEWEST.
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GuildMessageSearchResult
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
            content=content,
            authors=authors,
            channels=channels,
            mentions=mentions,
            mention_roles=mention_roles,
            author_types=author_types,
            has_attachments=has_attachments,
            pinned=pinned,
            after=after,
            before=before,
            offset=offset,
            sort=sort,
            limit=limit,
        )
    ).parsed
