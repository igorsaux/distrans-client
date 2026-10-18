from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.put_guild_roles_order_body import PutGuildRolesOrderBody
from ...types import Response


def _get_kwargs(
    guild_id: str,
    *,
    body: PutGuildRolesOrderBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/guilds/{guild_id}/roles/order".format(
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
    body: PutGuildRolesOrderBody,
) -> Response[Any | Error]:
    """Reorder guild roles (modify_roles required)

     Sets the order of the guild's roles in one atomic request. The body's
    `roles` array must list **every** non-`@everyone` role of the guild
    exactly once, in the desired order; `@everyone` (role id = guild id)
    must be absent. Positions are then assigned densely as `1..N`.

    Hierarchy is enforced by pinning: a role the caller cannot move (its
    current position is at or above the caller's highest role position)
    must keep its exact index
    in the list. Roles the caller can move may only be permuted within the
    segments between pinned roles; moving a pinned role is a 403. A role
    list that is not a permutation of the guild's roles is a 400.

    On success the server emits a `roles_reordered` gateway event carrying
    only `guild_id`; clients refetch `GET /guilds/{guild_id}/roles`.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutGuildRolesOrderBody):

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
    body: PutGuildRolesOrderBody,
) -> Any | Error | None:
    """Reorder guild roles (modify_roles required)

     Sets the order of the guild's roles in one atomic request. The body's
    `roles` array must list **every** non-`@everyone` role of the guild
    exactly once, in the desired order; `@everyone` (role id = guild id)
    must be absent. Positions are then assigned densely as `1..N`.

    Hierarchy is enforced by pinning: a role the caller cannot move (its
    current position is at or above the caller's highest role position)
    must keep its exact index
    in the list. Roles the caller can move may only be permuted within the
    segments between pinned roles; moving a pinned role is a 403. A role
    list that is not a permutation of the guild's roles is a 400.

    On success the server emits a `roles_reordered` gateway event carrying
    only `guild_id`; clients refetch `GET /guilds/{guild_id}/roles`.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutGuildRolesOrderBody):

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
    body: PutGuildRolesOrderBody,
) -> Response[Any | Error]:
    """Reorder guild roles (modify_roles required)

     Sets the order of the guild's roles in one atomic request. The body's
    `roles` array must list **every** non-`@everyone` role of the guild
    exactly once, in the desired order; `@everyone` (role id = guild id)
    must be absent. Positions are then assigned densely as `1..N`.

    Hierarchy is enforced by pinning: a role the caller cannot move (its
    current position is at or above the caller's highest role position)
    must keep its exact index
    in the list. Roles the caller can move may only be permuted within the
    segments between pinned roles; moving a pinned role is a 403. A role
    list that is not a permutation of the guild's roles is a 400.

    On success the server emits a `roles_reordered` gateway event carrying
    only `guild_id`; clients refetch `GET /guilds/{guild_id}/roles`.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutGuildRolesOrderBody):

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
    body: PutGuildRolesOrderBody,
) -> Any | Error | None:
    """Reorder guild roles (modify_roles required)

     Sets the order of the guild's roles in one atomic request. The body's
    `roles` array must list **every** non-`@everyone` role of the guild
    exactly once, in the desired order; `@everyone` (role id = guild id)
    must be absent. Positions are then assigned densely as `1..N`.

    Hierarchy is enforced by pinning: a role the caller cannot move (its
    current position is at or above the caller's highest role position)
    must keep its exact index
    in the list. Roles the caller can move may only be permuted within the
    segments between pinned roles; moving a pinned role is a 403. A role
    list that is not a permutation of the guild's roles is a 400.

    On success the server emits a `roles_reordered` gateway event carrying
    only `guild_id`; clients refetch `GET /guilds/{guild_id}/roles`.

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutGuildRolesOrderBody):

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
