from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.webhook import Webhook
from ...types import Response


def _get_kwargs(
    webhook_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/webhooks/{webhook_id}".format(
            webhook_id=quote(str(webhook_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | Webhook | None:
    if response.status_code == 200:
        response_200 = Webhook.from_dict(response.json())

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | Webhook]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    webhook_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Error | Webhook]:
    """Get a webhook

     Returns the webhook by id. Soft-deleted rows are still returned (with `deleted_at` set) so messages
    posted by a deleted webhook keep rendering name/avatar; management endpoints instead treat a deleted
    webhook as 404. Readable by any authenticated user (metadata is not permission-gated).

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Webhook]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    webhook_id: str,
    *,
    client: AuthenticatedClient,
) -> Error | Webhook | None:
    """Get a webhook

     Returns the webhook by id. Soft-deleted rows are still returned (with `deleted_at` set) so messages
    posted by a deleted webhook keep rendering name/avatar; management endpoints instead treat a deleted
    webhook as 404. Readable by any authenticated user (metadata is not permission-gated).

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Webhook
    """

    return sync_detailed(
        webhook_id=webhook_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    webhook_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Error | Webhook]:
    """Get a webhook

     Returns the webhook by id. Soft-deleted rows are still returned (with `deleted_at` set) so messages
    posted by a deleted webhook keep rendering name/avatar; management endpoints instead treat a deleted
    webhook as 404. Readable by any authenticated user (metadata is not permission-gated).

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Webhook]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: str,
    *,
    client: AuthenticatedClient,
) -> Error | Webhook | None:
    """Get a webhook

     Returns the webhook by id. Soft-deleted rows are still returned (with `deleted_at` set) so messages
    posted by a deleted webhook keep rendering name/avatar; management endpoints instead treat a deleted
    webhook as 404. Readable by any authenticated user (metadata is not permission-gated).

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Webhook
    """

    return (
        await asyncio_detailed(
            webhook_id=webhook_id,
            client=client,
        )
    ).parsed
