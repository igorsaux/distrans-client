from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel import Channel
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    guild_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/guilds/{guild_id}/channels".format(
            guild_id=quote(str(guild_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | list[Channel] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Channel.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Error | list[Channel]]:
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
) -> Response[Error | list[Channel]]:
    """List guild channels (full objects)

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[Channel]]
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
) -> Error | list[Channel] | None:
    """List guild channels (full objects)

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[Channel]
    """

    return sync_detailed(
        guild_id=guild_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    guild_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Error | list[Channel]]:
    """List guild channels (full objects)

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[Channel]]
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
) -> Error | list[Channel] | None:
    """List guild channels (full objects)

    Args:
        guild_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[Channel]
    """

    return (
        await asyncio_detailed(
            guild_id=guild_id,
            client=client,
        )
    ).parsed
