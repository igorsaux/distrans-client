from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.patch_me_body import PatchMeBody
from ...types import Response


def _get_kwargs(
    *,
    body: PatchMeBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/users/@me",
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
    *,
    client: AuthenticatedClient,
    body: PatchMeBody,
) -> Response[Any | Error]:
    """Update the current user

     PATCH semantics: an absent field is unchanged; an explicit `null` clears the field (nullable fields
    only). Every PATCH (including a no-op with only `current_password`) requires `current_password`,
    verified against the stored hash; on a mismatch the server responds 401 `"Bad password"`. Accounts
    without a password (bots, passwordless users) are rejected with 400 `"User has no password"`. A
    password change additionally requires the new `password` to differ from `current_password`. The
    `username` may be changed with the same validation as account creation; a taken username is rejected
    with 409 `"Username is already used"`. Every successful update dispatches a `user_updated` gateway
    event.

    Args:
        body (PatchMeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: PatchMeBody,
) -> Any | Error | None:
    """Update the current user

     PATCH semantics: an absent field is unchanged; an explicit `null` clears the field (nullable fields
    only). Every PATCH (including a no-op with only `current_password`) requires `current_password`,
    verified against the stored hash; on a mismatch the server responds 401 `"Bad password"`. Accounts
    without a password (bots, passwordless users) are rejected with 400 `"User has no password"`. A
    password change additionally requires the new `password` to differ from `current_password`. The
    `username` may be changed with the same validation as account creation; a taken username is rejected
    with 409 `"Username is already used"`. Every successful update dispatches a `user_updated` gateway
    event.

    Args:
        body (PatchMeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PatchMeBody,
) -> Response[Any | Error]:
    """Update the current user

     PATCH semantics: an absent field is unchanged; an explicit `null` clears the field (nullable fields
    only). Every PATCH (including a no-op with only `current_password`) requires `current_password`,
    verified against the stored hash; on a mismatch the server responds 401 `"Bad password"`. Accounts
    without a password (bots, passwordless users) are rejected with 400 `"User has no password"`. A
    password change additionally requires the new `password` to differ from `current_password`. The
    `username` may be changed with the same validation as account creation; a taken username is rejected
    with 409 `"Username is already used"`. Every successful update dispatches a `user_updated` gateway
    event.

    Args:
        body (PatchMeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: PatchMeBody,
) -> Any | Error | None:
    """Update the current user

     PATCH semantics: an absent field is unchanged; an explicit `null` clears the field (nullable fields
    only). Every PATCH (including a no-op with only `current_password`) requires `current_password`,
    verified against the stored hash; on a mismatch the server responds 401 `"Bad password"`. Accounts
    without a password (bots, passwordless users) are rejected with 400 `"User has no password"`. A
    password change additionally requires the new `password` to differ from `current_password`. The
    `username` may be changed with the same validation as account creation; a taken username is rejected
    with 409 `"Username is already used"`. Every successful update dispatches a `user_updated` gateway
    event.

    Args:
        body (PatchMeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
