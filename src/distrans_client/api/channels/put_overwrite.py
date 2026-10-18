from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.put_overwrite_body import PutOverwriteBody
from ...types import Response


def _get_kwargs(
    channel_id: str,
    *,
    body: PutOverwriteBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/channels/{channel_id}/overwrites".format(
            channel_id=quote(str(channel_id), safe=""),
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
    channel_id: str,
    *,
    client: AuthenticatedClient,
    body: PutOverwriteBody,
) -> Response[Any | Error]:
    """Create or update a channel permission overwrite (upsert)

     Upserts an overwrite for a role or member on the channel. Setting both `allow` and `deny` to `"0"`
    removes the overwrite. Requires `manage_overwrites` computed on the channel. Every bit flipped by
    the request (XOR of the old/new `allow` and old/new `deny`; all set `allow|deny` bits when creating)
    must be present in the caller's channel permissions. Target hierarchy: a member target must be
    strictly below the caller's highest role position (self-overwrites are always allowed, even with no
    roles), a role target's position must be strictly below the caller's highest role position. An
    identical `allow`/`deny` pair is an idempotent no-op (204) and bypasses the hierarchy checks.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutOverwriteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    body: PutOverwriteBody,
) -> Any | Error | None:
    """Create or update a channel permission overwrite (upsert)

     Upserts an overwrite for a role or member on the channel. Setting both `allow` and `deny` to `"0"`
    removes the overwrite. Requires `manage_overwrites` computed on the channel. Every bit flipped by
    the request (XOR of the old/new `allow` and old/new `deny`; all set `allow|deny` bits when creating)
    must be present in the caller's channel permissions. Target hierarchy: a member target must be
    strictly below the caller's highest role position (self-overwrites are always allowed, even with no
    roles), a role target's position must be strictly below the caller's highest role position. An
    identical `allow`/`deny` pair is an idempotent no-op (204) and bypasses the hierarchy checks.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutOverwriteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        channel_id=channel_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    body: PutOverwriteBody,
) -> Response[Any | Error]:
    """Create or update a channel permission overwrite (upsert)

     Upserts an overwrite for a role or member on the channel. Setting both `allow` and `deny` to `"0"`
    removes the overwrite. Requires `manage_overwrites` computed on the channel. Every bit flipped by
    the request (XOR of the old/new `allow` and old/new `deny`; all set `allow|deny` bits when creating)
    must be present in the caller's channel permissions. Target hierarchy: a member target must be
    strictly below the caller's highest role position (self-overwrites are always allowed, even with no
    roles), a role target's position must be strictly below the caller's highest role position. An
    identical `allow`/`deny` pair is an idempotent no-op (204) and bypasses the hierarchy checks.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutOverwriteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    channel_id: str,
    *,
    client: AuthenticatedClient,
    body: PutOverwriteBody,
) -> Any | Error | None:
    """Create or update a channel permission overwrite (upsert)

     Upserts an overwrite for a role or member on the channel. Setting both `allow` and `deny` to `"0"`
    removes the overwrite. Requires `manage_overwrites` computed on the channel. Every bit flipped by
    the request (XOR of the old/new `allow` and old/new `deny`; all set `allow|deny` bits when creating)
    must be present in the caller's channel permissions. Target hierarchy: a member target must be
    strictly below the caller's highest role position (self-overwrites are always allowed, even with no
    roles), a role target's position must be strictly below the caller's highest role position. An
    identical `allow`/`deny` pair is an idempotent no-op (204) and bypasses the hierarchy checks.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PutOverwriteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
            body=body,
        )
    ).parsed
