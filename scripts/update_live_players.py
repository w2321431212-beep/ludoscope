#!/usr/bin/env python3
"""Collect approximate-current Steam players for a monitored subset of games.
Only public Steam Web API data are queried. The page labels these as a limited
candidate ranking, not a ranking of all games or an exact point-in-time census.
"""
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "catalog.js"
OUTPUT = ROOT / "live_players.json"
LIMIT = 40
API_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={}"


def candidate_ids():
    content = SOURCE.read_text(encoding="utf-8").strip()
    prefix = "window.LUDOSCOPE_DATA="
    if not content.startswith(prefix):
        raise RuntimeError("Unexpected catalog.js data format")
    source = json.loads(content[len(prefix):].rstrip(";"))
    cols = {name: i for i, name in enumerate(source["columns"])}
    appid_i, current_i = cols["appid"], cols["current"]
    games = sorted(source["games"], key=lambda g: float(g[current_i] or 0), reverse=True)
    result = []
    for game in games:
        appid = game[appid_i]
        if isinstance(appid, int) and appid > 0 and appid not in result:
            result.append(appid)
        if len(result) >= LIMIT:
            break
    return result


def get_current_players(appid):
    req = urllib.request.Request(API_URL.format(appid), headers={
        "User-Agent": "LudoScope-Academic-Market-Research/1.0",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=12) as response:
        payload = json.load(response)
    result = payload.get("response", {})
    if result.get("result") != 1 or not isinstance(result.get("player_count"), int):
        raise ValueError(f"invalid response for {appid}: {result!r}")
    return max(0, result["player_count"])


def collect():
    ids = candidate_ids()
    values, errors = {}, []
    for index, appid in enumerate(ids):
        try:
            values[str(appid)] = get_current_players(appid)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            errors.append(f"appid={appid} {str(exc)[:120]}")
        if index < len(ids) - 1:
            time.sleep(0.5)  # controlled request pace
    if len(values) < 5:
        raise RuntimeError(f"Only {len(values)} API requests succeeded; refusing to publish stale data. {errors[:3]}")
    payload = {
        "source": "Steam Web API",
        "endpoint": "ISteamUserStats/GetNumberOfCurrentPlayers/v1",
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "candidate_count": len(ids),
        "success_count": len(values),
        "players": values,
    }
    tmp = OUTPUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    tmp.replace(OUTPUT)
    print(f"Updated {len(values)}/{len(ids)} Steam games. Failed AppIDs: {errors[:8]}")


if __name__ == "__main__":
    collect()
