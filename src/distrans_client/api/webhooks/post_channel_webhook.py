from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.webhook_input import WebhookInput
from ...models.webhook_token import WebhookToken
from ...types import Response


def _get_kwargs(
    channel_id: str,
    *,
    body: WebhookInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/channels/{channel_id}/webhooks".format(
            channel_id=quote(str(channel_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | WebhookToken | None:
    if response.status_code == 201:
        response_201 = WebhookToken.from_dict(response.json())

        return response_201

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
) -> Response[Error | WebhookToken]:
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
    body: WebhookInput,
) -> Response[Error | WebhookToken]:
    """Create a webhook (create_webhooks required)

     Creates a webhook on the channel. The channel must hold fewer than
    `api.webhooks.max_webhooks_per_channel` live webhooks, otherwise the request is rejected with 400
    "'webhooks' is too many". The response is `201 {"id","token"}`; the plaintext `token` is returned
    exactly once and only its sha256 is stored. Soft-deleted webhooks do not count against the cap.
    Dispatches a `webhook_created` gateway event.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (WebhookInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WebhookToken]
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
    body: WebhookInput,
) -> Error | WebhookToken | None:
    """Create a webhook (create_webhooks required)

     Creates a webhook on the channel. The channel must hold fewer than
    `api.webhooks.max_webhooks_per_channel` live webhooks, otherwise the request is rejected with 400
    "'webhooks' is too many". The response is `201 {"id","token"}`; the plaintext `token` is returned
    exactly once and only its sha256 is stored. Soft-deleted webhooks do not count against the cap.
    Dispatches a `webhook_created` gateway event.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (WebhookInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WebhookToken
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
    body: WebhookInput,
) -> Response[Error | WebhookToken]:
    """Create a webhook (create_webhooks required)

     Creates a webhook on the channel. The channel must hold fewer than
    `api.webhooks.max_webhooks_per_channel` live webhooks, otherwise the request is rejected with 400
    "'webhooks' is too many". The response is `201 {"id","token"}`; the plaintext `token` is returned
    exactly once and only its sha256 is stored. Soft-deleted webhooks do not count against the cap.
    Dispatches a `webhook_created` gateway event.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (WebhookInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | WebhookToken]
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
    body: WebhookInput,
) -> Error | WebhookToken | None:
    """Create a webhook (create_webhooks required)

     Creates a webhook on the channel. The channel must hold fewer than
    `api.webhooks.max_webhooks_per_channel` live webhooks, otherwise the request is rejected with 400
    "'webhooks' is too many". The response is `201 {"id","token"}`; the plaintext `token` is returned
    exactly once and only its sha256 is stored. Soft-deleted webhooks do not count against the cap.
    Dispatches a `webhook_created` gateway event.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (WebhookInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | WebhookToken
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
            body=body,
        )
    ).parsed
