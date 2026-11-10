# Party Mode shared room

This build puts all Party Mode users in one private relay room and enables Party
Mode automatically once Rose and League are ready. The existing toggle remains
available for disabling and re-enabling it.

## Private group build

This private build embeds one cryptographically generated 32-character
lowercase hexadecimal room key. No environment variable or `config.ini` value
is needed. All four users must install the exact same private build; ordinary
Rose builds and other modified builds use different room keys.

The key is a bearer secret. Do not publish the source, binary, screenshots of
the source, logs containing it, or the key itself. Anyone who obtains the source
or binary can recover the key and join the room. To rotate the room, generate a
new key with `python -c "import secrets; print(secrets.token_hex(16))"`, replace
`SHARED_ROOM_KEY` in `party/core/party_storage.py`, rebuild, and distribute the
new private build to all four users.

## Use the room

1. Install the same private Rose build on all four computers.
2. Start League if it is not already running.
3. Start or restart Rose.
4. Wait for Party Mode to auto-enable and the relay connection to become online;
   all four users should appear
   without pasting tokens.
5. Enter the same lobby and champion select, choose skins or custom mods, and
   verify that the selections appear for the matching champions.

Tokens remain supported. Pasting an existing valid token still decodes the
friend identity, but this build routes the join to the embedded shared room
instead of the friend's old per-account room.

## Compatibility and security

All members should use the same modified build and the same relay URL/version
compatibility. The relay supports at most 10 simultaneous connections per room,
so four users fit. A room key is a bearer secret; the relay does not authenticate
members separately. If the key is exposed, generate a replacement and update
all four installations.

Older Rose versions can still decode the existing token format and retain their
legacy per-account room behavior, but they will not automatically appear in the
new shared room unless they also run this shared-room change with the same key.
The skin and custom-mod hash protocol is unchanged, so modified clients retain
those features and remain compatible with the existing relay protocol.

## Startup behavior

Rose schedules a persistent Party Mode supervisor after the bridge and League
WebSocket are ready. It does not block startup and keeps retrying if League or
the relay is temporarily unavailable. It also resumes stopped relay connections
and re-enables Party Mode if it was manually disabled. The supervisor stops only
when Rose shuts down.
