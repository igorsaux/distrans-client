from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.users_sync import UsersSync
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    since: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["since"] = since

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/users/sync",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | UsersSync | None:
    if response.status_code == 200:
        response_200 = UsersSync.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | UsersSync]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Response[Error | UsersSync]:
    """Changed users since a cursor

     Global changed-since delta for users. Returns only the ids of present rows whose `updated_at` is
    newer than `since` (upserts). Soft-deleted users stay present and are therefore listed; the client
    drops them after fetching one and observing `deleted_at`. Hard deletions are not listed.

    Args:
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UsersSync]
    """

    kwargs = _get_kwargs(
        since=since,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Error | UsersSync | None:
    """Changed users since a cursor

     Global changed-since delta for users. Returns only the ids of present rows whose `updated_at` is
    newer than `since` (upserts). Soft-deleted users stay present and are therefore listed; the client
    drops them after fetching one and observing `deleted_at`. Hard deletions are not listed.

    Args:
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UsersSync
    """

    return sync_detailed(
        client=client,
        since=since,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Response[Error | UsersSync]:
    """Changed users since a cursor

     Global changed-since delta for users. Returns only the ids of present rows whose `updated_at` is
    newer than `since` (upserts). Soft-deleted users stay present and are therefore listed; the client
    drops them after fetching one and observing `deleted_at`. Hard deletions are not listed.

    Args:
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UsersSync]
    """

    kwargs = _get_kwargs(
        since=since,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    since: int | Unset = UNSET,
) -> Error | UsersSync | None:
    """Changed users since a cursor

     Global changed-since delta for users. Returns only the ids of present rows whose `updated_at` is
    newer than `since` (upserts). Soft-deleted users stay present and are therefore listed; the client
    drops them after fetching one and observing `deleted_at`. Hard deletions are not listed.

    Args:
        since (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UsersSync
    """

    return (
        await asyncio_detailed(
            client=client,
            since=since,
        )
    ).parsed
