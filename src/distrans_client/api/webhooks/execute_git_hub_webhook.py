from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.execute_git_hub_webhook_data_body import ExecuteGitHubWebhookDataBody
from ...models.execute_git_hub_webhook_json_body import ExecuteGitHubWebhookJsonBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    webhook_id: str,
    token: str,
    *,
    body: ExecuteGitHubWebhookJsonBody | ExecuteGitHubWebhookDataBody | Unset = UNSET,
    x_git_hub_event: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["X-GitHub-Event"] = x_git_hub_event

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/webhooks/{webhook_id}/{token}/github".format(
            webhook_id=quote(str(webhook_id), safe=""),
            token=quote(str(token), safe=""),
        ),
    }

    if isinstance(body, ExecuteGitHubWebhookJsonBody):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, ExecuteGitHubWebhookDataBody):
        _kwargs["data"] = body.to_dict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

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
) -> Response[Any | Error]:
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
    body: ExecuteGitHubWebhookJsonBody | ExecuteGitHubWebhookDataBody | Unset = UNSET,
    x_git_hub_event: str,
) -> Response[Any | Error]:
    """Execute a GitHub-compatible webhook (token-authenticated, no session)

     GitHub integration endpoint. Configure this URL as the "Payload URL" of a repository/organization
    webhook on GitHub. The `X-GitHub-Event` header selects the event; the JSON (or `application/x-www-
    form-urlencoded` `payload=`) body is rendered into a single rich embed and posted into the webhook's
    channel as the webhook (attribution uses the webhook's configured `name`/avatar). No signature
    verification (`X-Hub-Signature*` is ignored) and no delivery deduplication: the URL token is the
    capability, exactly like `POST /webhooks/{webhook_id}/{token}`. Supported event/action combinations
    are `commit_comment/created`, `create` (branch/tag), `delete` (branch/tag), `fork`,
    `issue_comment/created`, `issues` (opened/closed/reopened), `member/added`, `public`, `pull_request`
    (opened/closed/reopened), `pull_request_review/submitted`, `pull_request_review_comment/created`,
    `push`, `release/published`, `watch/started`, `star` (created/deleted), `check_run/completed`,
    `check_suite/completed`, `discussion/created`, `discussion_comment/created`, and
    `repository/created`. For a supported combination with a valid payload, the endpoint creates one
    message. For an unsupported event, unsupported action, or incomplete payload, it creates no message
    and still responds with `204 No Content`. GitHub's `ping` event is a setup verification delivery; it
    is acknowledged with `204 No Content` and does not create a chat message. Deliveries are not
    deduplicated, so a redelivery can create another message.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        x_git_hub_event (str):
        body (ExecuteGitHubWebhookJsonBody):
        body (ExecuteGitHubWebhookDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        token=token,
        body=body,
        x_git_hub_event=x_git_hub_event,
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
    body: ExecuteGitHubWebhookJsonBody | ExecuteGitHubWebhookDataBody | Unset = UNSET,
    x_git_hub_event: str,
) -> Any | Error | None:
    """Execute a GitHub-compatible webhook (token-authenticated, no session)

     GitHub integration endpoint. Configure this URL as the "Payload URL" of a repository/organization
    webhook on GitHub. The `X-GitHub-Event` header selects the event; the JSON (or `application/x-www-
    form-urlencoded` `payload=`) body is rendered into a single rich embed and posted into the webhook's
    channel as the webhook (attribution uses the webhook's configured `name`/avatar). No signature
    verification (`X-Hub-Signature*` is ignored) and no delivery deduplication: the URL token is the
    capability, exactly like `POST /webhooks/{webhook_id}/{token}`. Supported event/action combinations
    are `commit_comment/created`, `create` (branch/tag), `delete` (branch/tag), `fork`,
    `issue_comment/created`, `issues` (opened/closed/reopened), `member/added`, `public`, `pull_request`
    (opened/closed/reopened), `pull_request_review/submitted`, `pull_request_review_comment/created`,
    `push`, `release/published`, `watch/started`, `star` (created/deleted), `check_run/completed`,
    `check_suite/completed`, `discussion/created`, `discussion_comment/created`, and
    `repository/created`. For a supported combination with a valid payload, the endpoint creates one
    message. For an unsupported event, unsupported action, or incomplete payload, it creates no message
    and still responds with `204 No Content`. GitHub's `ping` event is a setup verification delivery; it
    is acknowledged with `204 No Content` and does not create a chat message. Deliveries are not
    deduplicated, so a redelivery can create another message.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        x_git_hub_event (str):
        body (ExecuteGitHubWebhookJsonBody):
        body (ExecuteGitHubWebhookDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return sync_detailed(
        webhook_id=webhook_id,
        token=token,
        client=client,
        body=body,
        x_git_hub_event=x_git_hub_event,
    ).parsed


async def asyncio_detailed(
    webhook_id: str,
    token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecuteGitHubWebhookJsonBody | ExecuteGitHubWebhookDataBody | Unset = UNSET,
    x_git_hub_event: str,
) -> Response[Any | Error]:
    """Execute a GitHub-compatible webhook (token-authenticated, no session)

     GitHub integration endpoint. Configure this URL as the "Payload URL" of a repository/organization
    webhook on GitHub. The `X-GitHub-Event` header selects the event; the JSON (or `application/x-www-
    form-urlencoded` `payload=`) body is rendered into a single rich embed and posted into the webhook's
    channel as the webhook (attribution uses the webhook's configured `name`/avatar). No signature
    verification (`X-Hub-Signature*` is ignored) and no delivery deduplication: the URL token is the
    capability, exactly like `POST /webhooks/{webhook_id}/{token}`. Supported event/action combinations
    are `commit_comment/created`, `create` (branch/tag), `delete` (branch/tag), `fork`,
    `issue_comment/created`, `issues` (opened/closed/reopened), `member/added`, `public`, `pull_request`
    (opened/closed/reopened), `pull_request_review/submitted`, `pull_request_review_comment/created`,
    `push`, `release/published`, `watch/started`, `star` (created/deleted), `check_run/completed`,
    `check_suite/completed`, `discussion/created`, `discussion_comment/created`, and
    `repository/created`. For a supported combination with a valid payload, the endpoint creates one
    message. For an unsupported event, unsupported action, or incomplete payload, it creates no message
    and still responds with `204 No Content`. GitHub's `ping` event is a setup verification delivery; it
    is acknowledged with `204 No Content` and does not create a chat message. Deliveries are not
    deduplicated, so a redelivery can create another message.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        x_git_hub_event (str):
        body (ExecuteGitHubWebhookJsonBody):
        body (ExecuteGitHubWebhookDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        token=token,
        body=body,
        x_git_hub_event=x_git_hub_event,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: str,
    token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ExecuteGitHubWebhookJsonBody | ExecuteGitHubWebhookDataBody | Unset = UNSET,
    x_git_hub_event: str,
) -> Any | Error | None:
    """Execute a GitHub-compatible webhook (token-authenticated, no session)

     GitHub integration endpoint. Configure this URL as the "Payload URL" of a repository/organization
    webhook on GitHub. The `X-GitHub-Event` header selects the event; the JSON (or `application/x-www-
    form-urlencoded` `payload=`) body is rendered into a single rich embed and posted into the webhook's
    channel as the webhook (attribution uses the webhook's configured `name`/avatar). No signature
    verification (`X-Hub-Signature*` is ignored) and no delivery deduplication: the URL token is the
    capability, exactly like `POST /webhooks/{webhook_id}/{token}`. Supported event/action combinations
    are `commit_comment/created`, `create` (branch/tag), `delete` (branch/tag), `fork`,
    `issue_comment/created`, `issues` (opened/closed/reopened), `member/added`, `public`, `pull_request`
    (opened/closed/reopened), `pull_request_review/submitted`, `pull_request_review_comment/created`,
    `push`, `release/published`, `watch/started`, `star` (created/deleted), `check_run/completed`,
    `check_suite/completed`, `discussion/created`, `discussion_comment/created`, and
    `repository/created`. For a supported combination with a valid payload, the endpoint creates one
    message. For an unsupported event, unsupported action, or incomplete payload, it creates no message
    and still responds with `204 No Content`. GitHub's `ping` event is a setup verification delivery; it
    is acknowledged with `204 No Content` and does not create a chat message. Deliveries are not
    deduplicated, so a redelivery can create another message.

    Args:
        webhook_id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        token (str):
        x_git_hub_event (str):
        body (ExecuteGitHubWebhookJsonBody):
        body (ExecuteGitHubWebhookDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
    """

    return (
        await asyncio_detailed(
            webhook_id=webhook_id,
            token=token,
            client=client,
            body=body,
            x_git_hub_event=x_git_hub_event,
        )
    ).parsed
