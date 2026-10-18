from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_me_userdata_response_200 import GetMeUserdataResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/users/@me/userdata",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | GetMeUserdataResponse200 | None:
    if response.status_code == 200:
        response_200 = GetMeUserdataResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | GetMeUserdataResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Error | GetMeUserdataResponse200]:
    """Get the current user's userdata

     Returns the stored opaque blob as `{"data": <arbitrary JSON value>, "updated_at": <epoch ms>}`. The
    server does not enforce any schema on `data`; it is whatever the client last stored. When nothing
    has been stored yet, both `data` and `updated_at` are `null` (never 404). `updated_at` is a non-
    negative Unix epoch in milliseconds, so a client can tell whether its local copy is stale.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetMeUserdataResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Error | GetMeUserdataResponse200 | None:
    """Get the current user's userdata

     Returns the stored opaque blob as `{"data": <arbitrary JSON value>, "updated_at": <epoch ms>}`. The
    server does not enforce any schema on `data`; it is whatever the client last stored. When nothing
    has been stored yet, both `data` and `updated_at` are `null` (never 404). `updated_at` is a non-
    negative Unix epoch in milliseconds, so a client can tell whether its local copy is stale.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetMeUserdataResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Error | GetMeUserdataResponse200]:
    """Get the current user's userdata

     Returns the stored opaque blob as `{"data": <arbitrary JSON value>, "updated_at": <epoch ms>}`. The
    server does not enforce any schema on `data`; it is whatever the client last stored. When nothing
    has been stored yet, both `data` and `updated_at` are `null` (never 404). `updated_at` is a non-
    negative Unix epoch in milliseconds, so a client can tell whether its local copy is stale.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetMeUserdataResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Error | GetMeUserdataResponse200 | None:
    """Get the current user's userdata

     Returns the stored opaque blob as `{"data": <arbitrary JSON value>, "updated_at": <epoch ms>}`. The
    server does not enforce any schema on `data`; it is whatever the client last stored. When nothing
    has been stored yet, both `data` and `updated_at` are `null` (never 404). `updated_at` is a non-
    negative Unix epoch in milliseconds, so a client can tell whether its local copy is stale.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetMeUserdataResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
