from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.put_me_userdata_response_200 import PutMeUserdataResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: Any,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/users/@me/userdata",
    }

    _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | PutMeUserdataResponse200 | None:
    if response.status_code == 200:
        response_200 = PutMeUserdataResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | PutMeUserdataResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Any,
) -> Response[Error | PutMeUserdataResponse200]:
    """Replace the current user's userdata

     Stores `data` as the user's opaque blob, replacing any previous value (full replace, idempotent
    upsert). The body must be a valid JSON value of any kind (object, array, string, number, boolean or
    null) and must not exceed `api.users.max_userdata_bytes` (see `GET /limits`). No schema is enforced.
    Responds `200` with the new `updated_at`. No gateway event is dispatched.

    Args:
        body (Any): Any valid JSON value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PutMeUserdataResponse200]
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
    body: Any,
) -> Error | PutMeUserdataResponse200 | None:
    """Replace the current user's userdata

     Stores `data` as the user's opaque blob, replacing any previous value (full replace, idempotent
    upsert). The body must be a valid JSON value of any kind (object, array, string, number, boolean or
    null) and must not exceed `api.users.max_userdata_bytes` (see `GET /limits`). No schema is enforced.
    Responds `200` with the new `updated_at`. No gateway event is dispatched.

    Args:
        body (Any): Any valid JSON value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PutMeUserdataResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Any,
) -> Response[Error | PutMeUserdataResponse200]:
    """Replace the current user's userdata

     Stores `data` as the user's opaque blob, replacing any previous value (full replace, idempotent
    upsert). The body must be a valid JSON value of any kind (object, array, string, number, boolean or
    null) and must not exceed `api.users.max_userdata_bytes` (see `GET /limits`). No schema is enforced.
    Responds `200` with the new `updated_at`. No gateway event is dispatched.

    Args:
        body (Any): Any valid JSON value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PutMeUserdataResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Any,
) -> Error | PutMeUserdataResponse200 | None:
    """Replace the current user's userdata

     Stores `data` as the user's opaque blob, replacing any previous value (full replace, idempotent
    upsert). The body must be a valid JSON value of any kind (object, array, string, number, boolean or
    null) and must not exceed `api.users.max_userdata_bytes` (see `GET /limits`). No schema is enforced.
    Responds `200` with the new `updated_at`. No gateway event is dispatched.

    Args:
        body (Any): Any valid JSON value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PutMeUserdataResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
