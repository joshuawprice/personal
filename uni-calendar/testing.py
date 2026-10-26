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
ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjgwREU5MzQ2RjA5MEFGMDI4MjUwRjUyNzQ1QjMwMjkwMDYyM0RBQ0VSUzI1NiIsIng1dCI6ImdONlRSdkNRcndLQ1VQVW5SYk1Da0FZajJzNCIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgubXlkYXkuY2xvdWQiLCJuYmYiOjE3OTI0NDM3MDAsImlhdCI6MTc5MjQ0MzcwMCwiZXhwIjoxNzkyNTMwMTAwLCJhdWQiOiJteWRheS13ZWItNGUwZjExZjktMDQ2ZS00NTA1LTljYjgtZGIyMTUyMzExZTIxIiwiYW1yIjpbImV4dGVybmFsIl0sIm5vbmNlIjoiTjAuNzU4MDMzNjY3NDE4MzgxNTE3OTI0NDM2ODUwMjQiLCJjX2hhc2giOiJ0b0tFc1pLNV8yZ2ZERWNWZHB0UDJRIiwic2lkIjoiNkZFOUY0RUJGQTc4OTk5NkRGMDE0ODhFMTlGOUY3OUYiLCJzdWIiOiI2YTAwNWI0ZC0xYzdlLTQzMzQtODg1NS0zMjU2NmVkNzcwNmIiLCJhdXRoX3RpbWUiOjE3OTI0NDM3MDAsImlkcCI6ImFhZCIsIm15ZGF5X3NpZCI6IjZGRTlGNEVCRkE3ODk5OTZERjAxNDg4RTE5RjlGNzlGIiwicm9sZSI6InN0ZCIsInRlbmFudCI6IjRlMGYxMWY5LTA0NmUtNDUwNS05Y2I4LWRiMjE1MjMxMWUyMSIsInByZWZlcnJlZF91c2VybmFtZSI6IjI2MjA2NTNAc3R1ZGVudC51d3RzZC5hYy51ayIsImdpdmVuX25hbWUiOiJKb3NodWEiLCJmYW1pbHlfbmFtZSI6IlByaWNlIiwibmFtZSI6Ikpvc2h1YSBQcmljZSAoMjYyMDY1MykiLCJlbWFpbCI6IjI2MjA2NTNAc3R1ZGVudC51d3RzZC5hYy51ayIsInVwZGF0ZWRfYXQiOiIyMDI2LTA5LTI5VDE0OjQyOjM4WiIsInJvbGVfcGVybWlzc2lvbiI6WyJUZW5hbnRSZWFkIiwiVXNlclJlYWQiXSwiX2NsYWltX25hbWVzIjp7Imdyb3VwcyI6InNyYzEifSwiX2NsYWltX3NvdXJjZXMiOnsic3JjMSI6eyJlbmRwb2ludCI6Imh0dHBzOi8vYXV0aC5teWRheS5jbG91ZC9hcGkvZ3JvdXBzX2NsYWltcyJ9fX0.ljqW8WOZ8DI_uut77lUIqBGYTrW1ne_Fsn-4OvpBB_JyeH8YLCOtb1e7wUyd4CUkimJXXbwHexwHfrh2_HKpjeYSI8tezMYYeUEW7ofrJ5XQVucq8OPjmcQ3ahLm_B-5fqLa29aqNwnqCRt9ELIPW1QMcaYbjoiLFqC4l4zC3dXCPKwbtzWC3qYEteF91YynRhE5pl69CB0RXxVgYNV8QjpEx3zSOrM8EPcmdqtm6gDs9x769gRpgJ9kBVSe40Y7Q9D_DfAYUWj53ClAZZtjAgbVBWClzZSPgqOYSVrhnvkcDRtxyi_fOFatBoLBVaRFjD1mGSKrnvIflfTqcfwO_DeVPUkYUkvAru4UOZzIgXnl9TtYJvmKE0iVt79UAjQCoHj-xrkM9GAm358PTNaxOVoaRizLf4jnq5zF_OmI8UKzsg3opghvH44UsGbMc1oFvdJAcqqjK-GBT93zc1dfa0nULT3brf4Cnult7WF2l5zleP3BNi2LK9Z-Y_D3jAatrteybiJrMNlEfJYhlNWBjocxMlHSj6cWb72DymqwjnXz41mRAtROOXDmLcAxaMYpSCn8L_giw2z8eZmSoYkAG32VRye1PdWwAdk4g9M0KZzeKXCdXTSiYE3tjTuxLNo5RVS60dgoc5EaFQFw9dsguyh7aDE4MuRUfJFL0xD8cbM"


def renew(s):
    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "get_token",  # guess: e.g. "refresh_token" or a custom value
            "client_id": CLIENT_ID,
            # "device_code": s["device_code"],  # confirm field name in DevTools
            "id_token": ID_TOKEN,
            "code": "AiRgALWdQBNrkGJoeEvRkGio",
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


s = {"device_code": "AiRgALWdQBNrkGJoeEvRkGio"}

renew(s)

print(s)
