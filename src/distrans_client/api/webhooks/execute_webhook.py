from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.execute_webhook_body import ExecuteWebhookBody
from ...models.message import Message
from ...types import Response


def _get_kwargs(
    webhook_id: str,
    token: str,
    *,
    body: ExecuteWebhookBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/webhooks/{webhook_id}/{token}".format(
            webhook_id=quote(str(webhook_id), safe=""),
            token=quote(str(token), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | Message | None:
    if response.status_code == 201:
        response_201 = Message.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

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
) -> Response[Error | Message]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    webhook_id: str,
    token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecuteWebhookBody,
) -> Response[Error | Message]:
    """Execute a webhook (token-authenticated, no session)

     Posts a message into the webhook's channel as the webhook. The token is the capability: there is no
    session, no bearer auth, and no channel permission check (mirroring `POST
    /channels/{channel_id}/messages`). The webhook must exist, not be soft-deleted and `token` must hash
    to its stored `token_hash`; anything else is 404. The body is validated exactly like `POST
    /channels/{channel_id}/messages` (`content`, `reply_to_id`, `embeds`, `mentions`,
    `allowed_mentions`, and attachments derived from `content`); the stored message has `author_id` null
    and `webhook_id` set. A `message_created` gateway event and push notifications are emitted like a
    user message; the push payload carries the author's `author_id` (null for a webhook), `author_name`,
    `author_avatar_hash` and `webhook_id` so the client can render the author without an extra lookup.
    Returns the created message object.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        body (ExecuteWebhookBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Message]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        token=token,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    webhook_id: str,
    token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecuteWebhookBody,
) -> Error | Message | None:
    """Execute a webhook (token-authenticated, no session)

     Posts a message into the webhook's channel as the webhook. The token is the capability: there is no
    session, no bearer auth, and no channel permission check (mirroring `POST
    /channels/{channel_id}/messages`). The webhook must exist, not be soft-deleted and `token` must hash
    to its stored `token_hash`; anything else is 404. The body is validated exactly like `POST
    /channels/{channel_id}/messages` (`content`, `reply_to_id`, `embeds`, `mentions`,
    `allowed_mentions`, and attachments derived from `content`); the stored message has `author_id` null
    and `webhook_id` set. A `message_created` gateway event and push notifications are emitted like a
    user message; the push payload carries the author's `author_id` (null for a webhook), `author_name`,
    `author_avatar_hash` and `webhook_id` so the client can render the author without an extra lookup.
    Returns the created message object.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        body (ExecuteWebhookBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Message
    """

    return sync_detailed(
        webhook_id=webhook_id,
        token=token,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    webhook_id: str,
    token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecuteWebhookBody,
) -> Response[Error | Message]:
    """Execute a webhook (token-authenticated, no session)

     Posts a message into the webhook's channel as the webhook. The token is the capability: there is no
    session, no bearer auth, and no channel permission check (mirroring `POST
    /channels/{channel_id}/messages`). The webhook must exist, not be soft-deleted and `token` must hash
    to its stored `token_hash`; anything else is 404. The body is validated exactly like `POST
    /channels/{channel_id}/messages` (`content`, `reply_to_id`, `embeds`, `mentions`,
    `allowed_mentions`, and attachments derived from `content`); the stored message has `author_id` null
    and `webhook_id` set. A `message_created` gateway event and push notifications are emitted like a
    user message; the push payload carries the author's `author_id` (null for a webhook), `author_name`,
    `author_avatar_hash` and `webhook_id` so the client can render the author without an extra lookup.
    Returns the created message object.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        body (ExecuteWebhookBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Message]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        token=token,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: str,
    token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecuteWebhookBody,
) -> Error | Message | None:
    """Execute a webhook (token-authenticated, no session)

     Posts a message into the webhook's channel as the webhook. The token is the capability: there is no
    session, no bearer auth, and no channel permission check (mirroring `POST
    /channels/{channel_id}/messages`). The webhook must exist, not be soft-deleted and `token` must hash
    to its stored `token_hash`; anything else is 404. The body is validated exactly like `POST
    /channels/{channel_id}/messages` (`content`, `reply_to_id`, `embeds`, `mentions`,
    `allowed_mentions`, and attachments derived from `content`); the stored message has `author_id` null
    and `webhook_id` set. A `message_created` gateway event and push notifications are emitted like a
    user message; the push payload carries the author's `author_id` (null for a webhook), `author_name`,
    `author_avatar_hash` and `webhook_id` so the client can render the author without an extra lookup.
    Returns the created message object.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        body (ExecuteWebhookBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Message
    """

    return (
        await asyncio_detailed(
            webhook_id=webhook_id,
            token=token,
            client=client,
            body=body,
        )
    ).parsed
