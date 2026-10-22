from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_webhook_message_body import EditWebhookMessageBody
from ...models.error import Error
from ...models.message import Message
from ...types import Response


def _get_kwargs(
    webhook_id: str,
    token: str,
    message_id: str,
    *,
    body: EditWebhookMessageBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/webhooks/{webhook_id}/{token}/messages/{message_id}".format(
            webhook_id=quote(str(webhook_id), safe=""),
            token=quote(str(token), safe=""),
            message_id=quote(str(message_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | Message | None:
    if response.status_code == 200:
        response_200 = Message.from_dict(response.json())

        return response_200

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
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: EditWebhookMessageBody,
) -> Response[Error | Message]:
    """Edit a webhook message (token-authenticated, no session)

     Edits a message previously sent by this webhook. The webhook and message checks are the same as
    `GET`. The body must contain `content` and/or `embeds`; an absent field keeps the stored value, an
    explicit `null` or `[]` clears embeds, and the resulting message must have non-empty content or
    embeds. Content follows the same sanitization and limits as `PATCH /messages/{message_id}`.
    Attachments and mentions are recomputed from the effective content; `allowed_mentions` is not
    accepted on edit because edits never notify. Emits `message_updated` and returns the updated message
    object.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (EditWebhookMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Message]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        token=token,
        message_id=message_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    webhook_id: str,
    token: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: EditWebhookMessageBody,
) -> Error | Message | None:
    """Edit a webhook message (token-authenticated, no session)

     Edits a message previously sent by this webhook. The webhook and message checks are the same as
    `GET`. The body must contain `content` and/or `embeds`; an absent field keeps the stored value, an
    explicit `null` or `[]` clears embeds, and the resulting message must have non-empty content or
    embeds. Content follows the same sanitization and limits as `PATCH /messages/{message_id}`.
    Attachments and mentions are recomputed from the effective content; `allowed_mentions` is not
    accepted on edit because edits never notify. Emits `message_updated` and returns the updated message
    object.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (EditWebhookMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Message
    """

    return sync_detailed(
        webhook_id=webhook_id,
        token=token,
        message_id=message_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    webhook_id: str,
    token: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: EditWebhookMessageBody,
) -> Response[Error | Message]:
    """Edit a webhook message (token-authenticated, no session)

     Edits a message previously sent by this webhook. The webhook and message checks are the same as
    `GET`. The body must contain `content` and/or `embeds`; an absent field keeps the stored value, an
    explicit `null` or `[]` clears embeds, and the resulting message must have non-empty content or
    embeds. Content follows the same sanitization and limits as `PATCH /messages/{message_id}`.
    Attachments and mentions are recomputed from the effective content; `allowed_mentions` is not
    accepted on edit because edits never notify. Emits `message_updated` and returns the updated message
    object.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (EditWebhookMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Message]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        token=token,
        message_id=message_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: str,
    token: str,
    message_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: EditWebhookMessageBody,
) -> Error | Message | None:
    """Edit a webhook message (token-authenticated, no session)

     Edits a message previously sent by this webhook. The webhook and message checks are the same as
    `GET`. The body must contain `content` and/or `embeds`; an absent field keeps the stored value, an
    explicit `null` or `[]` clears embeds, and the resulting message must have non-empty content or
    embeds. Content follows the same sanitization and limits as `PATCH /messages/{message_id}`.
    Attachments and mentions are recomputed from the effective content; `allowed_mentions` is not
    accepted on edit because edits never notify. Emits `message_updated` and returns the updated message
    object.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (EditWebhookMessageBody):

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
            message_id=message_id,
            client=client,
            body=body,
        )
    ).parsed
