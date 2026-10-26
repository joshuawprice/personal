import json
import time
from pathlib import Path

import requests

STATE = Path(
    "myday_state.json"
)  # {"device_code": "...", "access_token": "...", "expires_at": 0}
TOKEN_URL = "https://api.myday.cloud/sessions/token"
CLIENT_ID = "myday-web-4e0f11f9-046e-4505-9cb8-db2152311e21"
CALENDAR_URL = "https://api.myday.cloud/..."  # your calendar request
ID_TOKEN = ""


def renew(s):
    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "get_token",  # guess: e.g. "refresh_token" or a custom value
            "client_id": CLIENT_ID,
            # "device_code": s["device_code"],  # confirm field name in DevTools
            "id_token": ID_TOKEN,
            "code": "",
        },
    )
    r.raise_for_status()
    d = r.json()
    s["access_token"] = d["access_token"]
    s["expires_at"] = time.time() + d.get("expires_in", 3600)
    # in case the server rotates it:
    s["device_code"] = d.get("properties", {}).get("device_code", s["device_code"])
    STATE.write_text(json.dumps(s))
    return s


def get_calendar():
    s = json.loads(STATE.read_text())
    if time.time() > s.get("expires_at", 0) - 300:
        s = renew(s)
    r = requests.get(
        CALENDAR_URL, headers={"Authorization": f"Bearer {s['access_token']}"}
    )
    if r.status_code == 401:
        s = renew(s)
        r = requests.get(
            CALENDAR_URL, headers={"Authorization": f"Bearer {s['access_token']}"}
        )
    r.raise_for_status()
    return r.json()


s = {"device_code": ""}

renew(s)

print(s)
