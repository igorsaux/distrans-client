from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.patch_system_user_body import PatchSystemUserBody
from ...types import Response


def _get_kwargs(
    user_id: str,
    *,
    body: PatchSystemUserBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/system/users/{user_id}".format(
            user_id=quote(str(user_id), safe=""),
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

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

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
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: PatchSystemUserBody,
) -> Response[Any | Error]:
    """Edit a user

     Edits `username`, `display_name` and `password`. Absent fields are left unchanged; explicit `null`
    clears `display_name` or `password` (making the account passwordless). `username` cannot be cleared.
    A password is forbidden for bot accounts. Setting or clearing a password revokes all refresh tokens
    of the user and removes all of the user's push subscriptions. Avatars are managed by `PUT
    /users/@me/avatar`.

    Args:
        user_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchSystemUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: PatchSystemUserBody,
) -> Any | Error | None:
    """Edit a user

     Edits `username`, `display_name` and `password`. Absent fields are left unchanged; explicit `null`
    clears `display_name` or `password` (making the account passwordless). `username` cannot be cleared.
    A password is forbidden for bot accounts. Setting or clearing a password revokes all refresh tokens
    of the user and removes all of the user's push subscriptions. Avatars are managed by `PUT
    /users/@me/avatar`.

    Args:
        user_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchSystemUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: PatchSystemUserBody,
) -> Response[Any | Error]:
    """Edit a user

     Edits `username`, `display_name` and `password`. Absent fields are left unchanged; explicit `null`
    clears `display_name` or `password` (making the account passwordless). `username` cannot be cleared.
    A password is forbidden for bot accounts. Setting or clearing a password revokes all refresh tokens
    of the user and removes all of the user's push subscriptions. Avatars are managed by `PUT
    /users/@me/avatar`.

    Args:
        user_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchSystemUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: PatchSystemUserBody,
) -> Any | Error | None:
    """Edit a user

     Edits `username`, `display_name` and `password`. Absent fields are left unchanged; explicit `null`
    clears `display_name` or `password` (making the account passwordless). `username` cannot be cleared.
    A password is forbidden for bot accounts. Setting or clearing a password revokes all refresh tokens
    of the user and removes all of the user's push subscriptions. Avatars are managed by `PUT
    /users/@me/avatar`.

    Args:
        user_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchSystemUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
