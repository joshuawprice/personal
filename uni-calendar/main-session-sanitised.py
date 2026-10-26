import json
from datetime import UTC, datetime
from time import sleep

import requests

SESSION_EXTEND_URL = "https://api.myday.cloud/sessions/session/<session>/extend"
TOKEN_URL = "https://api.myday.cloud/sessions/token"
CLIENT_ID = "myday-web-4e0f11f9-046e-4505-9cb8-db2152311e21"
CALENDAR_URL = "https://api.myday.cloud/legacy/api/aggregate/v2/calendaritem?$filter=End%20gt%20datetime%272026-09-28T00:00:00Z%27%20and%20Start%20lt%20datetime%272026-11-09T00:00:00Z%27"
ID_TOKEN = ""
CODE = ""


def session_extend(token: str):
    print("Renewing access token...")
    r = requests.post(
        SESSION_EXTEND_URL,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    r.raise_for_status()
    d = r.json()
    print(datetime.now(UTC))
    print("sessionExpires:", d["sessionExpires"])
    print("sessionExpiresInSecs:", d["sessionExpiresInSecs"])


def renew():
    print("Renewing access token...")
    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "get_token",
            "client_id": CLIENT_ID,
            "id_token": ID_TOKEN,
            "code": CODE,
        },
    )
    r.raise_for_status()
    d = r.json()
    print(datetime.now(UTC))
    print("access_token:", d["access_token"])
    print("expires_in:", d["expires_in"])
    return d["access_token"]


while True:
    access_token: str
    for i in range(4):
        access_token = renew()
        sleep(3540)

    session_extend(access_token)
