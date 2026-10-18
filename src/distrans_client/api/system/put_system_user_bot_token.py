from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.put_system_user_bot_token_response_200 import (
    PutSystemUserBotTokenResponse200,
)
from ...types import Response


def _get_kwargs(
    user_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/system/users/{user_id}".format(
            user_id=quote(str(user_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | PutSystemUserBotTokenResponse200 | None:
    if response.status_code == 200:
        response_200 = PutSystemUserBotTokenResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | PutSystemUserBotTokenResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Error | PutSystemUserBotTokenResponse200]:
    """Issue (or rotate) the static bot token of a user

     Only bot accounts (`is_bot`) carry a static token. Exactly one token exists per bot: re-issuing
    revokes the previous token. The plaintext token is returned once; the server stores only its SHA-256
    hash. Bot tokens have no expiry and are accepted by `bearerAuth` and the gateway `identify`.

    Args:
        user_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PutSystemUserBotTokenResponse200]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: AuthenticatedClient,
) -> Error | PutSystemUserBotTokenResponse200 | None:
    """Issue (or rotate) the static bot token of a user

     Only bot accounts (`is_bot`) carry a static token. Exactly one token exists per bot: re-issuing
    revokes the previous token. The plaintext token is returned once; the server stores only its SHA-256
    hash. Bot tokens have no expiry and are accepted by `bearerAuth` and the gateway `identify`.

    Args:
        user_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PutSystemUserBotTokenResponse200
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Error | PutSystemUserBotTokenResponse200]:
    """Issue (or rotate) the static bot token of a user

     Only bot accounts (`is_bot`) carry a static token. Exactly one token exists per bot: re-issuing
    revokes the previous token. The plaintext token is returned once; the server stores only its SHA-256
    hash. Bot tokens have no expiry and are accepted by `bearerAuth` and the gateway `identify`.

    Args:
        user_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PutSystemUserBotTokenResponse200]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: AuthenticatedClient,
) -> Error | PutSystemUserBotTokenResponse200 | None:
    """Issue (or rotate) the static bot token of a user

     Only bot accounts (`is_bot`) carry a static token. Exactly one token exists per bot: re-issuing
    revokes the previous token. The plaintext token is returned once; the server stores only its SHA-256
    hash. Bot tokens have no expiry and are accepted by `bearerAuth` and the gateway `identify`.

    Args:
        user_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PutSystemUserBotTokenResponse200
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
        )
    ).parsed
