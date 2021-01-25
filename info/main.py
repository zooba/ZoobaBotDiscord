from __future__ import annotations

import azure.functions as func
import json
import logging
import os
import requests
import sys

API_ENDPOINT = "https://discord.com/api/v8"
AUTH_HEADER = {"Authorization": os.getenv("AUTHORIZATION")}


def error_resp(message, code=400):
    return func.HttpResponse(message, status_code=400)


def get_guild(req):
    if not AUTH_HEADER.get("Authorization"):
        return error_resp("authorization not configured")
    guild = req.params.get("guild")
    if not guild:
        return error_resp("guild parameter is required")
    try:
        return int(guild)
    except Exception:
        logging.exception("invalid guild value %s", guild)
        return error_resp("guild parameter is invalid")


def get_discord(resource):
    r = requests.get(f"{API_ENDPOINT}/{resource}", headers=AUTH_HEADER)
    logging.info("response for %s: %s", resource, r.status_code)
    r.raise_for_status()
    return r.json()


def get_role_names(req):
    guild = get_guild(req)
    roles = {r["id"]: r["name"] for r in get_discord(f"guilds/{guild}/roles")}
    key = req.params.get("role.id")
    if key:
        try:
            return str(roles[key])
        except KeyError:
            return key
    return roles


def get_role_count(req):
    guild = get_guild(req)
    roles = {r["id"]: r["name"] for r in get_discord(f"guilds/{guild}/roles")}
    members = get_discord(f"guilds/{guild}/members?limit=1000")
    counts = {}
    for m in members:
        for r in m["roles"]:
            counts[r] = counts.get(r, 0) + 1
    key = req.params.get("role.id")
    if key:
        try:
            return str(counts[key])
        except KeyError:
            return "0"
    return counts


HANDLERS = {
    "roles": get_role_names,
    "role_count": get_role_count,
}


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        what = req.route_params.get("what")
        try:
            fn = HANDLERS[what]
        except KeyError:
            return error_resp(
                "Supported APIs are {}".format(", ".join(HANDLERS)),
                404,
            )
        r = fn(req)
        if isinstance(r, dict):
            return func.HttpResponse(json.dumps(r), mimetype="application/json")
        return r
    except requests.exceptions.HTTPError as ex:
        logging.exception("Discord error")
        return error_resp(f"Discord error: {ex}", 400)
    except Exception as ex:
        logging.exception("Internal error")
        raise

