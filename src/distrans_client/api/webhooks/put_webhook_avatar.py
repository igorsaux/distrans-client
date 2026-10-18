from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.put_webhook_avatar_response_200 import PutWebhookAvatarResponse200
from ...types import File, Response


def _get_kwargs(
    webhook_id: str,
    *,
    body: File,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/webhooks/{webhook_id}/avatar".format(
            webhook_id=quote(str(webhook_id), safe=""),
        ),
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | PutWebhookAvatarResponse200 | None:
    if response.status_code == 200:
        response_200 = PutWebhookAvatarResponse200.from_dict(response.json())

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
) -> Response[Error | PutWebhookAvatarResponse200]:
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
    body: File,
) -> Response[Error | PutWebhookAvatarResponse200]:
    """Set a webhook avatar (modify_webhooks required)

     Uploads a raw image body and stores the re-encoded WebP avatar. The body must be non-empty with a
    supported raster `Content-Type` (`image/webp`, `image/gif`, `image/png`, `image/jpeg`, `image/jpg`);
    otherwise `400 "Bad image"` / `415`. An unsupported/empty body is rejected before any encoding. A
    body over `media.avatar.max_input_bytes` is 413 "Image is too large"; an image that is not a valid
    WebP/GIF/PNG/JPEG within the `media.avatar` dimension and animation caps is 400 "Bad image". A still
    JPEG is rotated to honor its EXIF orientation. A soft-deleted webhook is 404. Dispatches a
    `webhook_updated` gateway event.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PutWebhookAvatarResponse200]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    webhook_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Error | PutWebhookAvatarResponse200 | None:
    """Set a webhook avatar (modify_webhooks required)

     Uploads a raw image body and stores the re-encoded WebP avatar. The body must be non-empty with a
    supported raster `Content-Type` (`image/webp`, `image/gif`, `image/png`, `image/jpeg`, `image/jpg`);
    otherwise `400 "Bad image"` / `415`. An unsupported/empty body is rejected before any encoding. A
    body over `media.avatar.max_input_bytes` is 413 "Image is too large"; an image that is not a valid
    WebP/GIF/PNG/JPEG within the `media.avatar` dimension and animation caps is 400 "Bad image". A still
    JPEG is rotated to honor its EXIF orientation. A soft-deleted webhook is 404. Dispatches a
    `webhook_updated` gateway event.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PutWebhookAvatarResponse200
    """

    return sync_detailed(
        webhook_id=webhook_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    webhook_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Response[Error | PutWebhookAvatarResponse200]:
    """Set a webhook avatar (modify_webhooks required)

     Uploads a raw image body and stores the re-encoded WebP avatar. The body must be non-empty with a
    supported raster `Content-Type` (`image/webp`, `image/gif`, `image/png`, `image/jpeg`, `image/jpg`);
    otherwise `400 "Bad image"` / `415`. An unsupported/empty body is rejected before any encoding. A
    body over `media.avatar.max_input_bytes` is 413 "Image is too large"; an image that is not a valid
    WebP/GIF/PNG/JPEG within the `media.avatar` dimension and animation caps is 400 "Bad image". A still
    JPEG is rotated to honor its EXIF orientation. A soft-deleted webhook is 404. Dispatches a
    `webhook_updated` gateway event.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PutWebhookAvatarResponse200]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: str,
    *,
    client: AuthenticatedClient,
    body: File,
) -> Error | PutWebhookAvatarResponse200 | None:
    """Set a webhook avatar (modify_webhooks required)

     Uploads a raw image body and stores the re-encoded WebP avatar. The body must be non-empty with a
    supported raster `Content-Type` (`image/webp`, `image/gif`, `image/png`, `image/jpeg`, `image/jpg`);
    otherwise `400 "Bad image"` / `415`. An unsupported/empty body is rejected before any encoding. A
    body over `media.avatar.max_input_bytes` is 413 "Image is too large"; an image that is not a valid
    WebP/GIF/PNG/JPEG within the `media.avatar` dimension and animation caps is 400 "Bad image". A still
    JPEG is rotated to honor its EXIF orientation. A soft-deleted webhook is 404. Dispatches a
    `webhook_updated` gateway event.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PutWebhookAvatarResponse200
    """

    return (
        await asyncio_detailed(
            webhook_id=webhook_id,
            client=client,
            body=body,
        )
    ).parsed
