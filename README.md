# ZoobaBotDiscord
My own Discord bot, for fun and troublemaking

To add my bot, follow this link: https://discord.com/oauth2/authorize?client_id=803285375048613968&scope=bot

Currently, my bot does not require any permissions, but it _does_ have the right to list all members of your server. Also, you can't use it without getting an API key from me, so you probably don't want this at all unless I've sent you here myself.

# APIs

Current APIs are:

## Role list

``https://zoobabot.azurewebsites.net/api/v1/info/roles?guild=GUILD_ID``

Returns a JSON object mapping role IDs to names. Add the `role.id=ROLE_ID` parameter to just return the name of a specific role.

## Role count

``https://zoobabot.azurewebsites.net/api/v1/info/role_count?guild=GUILD_ID``

Returns a JSON object mapping role IDs to the number of members with each role. Add the `role.id=ROLE_ID` parameter to just get the number of members with that role.

(This one will probably break or be incorrect on servers with more than 1000 members.)

# Authorization

To access these API, I will have given you an API key. Either pass this key as `x-function-key: <KEY>` header, or as the `code=<KEY>` URL parameter.

# Contributions

Contributions are welcome, but not guaranteed to be merged. Because this is a live service that I own and pay for, I won't merge anything I'm not comfortable with fully owning myself and being responsible for.
