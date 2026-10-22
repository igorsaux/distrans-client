from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_message_body import EditMessageBody
from ...models.error import Error
from ...models.message import Message
from ...types import Response


def _get_kwargs(
    message_id: str,
    *,
    body: EditMessageBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/messages/{message_id}".format(
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
) -> Response[Error | Message]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    message_id: str,
    *,
    client: AuthenticatedClient,
    body: EditMessageBody,
) -> Response[Error | Message]:
    """Edit a message (author only; read_messages required)

     The caller must have `read_messages` on the message's channel and be the author of the message.
    `content` follows the same rules as POST /channels/{channel_id}/messages. An optional `embeds`
    replaces the message's embeds: absent leaves them unchanged, an explicit `null` or an empty array
    clears them, and a non-empty array is validated exactly like POST. Attachments are always derived
    from `content` and replace the message's attachment set: every `attachment://<file_id>` reference in
    the new content is a file id (deduplicated, first-appearance order), at most
    `api.messages.max_attachments` unique ids, each of which must exist. An edit that drops a reference
    also drops the file association (letting the GC collect it). Mentions (`mention_everyone`,
    `mentions`, `mention_roles`) are always recomputed from the new `content`; `allowed_mentions` is not
    accepted on edit because edits never notify. Returns the updated message object (the same shape as
    `GET`).

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (EditMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Message]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    message_id: str,
    *,
    client: AuthenticatedClient,
    body: EditMessageBody,
) -> Error | Message | None:
    """Edit a message (author only; read_messages required)

     The caller must have `read_messages` on the message's channel and be the author of the message.
    `content` follows the same rules as POST /channels/{channel_id}/messages. An optional `embeds`
    replaces the message's embeds: absent leaves them unchanged, an explicit `null` or an empty array
    clears them, and a non-empty array is validated exactly like POST. Attachments are always derived
    from `content` and replace the message's attachment set: every `attachment://<file_id>` reference in
    the new content is a file id (deduplicated, first-appearance order), at most
    `api.messages.max_attachments` unique ids, each of which must exist. An edit that drops a reference
    also drops the file association (letting the GC collect it). Mentions (`mention_everyone`,
    `mentions`, `mention_roles`) are always recomputed from the new `content`; `allowed_mentions` is not
    accepted on edit because edits never notify. Returns the updated message object (the same shape as
    `GET`).

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (EditMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Message
    """

    return sync_detailed(
        message_id=message_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    message_id: str,
    *,
    client: AuthenticatedClient,
    body: EditMessageBody,
) -> Response[Error | Message]:
    """Edit a message (author only; read_messages required)

     The caller must have `read_messages` on the message's channel and be the author of the message.
    `content` follows the same rules as POST /channels/{channel_id}/messages. An optional `embeds`
    replaces the message's embeds: absent leaves them unchanged, an explicit `null` or an empty array
    clears them, and a non-empty array is validated exactly like POST. Attachments are always derived
    from `content` and replace the message's attachment set: every `attachment://<file_id>` reference in
    the new content is a file id (deduplicated, first-appearance order), at most
    `api.messages.max_attachments` unique ids, each of which must exist. An edit that drops a reference
    also drops the file association (letting the GC collect it). Mentions (`mention_everyone`,
    `mentions`, `mention_roles`) are always recomputed from the new `content`; `allowed_mentions` is not
    accepted on edit because edits never notify. Returns the updated message object (the same shape as
    `GET`).

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (EditMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Message]
    """

    kwargs = _get_kwargs(
        message_id=message_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    message_id: str,
    *,
    client: AuthenticatedClient,
    body: EditMessageBody,
) -> Error | Message | None:
    """Edit a message (author only; read_messages required)

     The caller must have `read_messages` on the message's channel and be the author of the message.
    `content` follows the same rules as POST /channels/{channel_id}/messages. An optional `embeds`
    replaces the message's embeds: absent leaves them unchanged, an explicit `null` or an empty array
    clears them, and a non-empty array is validated exactly like POST. Attachments are always derived
    from `content` and replace the message's attachment set: every `attachment://<file_id>` reference in
    the new content is a file id (deduplicated, first-appearance order), at most
    `api.messages.max_attachments` unique ids, each of which must exist. An edit that drops a reference
    also drops the file association (letting the GC collect it). Mentions (`mention_everyone`,
    `mentions`, `mention_roles`) are always recomputed from the new `content`; `allowed_mentions` is not
    accepted on edit because edits never notify. Returns the updated message object (the same shape as
    `GET`).

    Args:
        message_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (EditMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Message
    """

    return (
        await asyncio_detailed(
            message_id=message_id,
            client=client,
            body=body,
        )
    ).parsed
