from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.message import Message
from ...models.post_message_body import PostMessageBody
from ...types import Response


def _get_kwargs(
    channel_id: str,
    *,
    body: PostMessageBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/channels/{channel_id}/messages".format(
            channel_id=quote(str(channel_id), safe=""),
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
    channel_id: str,
    *,
    client: AuthenticatedClient,
    body: PostMessageBody,
) -> Response[Error | Message]:
    """Send a message (send_messages required)

     `content` follows `format: message-body`: it must be valid UTF-8; forbidden codepoints (controls
    except \\n/\\t, BiDi overrides, zero-width, tag characters are kept — see the conventions section)
    are stripped server-side before storage. After stripping, the content must not be empty and must not
    exceed `api.messages.max_codepoints_per_message` codepoints. An optional `reply_to_id` must
    reference an existing (not deleted) message in the same channel; a missing, deleted or other-channel
    target is rejected with 400 "'reply_to_id' is invalid". An optional `embeds` is a list of at most
    `api.messages.max_embeds` rich embeds (see the `Embed` schema); `null` or `[]` stores no embeds.
    Attachments are derived from `content`: every `attachment://<file_id>` reference yields a file id,
    deduplicated in first-appearance order. At most `api.messages.max_attachments` unique ids are
    accepted and every id must reference an existing file.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PostMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Message]
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
    body: PostMessageBody,
) -> Error | Message | None:
    """Send a message (send_messages required)

     `content` follows `format: message-body`: it must be valid UTF-8; forbidden codepoints (controls
    except \\n/\\t, BiDi overrides, zero-width, tag characters are kept — see the conventions section)
    are stripped server-side before storage. After stripping, the content must not be empty and must not
    exceed `api.messages.max_codepoints_per_message` codepoints. An optional `reply_to_id` must
    reference an existing (not deleted) message in the same channel; a missing, deleted or other-channel
    target is rejected with 400 "'reply_to_id' is invalid". An optional `embeds` is a list of at most
    `api.messages.max_embeds` rich embeds (see the `Embed` schema); `null` or `[]` stores no embeds.
    Attachments are derived from `content`: every `attachment://<file_id>` reference yields a file id,
    deduplicated in first-appearance order. At most `api.messages.max_attachments` unique ids are
    accepted and every id must reference an existing file.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PostMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Message
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
    body: PostMessageBody,
) -> Response[Error | Message]:
    """Send a message (send_messages required)

     `content` follows `format: message-body`: it must be valid UTF-8; forbidden codepoints (controls
    except \\n/\\t, BiDi overrides, zero-width, tag characters are kept — see the conventions section)
    are stripped server-side before storage. After stripping, the content must not be empty and must not
    exceed `api.messages.max_codepoints_per_message` codepoints. An optional `reply_to_id` must
    reference an existing (not deleted) message in the same channel; a missing, deleted or other-channel
    target is rejected with 400 "'reply_to_id' is invalid". An optional `embeds` is a list of at most
    `api.messages.max_embeds` rich embeds (see the `Embed` schema); `null` or `[]` stores no embeds.
    Attachments are derived from `content`: every `attachment://<file_id>` reference yields a file id,
    deduplicated in first-appearance order. At most `api.messages.max_attachments` unique ids are
    accepted and every id must reference an existing file.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PostMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Message]
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
    body: PostMessageBody,
) -> Error | Message | None:
    """Send a message (send_messages required)

     `content` follows `format: message-body`: it must be valid UTF-8; forbidden codepoints (controls
    except \\n/\\t, BiDi overrides, zero-width, tag characters are kept — see the conventions section)
    are stripped server-side before storage. After stripping, the content must not be empty and must not
    exceed `api.messages.max_codepoints_per_message` codepoints. An optional `reply_to_id` must
    reference an existing (not deleted) message in the same channel; a missing, deleted or other-channel
    target is rejected with 400 "'reply_to_id' is invalid". An optional `embeds` is a list of at most
    `api.messages.max_embeds` rich embeds (see the `Embed` schema); `null` or `[]` stores no embeds.
    Attachments are derived from `content`: every `attachment://<file_id>` reference yields a file id,
    deduplicated in first-appearance order. At most `api.messages.max_attachments` unique ids are
    accepted and every id must reference an existing file.

    Args:
        channel_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PostMessageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Message
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
            body=body,
        )
    ).parsed
