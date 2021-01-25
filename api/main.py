from __future__ import annotations

import azure.functions as func
import requests
import logging
import os
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
    r = requests.get(f"{API_ENDPOINT}/{resource}")
    logging.info("response for %s: %s", resource, r.status_code)
    r.raise_for_status()
    return r.json()


def get_role_count(guild, req):
    roles = get_discord(f"guilds/{guild}/roles")
    members = get_discord(f"guilds/{guild}/members?limit=1000")
    counts = {}
    for m in members:
        for r in m["roles"]:
            counts[r] = counts.get(r, 0) + 1
    return {roles[k]: v for k, v in counts.items()}


def main(req: func.HttpRequest) -> func.HttpResponse:
    guild = get_guild(req)
    what = req.params.get("what")
    try:
        if what == "role_count":
            r = get_role_count(guild, req)
        else:
            return error_resp("'what' parameter is required", 400)
    except requests.exceptions.HTTPError as ex:
        return error_resp(f"Discord error: {ex}", 400)

    if isinstance(r, dict):
        return func.HttpResponse(r, mimetype="application/json")
    return r
