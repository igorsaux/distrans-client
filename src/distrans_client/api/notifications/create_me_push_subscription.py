from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.push_subscription import PushSubscription
from ...models.push_subscription_input import PushSubscriptionInput
from ...types import Response


def _get_kwargs(
    *,
    body: PushSubscriptionInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/users/@me/push-subscriptions",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | PushSubscription | None:
    if response.status_code == 200:
        response_200 = PushSubscription.from_dict(response.json())

        return response_200

    if response.status_code == 201:
        response_201 = PushSubscription.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 415:
        response_415 = Error.from_dict(response.json())

        return response_415

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | PushSubscription]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PushSubscriptionInput,
) -> Response[Error | PushSubscription]:
    """Register a push subscription

     Stores a browser `PushSubscription` (from `PushManager.subscribe`). An endpoint is globally unique —
    a browser profile is logged into one account at a time — so posting an endpoint another account
    registered takes it over (reassigns it to the caller); the previous account stops receiving on that
    device. Responds `201` when the caller did not own the endpoint before (a new endpoint or a
    takeover) and `200` with the object when the caller already owned it (re-posting refreshes its
    keys). `p256dh` must be a valid uncompressed P-256 point and `auth` 16 bytes. At most
    `api.push.max_subscriptions_per_user` are stored per user; re-posting an endpoint the caller already
    owns stays allowed at the cap, but taking over another account's endpoint is `400` at the cap. No
    gateway event is dispatched.

    Args:
        body (PushSubscriptionInput): A browser `PushSubscription` to register. Registering an
            endpoint already owned by another account takes it over (moves it to the caller).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PushSubscription]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: PushSubscriptionInput,
) -> Error | PushSubscription | None:
    """Register a push subscription

     Stores a browser `PushSubscription` (from `PushManager.subscribe`). An endpoint is globally unique —
    a browser profile is logged into one account at a time — so posting an endpoint another account
    registered takes it over (reassigns it to the caller); the previous account stops receiving on that
    device. Responds `201` when the caller did not own the endpoint before (a new endpoint or a
    takeover) and `200` with the object when the caller already owned it (re-posting refreshes its
    keys). `p256dh` must be a valid uncompressed P-256 point and `auth` 16 bytes. At most
    `api.push.max_subscriptions_per_user` are stored per user; re-posting an endpoint the caller already
    owns stays allowed at the cap, but taking over another account's endpoint is `400` at the cap. No
    gateway event is dispatched.

    Args:
        body (PushSubscriptionInput): A browser `PushSubscription` to register. Registering an
            endpoint already owned by another account takes it over (moves it to the caller).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PushSubscription
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PushSubscriptionInput,
) -> Response[Error | PushSubscription]:
    """Register a push subscription

     Stores a browser `PushSubscription` (from `PushManager.subscribe`). An endpoint is globally unique —
    a browser profile is logged into one account at a time — so posting an endpoint another account
    registered takes it over (reassigns it to the caller); the previous account stops receiving on that
    device. Responds `201` when the caller did not own the endpoint before (a new endpoint or a
    takeover) and `200` with the object when the caller already owned it (re-posting refreshes its
    keys). `p256dh` must be a valid uncompressed P-256 point and `auth` 16 bytes. At most
    `api.push.max_subscriptions_per_user` are stored per user; re-posting an endpoint the caller already
    owns stays allowed at the cap, but taking over another account's endpoint is `400` at the cap. No
    gateway event is dispatched.

    Args:
        body (PushSubscriptionInput): A browser `PushSubscription` to register. Registering an
            endpoint already owned by another account takes it over (moves it to the caller).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PushSubscription]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: PushSubscriptionInput,
) -> Error | PushSubscription | None:
    """Register a push subscription

     Stores a browser `PushSubscription` (from `PushManager.subscribe`). An endpoint is globally unique —
    a browser profile is logged into one account at a time — so posting an endpoint another account
    registered takes it over (reassigns it to the caller); the previous account stops receiving on that
    device. Responds `201` when the caller did not own the endpoint before (a new endpoint or a
    takeover) and `200` with the object when the caller already owned it (re-posting refreshes its
    keys). `p256dh` must be a valid uncompressed P-256 point and `auth` 16 bytes. At most
    `api.push.max_subscriptions_per_user` are stored per user; re-posting an endpoint the caller already
    owns stays allowed at the cap, but taking over another account's endpoint is `400` at the cap. No
    gateway event is dispatched.

    Args:
        body (PushSubscriptionInput): A browser `PushSubscription` to register. Registering an
            endpoint already owned by another account takes it over (moves it to the caller).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PushSubscription
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
