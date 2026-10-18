from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.file_upload import FileUpload
from ...types import UNSET, File, Response


def _get_kwargs(
    *,
    body: File,
    name: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/files",
        "params": params,
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | FileUpload | None:
    if response.status_code == 200:
        response_200 = FileUpload.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = FileUpload.from_dict(response.json())

        return response_201

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | FileUpload]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: File,
    name: str,
) -> Response[Error | FileUpload]:
    """Upload a file

     Uploads a file and stores it as an immutable object in S3. The body must be non-empty and its
    `Content-Type` must be allowed by `files.whitelist` (`null` allows every type, an empty list allows
    none; otherwise only the listed patterns, where an exact `type/subtype` matches that type and a
    `<type>/*` entry such as `text/*` matches any subtype of that type). The default whitelist is
    `image/webp`, `image/gif`, `image/png`, `image/jpeg`, `image/jpg`, `text/*`. Supported raster types
    (WebP/GIF/PNG/JPEG) are re-encoded to WebP (container metadata is dropped) and stored with `Content-
    Type: image/webp`; the body of a re-encoded type must not exceed `media.files.max_input_bytes`, and
    a still JPEG is rotated to honor its EXIF orientation. All other whitelisted types are stored raw
    with the request `Content-Type`, and their metadata is preserved. The body must not exceed
    `files.max_size`. The object key is `files/{hash}` where `hash` is the hex SHA-256 of the final
    (possibly re-encoded) bytes, so re-uploading identical bytes reuses the existing file (no second
    upload). Stored objects are immutable and served with `Cache-Control: public, max-age=31536000,
    immutable` and `Content-Disposition: attachment` carrying the sanitized original name as `filename`
    (ASCII fallback) plus `filename*=UTF-8''<percent-encoded>` (RFC 6266/5987), so navigating to
    `public_url` saves the file under its original name. Embedded resources (`<img>`/`<video>`/`<audio
    src>`) ignore `Content-Disposition`, so inline rendering and playback are unaffected. The `hash` is
    `UNIQUE`, so an object always corresponds to a single `File` row and name. Responds with the file
    metadata and its hash. A file that no message ever references is deleted by the background GC once
    it is older than `files.gc.grace_s` (the row first, then the S3 object); uploaded-but-unattached
    files are therefore temporary. Responds `201 Created` when a new file row is inserted, or `200 OK`
    when the same bytes already exist and the row is reused.

    Args:
        name (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FileUpload]
    """

    kwargs = _get_kwargs(
        body=body,
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: File,
    name: str,
) -> Error | FileUpload | None:
    """Upload a file

     Uploads a file and stores it as an immutable object in S3. The body must be non-empty and its
    `Content-Type` must be allowed by `files.whitelist` (`null` allows every type, an empty list allows
    none; otherwise only the listed patterns, where an exact `type/subtype` matches that type and a
    `<type>/*` entry such as `text/*` matches any subtype of that type). The default whitelist is
    `image/webp`, `image/gif`, `image/png`, `image/jpeg`, `image/jpg`, `text/*`. Supported raster types
    (WebP/GIF/PNG/JPEG) are re-encoded to WebP (container metadata is dropped) and stored with `Content-
    Type: image/webp`; the body of a re-encoded type must not exceed `media.files.max_input_bytes`, and
    a still JPEG is rotated to honor its EXIF orientation. All other whitelisted types are stored raw
    with the request `Content-Type`, and their metadata is preserved. The body must not exceed
    `files.max_size`. The object key is `files/{hash}` where `hash` is the hex SHA-256 of the final
    (possibly re-encoded) bytes, so re-uploading identical bytes reuses the existing file (no second
    upload). Stored objects are immutable and served with `Cache-Control: public, max-age=31536000,
    immutable` and `Content-Disposition: attachment` carrying the sanitized original name as `filename`
    (ASCII fallback) plus `filename*=UTF-8''<percent-encoded>` (RFC 6266/5987), so navigating to
    `public_url` saves the file under its original name. Embedded resources (`<img>`/`<video>`/`<audio
    src>`) ignore `Content-Disposition`, so inline rendering and playback are unaffected. The `hash` is
    `UNIQUE`, so an object always corresponds to a single `File` row and name. Responds with the file
    metadata and its hash. A file that no message ever references is deleted by the background GC once
    it is older than `files.gc.grace_s` (the row first, then the S3 object); uploaded-but-unattached
    files are therefore temporary. Responds `201 Created` when a new file row is inserted, or `200 OK`
    when the same bytes already exist and the row is reused.

    Args:
        name (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FileUpload
    """

    return sync_detailed(
        client=client,
        body=body,
        name=name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: File,
    name: str,
) -> Response[Error | FileUpload]:
    """Upload a file

     Uploads a file and stores it as an immutable object in S3. The body must be non-empty and its
    `Content-Type` must be allowed by `files.whitelist` (`null` allows every type, an empty list allows
    none; otherwise only the listed patterns, where an exact `type/subtype` matches that type and a
    `<type>/*` entry such as `text/*` matches any subtype of that type). The default whitelist is
    `image/webp`, `image/gif`, `image/png`, `image/jpeg`, `image/jpg`, `text/*`. Supported raster types
    (WebP/GIF/PNG/JPEG) are re-encoded to WebP (container metadata is dropped) and stored with `Content-
    Type: image/webp`; the body of a re-encoded type must not exceed `media.files.max_input_bytes`, and
    a still JPEG is rotated to honor its EXIF orientation. All other whitelisted types are stored raw
    with the request `Content-Type`, and their metadata is preserved. The body must not exceed
    `files.max_size`. The object key is `files/{hash}` where `hash` is the hex SHA-256 of the final
    (possibly re-encoded) bytes, so re-uploading identical bytes reuses the existing file (no second
    upload). Stored objects are immutable and served with `Cache-Control: public, max-age=31536000,
    immutable` and `Content-Disposition: attachment` carrying the sanitized original name as `filename`
    (ASCII fallback) plus `filename*=UTF-8''<percent-encoded>` (RFC 6266/5987), so navigating to
    `public_url` saves the file under its original name. Embedded resources (`<img>`/`<video>`/`<audio
    src>`) ignore `Content-Disposition`, so inline rendering and playback are unaffected. The `hash` is
    `UNIQUE`, so an object always corresponds to a single `File` row and name. Responds with the file
    metadata and its hash. A file that no message ever references is deleted by the background GC once
    it is older than `files.gc.grace_s` (the row first, then the S3 object); uploaded-but-unattached
    files are therefore temporary. Responds `201 Created` when a new file row is inserted, or `200 OK`
    when the same bytes already exist and the row is reused.

    Args:
        name (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FileUpload]
    """

    kwargs = _get_kwargs(
        body=body,
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: File,
    name: str,
) -> Error | FileUpload | None:
    """Upload a file

     Uploads a file and stores it as an immutable object in S3. The body must be non-empty and its
    `Content-Type` must be allowed by `files.whitelist` (`null` allows every type, an empty list allows
    none; otherwise only the listed patterns, where an exact `type/subtype` matches that type and a
    `<type>/*` entry such as `text/*` matches any subtype of that type). The default whitelist is
    `image/webp`, `image/gif`, `image/png`, `image/jpeg`, `image/jpg`, `text/*`. Supported raster types
    (WebP/GIF/PNG/JPEG) are re-encoded to WebP (container metadata is dropped) and stored with `Content-
    Type: image/webp`; the body of a re-encoded type must not exceed `media.files.max_input_bytes`, and
    a still JPEG is rotated to honor its EXIF orientation. All other whitelisted types are stored raw
    with the request `Content-Type`, and their metadata is preserved. The body must not exceed
    `files.max_size`. The object key is `files/{hash}` where `hash` is the hex SHA-256 of the final
    (possibly re-encoded) bytes, so re-uploading identical bytes reuses the existing file (no second
    upload). Stored objects are immutable and served with `Cache-Control: public, max-age=31536000,
    immutable` and `Content-Disposition: attachment` carrying the sanitized original name as `filename`
    (ASCII fallback) plus `filename*=UTF-8''<percent-encoded>` (RFC 6266/5987), so navigating to
    `public_url` saves the file under its original name. Embedded resources (`<img>`/`<video>`/`<audio
    src>`) ignore `Content-Disposition`, so inline rendering and playback are unaffected. The `hash` is
    `UNIQUE`, so an object always corresponds to a single `File` row and name. Responds with the file
    metadata and its hash. A file that no message ever references is deleted by the background GC once
    it is older than `files.gc.grace_s` (the row first, then the S3 object); uploaded-but-unattached
    files are therefore temporary. Responds `201 Created` when a new file row is inserted, or `200 OK`
    when the same bytes already exist and the row is reused.

    Args:
        name (str):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FileUpload
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            name=name,
        )
    ).parsed
