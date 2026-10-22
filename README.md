# distrans-client

Low-level Python client for the [Distrans](https://github.com/igorsaux/distrans) chat API,
generated from [`openapi/openapi.yml`](openapi/openapi.yml) with
[`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client).

The package targets Python 3.11+, uses `httpx` for HTTP transport, `attrs` for models and
`websockets` for the realtime gateway. It ships both synchronous and asynchronous variants
of every operation, plus `DistransClient` / `AsyncDistransClient` facades and typed
WebSocket gateway clients.

## Install

```sh
uv add distrans-client
# or
pip install distrans-client
```

For development:

```sh
uv sync
```

## Quick start

Distrans is self-hosted, so `base_url` is required and points at your deployment's API root
including the `/api` prefix:

```python
from distrans_client import DistransClient
from distrans_client.api.meta import get_limits

with DistransClient("https://chat.example.com/api") as client:
    limits = get_limits.sync(client=client.raw)
    print(limits.messages.max_codepoints_per_message)

    token = client.login("alice", "secret")
    print(token.access_token, token.expires_in)
```

`DistransClient` owns a single `httpx.Client`, so the connection pool and cookie jar (including
the HttpOnly `refresh_token` cookie) survive between calls:

```python
with DistransClient("https://chat.example.com/api") as client:
    client.login("alice", "secret")
    client.refresh()  # rotates the cookie and updates the access token
    client.logout()  # revokes the refresh token
```

Cookies issued with `Secure` are not sent over plain `http://`. Run the server behind HTTPS
(or inject the cookie manually) if you need `refresh`/`logout` against a local HTTP server.

## Calling generated operations

Every operation lives under `distrans_client.api.<tag>` and exposes four entry points:

| Function | Returns |
| --- | --- |
| `sync(...)` | Parsed model, or `Error` for a documented error status |
| `sync_detailed(...)` | `Response` with status, headers, raw bytes and parsed body |
| `asyncio(...)` | Awaitable parsed model |
| `asyncio_detailed(...)` | Awaitable `Response` |

```python
from distrans_client.api.messages import get_messages, post_message
from distrans_client.models.post_message_body import PostMessageBody

messages = get_messages.sync(client=client.raw, channel_id="123", limit=50)
created = post_message.sync(
    client=client.raw,
    channel_id="123",
    body=PostMessageBody(content="hello"),
)
```

Documented non-2xx responses are returned as `distrans_client.models.Error` instead of being
raised, matching the generator's defaults. Pass `raise_on_unexpected_status=False` to
`DistransClient` if you prefer `None` for undocumented statuses.

Model fields follow the OpenAPI contract. Wire names that collide with Python keywords gain a
trailing underscore (`hash_`, `type_`); use `to_dict()` / `from_dict()` to move between models
and JSON.

## Binary uploads

The generated endpoints send `Content-Type: application/octet-stream` for raw bodies. The
server validates the request `Content-Type` against `files.whitelist` (and against the allowed
image types for avatars and emoji icons), so always pass the real media type. The wrapper
overrides the header for you:

```python
with open("photo.png", "rb") as fh:
    upload = client.upload_file("photo.png", fh.read(), "image/png")
    print(upload.public_url)

client.set_my_avatar(png_bytes, "image/png")
client.set_guild_avatar(guild_id, png_bytes, "image/png")
client.create_emoji(guild_id, "party", png_bytes, "image/png")
client.set_emoji_icon(emoji_id, gif_bytes, "image/gif")
client.set_webhook_avatar(webhook_id, webp_bytes, "image/webp")
```

Files are served by the S3 public URL, not by the API host.

## Downloads

Public files live on S3, not on the API host. Use `download` or `download_attachment`:
the client keeps a separate `httpx` client for downloads and never sends the API
`Authorization` header or the API cookie jar. Attaching a bot token to a public S3 URL
makes S3 reject the request with `400`.

```python
data = client.download("https://files.example.com/files/abc")

for attachment in message.attachments:
    if attachment.public_url is not None:
        data = client.download_attachment(attachment)
```

Downloads follow redirects, use `download_timeout` (30 seconds by default), and retry
safe `GET` requests. A non-2xx response raises `DistransDownloadError` with `url`,
`status_code` and `message`; network failures propagate as `httpx.TransportError` (or
`httpx.TimeoutException`). `client.download_http` exposes the separate client if you need
a custom timeout; do not use `client.http` for public file URLs.

## Custom emojis and mentions

```python
from distrans_client import emoji_token, no_mentions

for emoji in client.iter_guild_emojis(guild_id):
    print(emoji_token(emoji))  # "<:name:id>"

client.send_message(channel_id, "hello @here", allowed_mentions=no_mentions())
```

`no_mentions()` returns a fresh `AllowedMentions(parse=[])` on every call. Do not keep a
shared instance.

## Pagination

The facade exposes explicit iterators rather than a generic paginator:

```python
for emoji in client.iter_guild_emojis(guild_id):
    ...

for message in client.iter_messages_after(channel_id, after=last_seen_id):
    ...  # oldest to newest

for message in client.iter_messages_before(channel_id):
    ...  # newest to oldest; omit `before` to start at the latest message

for message in client.iter_pinned_messages_after(channel_id, after=last_seen_id):
    ...  # oldest to newest

for message in client.iter_pinned_messages_before(channel_id):
    ...  # newest to oldest; omit `before` to start at the latest pinned message
```

`page_size` defaults to `100` and must be between `1` and `100`; other values raise
`ValueError`. Iterators stop on an empty page or when the keyset cursor stops advancing.
They also tolerate servers configured with a lower message limit, so a short page is not
treated as the end of history. A documented error page raises `DistransAPIError`.
Pinned-message iterators return only pinned, non-deleted messages and are also available
on `AsyncDistransClient`.

## Sending messages and replies

```python
message = client.send_message(
    channel_id,
    "hello",
    allowed_mentions=no_mentions(),
)
reply = client.reply(channel_id, message.id, "world", allowed_mentions=no_mentions())
```

`send_message` accepts `reply_to_id`, `embeds` and `allowed_mentions`, and returns the
created `Message`. If a reply target is rejected with `400` and the error message mentions
`reply_to_id`, the client retries once without the reply target. Other `400`s and all other
errors raise `DistransAPIError`.

## Webhook messages

Webhook message operations use the webhook execute token and require no session or channel
permission check:

```python
message = client.get_webhook_message(webhook_id, token, message_id)
edited = client.edit_webhook_message(webhook_id, token, message_id, content="updated")
client.edit_webhook_message(webhook_id, token, message_id, embeds=None)  # clear embeds
client.delete_webhook_message(webhook_id, token, message_id)
```

`edit_webhook_message` accepts `content` and/or `embeds`; omitted fields keep their stored
values, and `embeds=None` or `[]` clears them. `AsyncDistransClient` mirrors these methods.

## Retries

Retries are disabled by default for the API. Enable them with a `RetryPolicy`:

```python
from distrans_client import DistransClient, RetryPolicy

client = DistransClient(
    "https://chat.example.com/api",
    token="bot_...",
    retry=RetryPolicy(attempts=2),
)
```

Only `GET`, `HEAD` and `OPTIONS` are retried by default, so a retry cannot duplicate a
message. Adding `POST` to `methods` makes retries at-least-once: the server may have
created the message even though the response was lost. Retries also apply to
`httpx.TransportError`, honor integer `Retry-After` seconds, and use exponential backoff
with jitter. The policy is implemented as a transport wrapper, so generated operations
work unchanged. Downloads retry `GET` twice by default; pass `download_retry=None` to
disable that.

## Errors

```python
from distrans_client import DistransAPIError

try:
    client.set_guild_avatar(guild_id, png_bytes, "image/png")
except DistransAPIError as exc:
    print(exc.status_code, exc.message)  # e.g. 403 Missing permissions
```

## WebSocket gateway

`GET /gateway` is an HTTP upgrade; the generated HTTP functions cannot use it. The
package wraps the JSON frame protocol (`identify`, `hello`, periodic `ack`, then
`dispatch` events) with a typed client:

```python
from distrans_client import DistransClient, GatewayEventType

with DistransClient("https://chat.example.com/api") as client:
    client.login("alice", "secret")

    with client.gateway() as gateway:
        for event in gateway:
            if event.type is GatewayEventType.MESSAGE_CREATED:
                print(event.seq, event.channel_id, event.message_id)
```

`client.gateway()` returns a `Gateway`. It connects lazily (on `with`, `connect()`,
or the first `recv()`/iteration), sends `identify` with the client's current access
token (JWT or a static `bot_` token), waits for `hello`, and then acknowledges the
server heartbeat from a background thread. Slow consumers therefore do not get
dropped, and `refresh()` is picked up on the next connection attempt.

- `recv(timeout=None)` returns the next dispatch event. It raises the built-in
  `TimeoutError` when no event arrives in time.
- Iterating (`for event in gateway`) is the same as calling `recv()` repeatedly.
- Dispatch payloads are parsed into `MessageEvent`, `MessageReactionEvent`,
  `UserEvent`, `GuildEvent`, `ChannelEvent`, `ChannelsReorderedEvent`,
  `RoleEvent`, `RoleAssignmentEvent`, `RolesReorderedEvent`, `EmojiEvent`,
  `OverwriteEvent` and `WebhookEvent`. Unknown server event types are returned as
  `UnknownDispatchEvent` instead of being dropped.
- `GatewayClosedError` carries the close `code`/`reason`; `GatewayAuthError`
  means the server refused `identify`; `GatewayProtocolError` means a malformed
  frame.

The server does not replay missed events, so reconnection is off by default:

```python
def resync(gateway):
    print("reconnected; refetch /guilds/{id}/sync and channel message syncs")


with client.gateway(auto_reconnect=True, on_reconnect=resync) as gateway:
    for event in gateway:
        ...
```

`auto_reconnect` retries transient failures with exponential backoff, calls
`token_provider` (by default the client's current token) before each attempt, and
invokes `on_reconnect` after a new `hello`. Use it together with an explicit
resync in `on_reconnect`, because events produced while disconnected are lost.

`Gateway` can also be constructed directly with a full WebSocket URL from
`distrans_client.gateway.gateway_url(base_url)` and a `token` or `token_provider`.

## Async client

`AsyncDistransClient` mirrors `DistransClient` for asyncio: `login`, `refresh`,
`logout`, `upload_file`, the avatar/emoji/webhook helpers, downloads, message
sending/replies, pagination, retries, and `gateway()`:

```python
from distrans_client import AsyncDistransClient, GatewayEventType

async with AsyncDistransClient("https://chat.example.com/api") as client:
    await client.login("alice", "secret")

    async with client.gateway() as gateway:
        async for event in gateway:
            if event.type is GatewayEventType.MESSAGE_CREATED:
                print(event.message_id)
```

Every generated operation still exposes `asyncio()` / `asyncio_detailed()`, so
`client.raw` can be used directly for endpoints without a facade helper. The
gateway accepts sync or async `token_provider` and `on_reconnect` callbacks.

## Updating the client

The client is generated from a vendored copy of the backend contract. Never edit
`src/distrans_client/api/`, `models/`, `client.py`, `errors.py` or `types.py` by hand: every
regeneration replaces them. Hand-written code stays in `facade.py`, `async_facade.py`,
`exceptions.py`, `helpers.py`, `retry.py` and `__init__.py`.

### 1. Sync the contract

Copy the spec from the backend repository and review the diff before generating:

```sh
cp ../distrans/docs/openapi.yml openapi/openapi.yml
git diff -- openapi/openapi.yml
```

`openapi/openapi.yml` is the only source of truth for the client. If the backend change is
externally visible, `info.version` in the contract should change too. The package version in
`pyproject.toml` may be ahead of `info.version` for client-only additions (the WebSocket
gateway wrapper and `AsyncDistransClient` do not change the HTTP contract). Use semver:
breaking wire changes bump the major version.

### 2. Regenerate

```sh
uv run python scripts/generate.py
```

The script runs the pinned `openapi-python-client` version (`0.29.1`, see
`DEFAULT_GENERATOR_VERSION` in `scripts/generate.py`) through `uvx`, copies the generated
artifacts into `src/distrans_client/`, and applies one workaround for a known generator bug
(missing `Unset` import in operations with an optional union body).

Review the result:

```sh
git diff --stat
git diff -- src/distrans_client
```

Generated directories and files are replaced wholesale, so removed schemas disappear on their
own. Only hand-written code needs attention: update `facade.py` if it imports a model or
endpoint that changed, then re-run `uv sync` if dependencies changed.

### 3. Verify

```sh
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/generate.py --check
```

`--check` regenerates into a temporary directory and compares it with the committed artifacts.
CI runs the same command, so a stale client fails the build instead of shipping silently.

Optional integration run against a live server:

```sh
DISTRANS_BASE_URL=http://localhost:8080/api \
DISTRANS_USERNAME=alice DISTRANS_PASSWORD=secret \
uv run pytest -m integration
```

### 4. Bump the generator

The generator version is pinned because `openapi-python-client` is still 0.x and minor releases
change generated behavior. To upgrade, pass a new version, regenerate, and review the diff as
usual:

```sh
uv run python scripts/generate.py --generator-version 0.30.0
```

Then update `DEFAULT_GENERATOR_VERSION` in `scripts/generate.py` so `--check` and CI use the
same version.

## Layout

```
openapi/openapi.yml              vendored API contract
scripts/generate.py              generator driver (pinned to openapi-python-client 0.29.1)
src/distrans_client/api/         generated operation modules (do not edit)
src/distrans_client/models/      generated models (do not edit)
src/distrans_client/client.py    generated transport client (do not edit)
src/distrans_client/facade.py    DistransClient facade: auth, uploads, downloads,
                                 messages, pagination, gateway()
src/distrans_client/async_facade.py  AsyncDistransClient: asyncio auth, uploads,
                                 downloads, messages, pagination, gateway()
src/distrans_client/gateway/     WebSocket protocol, sync/async gateway, typed events
src/distrans_client/helpers.py   emoji_token and no_mentions helpers
src/distrans_client/retry.py     optional RetryPolicy and httpx transport wrappers
src/distrans_client/exceptions.py
tests/                           unit tests with httpx.MockTransport, local WebSocket servers,
                                 optional integration tests
```

## Credentials and base URL

Distrans is self-hosted: there is no default host. Always pass the API root, including the
`/api` prefix (`https://chat.example.com/api`). The client never reads environment variables
implicitly; configuration stays explicit.

## Integration tests

```sh
DISTRANS_BASE_URL=http://localhost:8080/api \
DISTRANS_USERNAME=alice DISTRANS_PASSWORD=secret \
uv run pytest -m integration
```

Integration tests are skipped when `DISTRANS_BASE_URL` is not set.

## License

Apache-2.0, matching the Distrans API contract.
