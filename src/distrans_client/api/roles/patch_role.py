from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.patch_role_body import PatchRoleBody
from ...types import Response


def _get_kwargs(
    role_id: str,
    *,
    body: PatchRoleBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/roles/{role_id}".format(
            role_id=quote(str(role_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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
) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    role_id: str,
    *,
    client: AuthenticatedClient,
    body: PatchRoleBody,
) -> Response[Any | Error]:
    """Modify a role (modify_roles required)

     At least one of name / permissions / color / mentionable must be
    present; `"color": null` counts as present and clears the color. An
    explicit null in name / permissions is a 400 with the field's type
    error. The response is 204 — there are no server-derived fields to
    return. The required
    permission check includes the new permission mask: the caller may only
    grant permissions it already has (subset rule). Role hierarchy applies:
    the role's current position must be strictly below the caller's highest
    role position.
    The @everyone role (role_id = guild_id) only accepts a "permissions"
    change and is subject to the same hierarchy (its position is 0).

    Args:
        role_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        role_id=role_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    role_id: str,
    *,
    client: AuthenticatedClient,
    body: PatchRoleBody,
) -> Any | Error | None:
    """Modify a role (modify_roles required)

     At least one of name / permissions / color / mentionable must be
    present; `"color": null` counts as present and clears the color. An
    explicit null in name / permissions is a 400 with the field's type
    error. The response is 204 — there are no server-derived fields to
    return. The required
    permission check includes the new permission mask: the caller may only
    grant permissions it already has (subset rule). Role hierarchy applies:
    the role's current position must be strictly below the caller's highest
    role position.
    The @everyone role (role_id = guild_id) only accepts a "permissions"
    change and is subject to the same hierarchy (its position is 0).

    Args:
        role_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        role_id=role_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    role_id: str,
    *,
    client: AuthenticatedClient,
    body: PatchRoleBody,
) -> Response[Any | Error]:
    """Modify a role (modify_roles required)

     At least one of name / permissions / color / mentionable must be
    present; `"color": null` counts as present and clears the color. An
    explicit null in name / permissions is a 400 with the field's type
    error. The response is 204 — there are no server-derived fields to
    return. The required
    permission check includes the new permission mask: the caller may only
    grant permissions it already has (subset rule). Role hierarchy applies:
    the role's current position must be strictly below the caller's highest
    role position.
    The @everyone role (role_id = guild_id) only accepts a "permissions"
    change and is subject to the same hierarchy (its position is 0).

    Args:
        role_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        role_id=role_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    role_id: str,
    *,
    client: AuthenticatedClient,
    body: PatchRoleBody,
) -> Any | Error | None:
    """Modify a role (modify_roles required)

     At least one of name / permissions / color / mentionable must be
    present; `"color": null` counts as present and clears the color. An
    explicit null in name / permissions is a 400 with the field's type
    error. The response is 204 — there are no server-derived fields to
    return. The required
    permission check includes the new permission mask: the caller may only
    grant permissions it already has (subset rule). Role hierarchy applies:
    the role's current position must be strictly below the caller's highest
    role position.
    The @everyone role (role_id = guild_id) only accepts a "permissions"
    change and is subject to the same hierarchy (its position is 0).

    Args:
        role_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        body (PatchRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            role_id=role_id,
            client=client,
            body=body,
        )
    ).parsed
